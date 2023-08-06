import asyncio
import glob
import json
import logging
import operator
import os
import sys
import time
from functools import reduce
from io import StringIO
from typing import List, Dict, Optional

import requests
from nubia import argument
from nubia import command
from nubia import context
from sample_sheet import SampleSheet, Sample
from seqslab.exceptions import async_exception_handler, exception_handler
from seqslab.runsheet.runsheet import RunSheet
from tabulate import tabulate
from termcolor import cprint
from yarl import URL

from . import __version__, API_HOSTNAME
from .api.common import drs_register
from .internal import aiocopy
from .internal import utils
from .internal.common import get_factory
import csv
import errno

"""
Copyright (C) 2021, Atgenomix Incorporated.

All Rights Reserved.

This program is an unpublished copyrighted work which is proprietary to
Atgenomix Incorporated and contains confidential information that is not to
be reproduced or disclosed to any other person or entity without prior
written consent from Atgenomix, Inc. in each and every instance.

Unauthorized reproduction of this program as well as unauthorized
preparation of derivative works based upon the program or distribution of
copies by sale, rental, lease or lending are violations of federal copyright
laws and state trade secret laws, punishable by civil and criminal penalties.
"""


class BaseDatahub:
    DRS_SEARCH_URL = f"https://{API_HOSTNAME}/ga4gh/drs/{__version__}/objects/search/"

    def __init__(self,
                 workspace: str = None,
                 ):
        self._workspace = workspace

    @property
    def proxy(self) -> str:
        """web proxy server"""
        return context.get_context().args.proxy

    @property
    def workspace(self) -> str:
        """user workspace"""
        return self._workspace

    @staticmethod
    @exception_handler
    def _upload(src: URL, dst: URL, recursive: bool, **kwargs) -> list:
        # copy from local to cloud
        paths = glob.glob(src.path)
        if not len(paths):
            raise FileNotFoundError("--src Enter a valid src path. ")

        if 1 == len(paths):
            if os.path.isdir(paths[0]):
                if not recursive:
                    raise OSError("--recursive (-r) is Required.")
                coro = aiocopy.dir_to_blob(URL(*paths), dst, **kwargs)
            else:
                coro = aiocopy.file_to_blob([URL(*paths)], dst, **kwargs)
        else:
            if os.path.splitext(str(dst))[1]:
                raise OSError('--dst Enter a valid dst path.')
            files = []
            dirs = []
            for p in paths:
                if os.path.isfile(p):
                    files.append(URL(p))
                else:
                    dirs.append(URL(p))
            if len(dirs) != 0:
                for dir_path in dirs:
                    for root, folderlist, filelist in os.walk(str(dir_path)):
                        if filelist:
                            abs_paths = [URL(os.path.join(root, file)) for file in filelist]
                            files.extend(abs_paths)
            coro = aiocopy.file_to_blob(files, dst, **kwargs)

        results = asyncio.run(coro)
        for result in results:
            if result['status'] != 'complete':
                raise ValueError(json.dumps(results, indent=4))
        return results

    @staticmethod
    def _upload_nonexistence(src: URL, dst: URL, excludes: list[URL], label_matching: bool, **kwargs) -> list:
        urls = []

        for dir_path, _, files in os.walk(str(src)):
            # exclude filtering
            exc = False
            for e in excludes:
                if dir_path.find(str(e)) != -1:
                    exc = True
            if exc:
                continue

            # file matching
            for f in files:
                url = URL(os.path.join(dir_path, f))
                if not asyncio.run(utils.drs_existence(path=url, label_check=label_matching)):
                    urls.append(url)

        cprint(f'files to upload')
        for p in urls:
            cprint(str(p))
        coro = aiocopy.file_to_blob(urls, dst, **kwargs)
        results = asyncio.run(coro)
        return results

    @staticmethod
    def _stdout(results: List[dict], output: str) -> int:
        """
            stdout:: support different format [json, tsv, table]
        """
        if output == "tsv":
            s = StringIO()
            writer = csv.DictWriter(s, fieldnames=list(results[0].keys()))
            writer.writeheader()
            for result in results:
                writer.writerow(result)
            s.seek(0)
            content = s.read().replace(',', '\t')
            cprint(content)
        elif output == 'table':
            table_header = list(results[0].keys())
            table_datas = [result.values() for result in results]
            cprint(tabulate(
                tabular_data=table_datas,
                headers=table_header,
                tablefmt='pipe'
            ))
        else:
            cprint(json.dumps(results, indent=4))
        return 0

    @staticmethod
    def _stdin() -> list:
        payload = sys.stdin.readlines()
        try:
            jsons = json.loads(''.join(payload))
            if not isinstance(jsons, list):
                jsons = [jsons]
            return jsons
        except json.JSONDecodeError:
            raise ValueError(
                f'Stdin format only support json. Please read the document and make sure the format is valid.')

    @command(aliases=["copy"])
    @argument("src",
              type=URL,
              positional=False,
              description="source directory, file path, or DRS url", )
    @argument("dst",
              type=URL,
              positional=False,
              description="destination directory, file path, or DRS url")
    @argument("recursive",
              type=bool,
              positional=False,
              description="copy an entire directory tree",
              aliases=["r"])
    @argument("concurrency",
              type=int,
              positional=False,
              description="The numbers of concurrency you want to upload per file. "
                          "Not recommended to adjust. (Default = 0, auto scale)")
    @argument("multiprocessing",
              type=int,
              positional=False,
              description="The numbers of file you want to upload per time. "
                          "Not recommended to adjust. (Default = 1)")
    @argument("chunk_size",
              type=str,
              positional=False,
              description="The numbers of size you want to upload per file. "
                          "Not recommended to adjust. (Default = 8MB)",
              choices=['8', '16'])
    @argument("output",
              type=str,
              positional=False,
              description="The format of the stdout. (Default = json)",
              choices=['json', 'table', 'tsv'])
    @argument("white_list",
              type=Optional[str],
              positional=False,
              description="The path of White list for copying entire directory")
    def upload(
            self, src: URL, dst: URL = URL('/'), recursive: bool = False, output: str = 'json',
            concurrency: int = 0, multiprocessing: int = 1, chunk_size: str = '8',
            white_list: Optional[str] = None
    ) -> int:
        """
        copy data between your local file system and SeqsLab DataHub cloud service,
        within the cloud service, and between cloud storage providers.
        """

        def __log(results: List[dict], output: str):
            self._stdout(results=results, output=output)
            for _, r in enumerate(results):
                msg = "Copy {name} {size}) is {status}".format(
                    name=r.get('name'), size=r.get('size'), status=r.get('status')
                )
                if r.get('status') == "failed":
                    logging.error(msg)
                elif r.get('status') == "partial":
                    logging.error(msg)
                else:
                    logging.info(msg)

        size = {
            '8': 8 * 1024 * 1024,
            '16': 16 * 1024 * 1024,
        }
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Enter a valid workspace name.", "red")
            return errno.EINVAL

        if str(dst).isspace() or len(str(dst)) == 0:
            logging.error("Invalid dst path")
            cprint("Enter a valid dst path.", "red")
            return errno.EINVAL

        if os.path.isdir(str(src)):
            if not str(dst).endswith('/'):
                dst = URL(f'{str(dst)}/')
            if str(src).endswith('/'):
                src = URL(f'{str(src).rstrip("/")}')

        result = self._upload(src=src, dst=dst, recursive=recursive, workspace=self.workspace,
                              multiprocessing=multiprocessing, concurrency=concurrency,
                              chunk_size=size[chunk_size], proxy=self.proxy, white_list=white_list)
        if isinstance(result, int):
            return result
        __log(result, output)
        return 0

    @command
    @argument("drs_ids",
              type=List[str],
              positional=False,
              description="The list of DRS object id. (Required if no self_uris)")
    @argument("self_uris",
              type=List[URL],
              positional=False,
              description="The list of DRS self uri. (Required if no drs_ids)")
    @argument("dst",
              type=str,
              positional=False,
              description="destination directory, file path")
    @argument("bandwidth",
              type=str,
              positional=False,
              description="The numbers of mbps you want to download per round."
                          "If the setting number is bigger than your network bandwidth,"
                          "it will take all your bandwidth to run the command."
                          "Not recommended to adjust. (Default = 160)",
              choices=['20', '40', '80', '120', '160'])
    @argument("chunk_size",
              type=str,
              positional=False,
              description="The numbers of size you want to download per file. "
                          "If the numbers of size > 4MB, no md5 checking."
                          "Not recommended to adjust. (Default = 4MB)",
              choices=['16', '32'])
    @argument("output",
              type=str,
              positional=False,
              description="The format of the stdout. (Default = json)",
              choices=['json', 'table', 'tsv'])
    @argument("overwrite",
              type=bool,
              positional=False,
              description="overwrite the exist files.(Default = False)")
    @argument("multiprocessing",
              type=int,
              positional=False,
              description="The numbers of file you want to upload per round."
                          "Not recommended to adjust. (Default = 1)")
    def download(self, dst: str, drs_ids: List[str] = None, self_uris: List[URL] = None, overwrite: bool = False,
                 output: str = 'json', chunk_size: str = '16', bandwidth: str = '160', multiprocessing: int = 1) -> int:
        """
                copy data between your local file system and SeqsLab DataHub cloud service,
                within the cloud service, and between cloud storage providers.
        """

        def __log(results: List[dict], output: str):
            self._stdout(results=results, output=output)
            for _, r in enumerate(results):
                msg = "Copy {uri}({size}) is {status}".format(
                    uri=r['dst'], size=r['size'], status=r['status']
                )
                if r['status'] == "failed":
                    logging.error(msg)
                elif r['status'] == "partial":
                    logging.error(msg)
                else:
                    logging.info(msg)

        size = {
            '16': 16 * 1024 * 1024,
            '32': 32 * 1024 * 1024
        }
        bandwidths = {
            '20': 4,
            '40': 8,
            '80': 20,
            '120': 60,
            '160': 120,
        }
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Invalid workspace name", "red")
            return errno.EINVAL

        if not drs_ids:
            if not self_uris:
                logging.error("Invalid executions, Enter a list of valid drs_ids or a list of valid self_uris.")
                cprint("Invalid executions, Enter a list of valid drs_ids or a list of valid self_uris.", "red")
                return errno.EINVAL
        else:
            if self_uris:
                logging.error("Invalid executions, Enter a list of valid drs_ids or a list of valid self_uris,"
                              "not both given.")
                cprint("Invalid executions, Enter a list of valid drs_ids or a list of valid self_uris,"
                       "not both given.", "red")
                return errno.EINVAL
        tasks = []
        kwargs = {}
        objs = drs_ids if drs_ids else self_uris
        if len(objs) > 1 and not os.path.isdir(dst):
            logging.error("Invalid executions, Enter a valid dst directory for multi-objects download", "red")
            cprint("Invalid executions, Enter a valid dst directory for multi-objects download", "red")
            return errno.EINVAL
        for obj in set(objs):
            if isinstance(obj, URL):
                drs_id = obj.name
                if obj.host:
                    kwargs['self_uri_host'] = obj.host
            else:
                drs_id = obj
            tasks.append(
                self._download(drs_id=drs_id, dst=dst, workspace=self.workspace, chunk_size=size[chunk_size],
                               bandwidth=bandwidths[bandwidth], proxy=self.proxy, overwrite=overwrite,
                               multiprocessing=multiprocessing, **kwargs))
        loop = asyncio.get_event_loop()
        results, _ = loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        result = []
        for r in results:
            if isinstance(r.result(), int):
                continue
            result.extend(r.result())

        if not result:
            return errno.EINVAL
        __log(result, output)
        return 0

    @staticmethod
    @async_exception_handler
    async def _download(drs_id: str, dst: str, **kwargs):
        backend = get_factory().load_storage(kwargs.get('workspace'))
        download_info = await backend.expand_blob(drs_id=drs_id, **kwargs)
        dst = os.path.abspath(os.path.expanduser(dst))
        files = download_info['files']
        kwargs['size'] = [file['size'] for file in files]
        kwargs['access_url'] = download_info['access_url']
        kwargs['token'] = download_info['token']['Authorization']
        if 1 == len(files):
            if os.path.isdir(dst):
                coro = await aiocopy.blobfile_to_dir(src=URL(files[0]['path']), dir=URL(dst), **kwargs)
            else:
                coro = await aiocopy.blobfile_to_file(src=URL(files[0]['path']), file=URL(dst), **kwargs)

        else:
            coro = await aiocopy.blobdir_to_dir(srcs=[URL(file['path']) for file in files], dir=URL(dst), **kwargs)
        return coro

    @command
    @argument("type",
              type=str,
              positional=True,
              description="If you want to register a file as a blob , please choose a file-blob. "
                          "If you want to register a folder as a blob , please choose a folder-blob. "
                          "If you want to register a folder as a bundle, please register each file "
                          "one by one as a blob, register the folder as a bundle, "
                          "and then pass the DRS object_ids for each of the blobs via the object_id interface. "
                          "(Required)",
              choices=['file-blob', 'folder-blob', 'bundle'])
    @argument("name",
              type=str,
              description="The name of the object you want to register. "
                          "(Required not in stdin mode)", )
    @argument("file_type",
              type=str,
              description="The file_type of the object you want to register. "
                          "(Required not in stdin mode) "
                          "Example: application/json", )
    @argument("mime_type",
              type=str,
              description="The mime-type of the object you want to register. "
                          "(Required not in stdin mode) "
                          "Example: application/json", )
    @argument("description",
              type=str,
              description="The description of the object you want to register. "
                          "(Optional)")
    @argument("aliases",
              type=List[str],
              description="The aliases of the object you want to register. "
                          "(Optional)")
    @argument("tags",
              type=List[str],
              positional=False,
              description="The tags of the object you want to register. "
                          "(Optional)", )
    @argument("created_time",
              type=str,
              positional=False,
              description="The created time of the object you want to register. "
                          "The created time is the time that the object first time created in storage. "
                          "The created_time format must be in RFC3339. "
                          "If drs_type=blob (Required not in stdin mode)"
                          "Example: 2021-09-13 02:54:03.636044+00:00")
    @argument("updated_time",
              type=str,
              positional=False,
              description="The updated time of the object you want to register. "
                          "The updated time is the time that the object updated in storage. "
                          "The updated time format must be in RFC3339. "
                          "If drs_type=blob (Required not in stdin mode)"
                          "Example: 2021-09-13 02:54:03.636044+00:00")
    @argument("size",
              type=int,
              positional=False,
              description="The size of object you want to register. "
                          "If drs_type=blob (Required not in stdin mode)", )
    @argument("urls",
              type=List[URL],
              description="The absolute path of object you want to register. "
                          "If drs_type=blob (Required not in stdin mode)")
    @argument("access_tiers",
              type=str,
              description="The access_tier of the object you want to register. "
                          "If drs_type=bundle, please ignore. (Required not in stdin mode)",
              choices=['Hot', 'Cool', 'Archive'])
    @argument("regions",
              type=List[str],
              description="The region of the storage where the object you want to register was stored. "
                          "If drs_type=blob (Required not in stdin mode)"
                          "Example: local, westus, eastjp etc ...")
    @argument("Authorizations",
              type=List[str],
              description="The Authorization to the storage where the object you stored. "
                          "(Optional)")
    @argument("checksum",
              type=str,
              positional=False,
              description="The checksum of the object you want to register. "
                          "The checksum_type must be sha256. "
                          "If drs_type=blob (Required not in stdin mode)")
    @argument("checksum_type",
              type=str,
              positional=False,
              description="The type of the checksum. (Required not in stdin mode)",
              choices=['sha256'])
    @argument("metadata",
              type=Dict,
              positional=False,
              description="The metadata of the the object you want to register. "
                          "(Optional)")
    @argument("stdin",
              type=bool,
              positional=False,
              description="stdin mode or not (Optional)")
    @argument("output",
              type=str,
              positional=False,
              description="The format of the stdout. (Default = json) (Optional)",
              choices=['json', 'table', 'tsv'])
    @argument("drs_id",
              type=str,
              positional=False,
              description="The customized drs object id. (Optional)")
    def register(self, type: str, output: str = 'json', stdin: bool = False, **kwargs) -> int:
        """
            drs register
        """

        def __log(results: List[dict], output: str):
            self._stdout(results=results, output=output)
            for r in results:
                msg = f"Register {r['id']}  is complete."
                logging.info(msg)

        if not self.workspace:
            cprint('Enter a valid workspace', 'red')
            return errno.EINVAL

        if "blob" in type:
            """
                blob register
            """
            results = self._register(drs_type=type, stdin=stdin, workspace=self.workspace, **kwargs)
            if isinstance(results, int):
                return results
            __log(results=results, output=output)
            return 0
        else:
            """
                bundle register
            """
            raise NotImplementedError('Not implemented yet.')

    @staticmethod
    @exception_handler
    def _register(drs_type: str, stdin: bool, workspace: str, **kwargs) -> list[dict]:
        backend = drs_register().load_register(workspace)
        if stdin:
            if len(kwargs):
                raise ValueError(f'Stdin mode does not support these commands {kwargs.keys()}.')
            payloads = backend.create_payload(stdin=BaseDatahub._stdin(), type=drs_type, **kwargs)
        else:
            payloads = [{
                "name": kwargs.get('name'),
                "mime_type": kwargs.get('mime_type'),
                "file_type": kwargs.get('file_type'),
                "created_time": kwargs.get('created_time'),
                "updated_time": kwargs.get('updated_time') if kwargs.get('updated_time') else kwargs.get(
                    'created_time'),
                "size": kwargs.get('size'),
                "access_methods": [
                    {'type': url.scheme,
                     'access_url': {
                         'url': url,
                         'headers': {
                             "Authorization": kwargs.get('Authorizations')[i] if kwargs.get('Authorizations') else None
                         }
                     },
                     "access_tier": kwargs.get('access_tiers'),
                     "region": kwargs.get('regions')[i]} for i, url in enumerate(kwargs.get('urls'))
                ] if kwargs.get('urls') else [],
                "checksums": [{
                    "checksum": kwargs.get('checksum'),
                    "checksum_type": kwargs.get('checksum_type'),
                }],
                "description": kwargs.get('description'),
                "aliases": kwargs.get('aliases'),
                "metadata": kwargs.get('metadata'),
                "tags": kwargs.get('tags'),
                "id": kwargs.get('drs_id')
            }]

        results = backend.muti_register(drs_type='bundle' if drs_type == 'bundle' else 'blob', payloads=payloads)
        return results

    @command(aliases=["clean"])
    @argument("names",
              type=List[str],
              positional=False,
              description="a list of names"
                          "(Optional)")
    @argument("tags",
              type=List[str],
              positional=False,
              description="tag to match drs datasets"
                          "(Optional)")
    def delete(
            self,
            tags: List[str] = [],
            names: List[str] = [],
    ) -> int:
        """
        clear drs object by names or by tags.
        """
        if not names and not tags:
            cprint("Either give names or tags to do drs query", "red")
            return errno.ENOENT

        try:
            asyncio.run(utils.drs_delete(names, tags))

        except OSError as error:
            cprint(f"{error}", "red")
            return errno.ENOENT
        except requests.HTTPError as error:
            cprint(f"{error}", "red")
            return errno.ECONNREFUSED
        except LookupError as error:
            cprint(f"{error}", "red")
            return errno.EINVAL

        return 0

    @command(aliases=["search"])
    @argument("names",
              type=List[str],
              positional=False,
              description="a list of names"
                          "(Optional)")
    @argument("tags",
              type=List[str],
              positional=False,
              description="tag to match drs datasets"
                          "(Optional)")
    def search(
            self,
            tags: List[str] = [],
            names: List[str] = [],
    ) -> int:
        """
        search drs object either by names or by tags.  Cannot submit names and tags at the same time.
        """
        if not names and not tags:
            cprint("Either give names or tags to do drs query", "red")
            return errno.ENOENT
        if names and tags:
            cprint("search condition names and tags cannot be given at the same time", "red")
            return errno.ENOENT

        try:
            result = asyncio.run(utils.drs_search(names, tags))
            cprint(json.dumps(result, indent=4))

        except OSError as error:
            cprint(f"{error}", "red")
            return errno.ENOENT
        except requests.HTTPError as error:
            cprint(f"{error}", "red")
            return errno.ECONNREFUSED
        except LookupError as error:
            cprint(f"{error}", "red")
            return errno.EINVAL

        return 0

    @staticmethod
    def find_fastq_paths(sample: Sample, fastq_path: str) -> list[str]:
        return [os.path.join(root, f) for root, dirs, files in os.walk(fastq_path) for f in files
                if f.find(f'{sample.Sample_ID}') != -1 and f.rfind('fastq.gz') != -1]

    @staticmethod
    def find_fqs(
            fastq_path: str,
            run_sheet_path: str
    ) -> list:
        """
        create upload list based on run_sheet and fastq path
        """
        run_sheet = RunSheet(run_sheet_path)
        hdr_meta = {k.replace(' ', '_'): v for k, v in run_sheet.Header.items()}
        overall_idx = 0
        upload_info = []
        for s in run_sheet.samples:
            overall_idx += 1
            sample_meta = {k.replace(' ', '_'): v for k, v in s.to_json().items()}
            sample_meta.update({"Order_Overall": str(overall_idx)})
            id_rule = s.get('Drs_ID', None)

            fq_paths = BaseDatahub.find_fastq_paths(s, fastq_path)
            if run_sheet.is_single_end:
                assert len(fq_paths) == 1
                upload_info.append({
                    "src": fq_paths[0],
                    "dst": fq_paths[0],
                    "tags": [f"{s.get('Run_Name', run_sheet.Header.Date)}/{s.get('Read1_Tag', '')}"],
                    "metadata": {"header": hdr_meta, "sample": sample_meta, "file": {"Pair": "1"}}
                })
                if id_rule:
                    upload_info[-1]['id'] = BaseDatahub._gen_drs_id(id_rule, upload_info[-1]['metadata'])

            if run_sheet.is_paired_end:
                assert len(fq_paths) == 2
                fq_paths.sort()
                upload_info.append({
                    "src": fq_paths[0],
                    "dst": fq_paths[0],
                    "tags": [f"{s.get('Run_Name', run_sheet.Header.Date)}/{s.get('Read1_Tag', '')}"],
                    "metadata": {"header": hdr_meta, "sample": sample_meta, "file": {"Pair": "1"}}
                })
                upload_info.append({
                    "src": fq_paths[1],
                    "dst": fq_paths[1],
                    "tags": [f"{s.get('Run_Name', run_sheet.Header.Date)}/{s.get('Read2_Tag', '')}"],
                    "metadata": {"header": hdr_meta, "sample": sample_meta, "file": {"Pair": "2"}}
                })
                if id_rule:
                    upload_info[-1]['id'] = BaseDatahub._gen_drs_id(id_rule, upload_info[-1]['metadata'])
                    upload_info[-2]['id'] = BaseDatahub._gen_drs_id(id_rule, upload_info[-2]['metadata'])

        return upload_info

    @staticmethod
    def _gen_drs_id(rule: str, meta: dict, separator='-', bracket='{}') -> str:
        content = []
        for kw in rule.split(separator):
            i = kw.strip(bracket)
            try:
                val = reduce(operator.getitem, i.split('.'), meta).replace('/', '-')
                content.append(val)
            except:
                raise RuntimeError('Illegal tag rule - rule must start with either header or sample')

        return '_'.join(filter(None, content))

    @command(aliases=["runsheet"])
    @argument("input_dir",
              type=str,
              positional=False,
              description="fastq file path")
    @argument("upload_dst",
              type=str,
              positional=False,
              description="upload destination path. (Default = input_dir)")
    @argument("run_sheet",
              type=str,
              positional=False,
              description="run sheet path")
    @argument("concurrency",
              type=int,
              positional=False,
              description="The numbers of concurrency you want to upload per file. "
                          "Not recommended to adjust. (Default = 0, auto scale)")
    @argument("multiprocessing",
              type=int,
              positional=False,
              description="The numbers of file you want to upload per time. "
                          "Not recommended to adjust. (Default = 1)")
    def upload_runsheet(self, input_dir: str, run_sheet: str, upload_dst: str = None,
                        concurrency: int = 0, multiprocessing: int = 1) -> int:
        """
        sample upload based on run_sheet and fastq path
        """
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Invalid workspace name", "red")
            return errno.EINVAL
        failed = False
        upload_payload = BaseDatahub.find_fqs(input_dir, run_sheet)
        ret = []
        for payload in upload_payload:
            dst = upload_dst if upload_dst else payload.get('dst')
            result = self._upload(src=URL(payload.get('src')),
                                  dst=URL(dst),
                                  recursive=False,
                                  workspace=self.workspace,
                                  multiprocessing=multiprocessing,
                                  concurrency=concurrency,
                                  proxy=self.proxy)[0]
            result['metadata'] = payload.get('metadata')
            result['tags'] = payload.get('tags')
            if payload.get('id'):
                result['id'] = payload.get('id')
            ret.append(result)
            if result['status'] != 'complete':
                failed = True
        cprint(json.dumps(ret, indent=4), 'yellow')

        # use non-zero return code to indicate upload failed scenario
        if failed:
            return -1
        return 0

    @command(aliases=["patch"])
    @argument("id",
              type=str,
              positional=True,
              description="drs object id.(Required)")
    @argument("name",
              type=str,
              positional=False,
              description="drs object name. (Optional)")
    @argument("tags",
              type=List[str],
              positional=False,
              description="drs object tags. (Optional)")
    @argument("metadata",
              type=dict,
              positional=False,
              description="drs object metadata. (Optional)")
    @argument("checksum",
              type=str,
              positional=False,
              description="drs object checksum. (Optional)")
    @argument("checksum_type",
              type=str,
              positional=False,
              description="The type of the checksum. (Required not in stdin mode)",
              choices=['sha256'])
    @argument("updated_time",
              type=str,
              positional=False,
              description="The updated time of the object."
                          "The updated time format must be in RFC3339. "
                          "Example: 2021-09-13 02:54:03.636044+00:00")
    @argument("stdin",
              type=bool,
              positional=False,
              description="stdin mode or not (Optional)")
    def update(self, id: str, stdin: bool = False, **kwargs) -> int:
        """
         Update a drs object
        """
        if not self.workspace:
            cprint('Enter a valid workspace', 'red')
            return errno.EINVAL

        if stdin:
            if len(kwargs) > 0:
                cprint(f'Stdin mode not support {list(kwargs.keys())}')
                return errno.EINVAL
            else:
                kwargs = self._stdin()
                if len(kwargs) > 1:
                    cprint(f'Enter a valid Json not a list of Json.')
                    return errno.EINVAL
                kwargs = kwargs[0]
        else:
            checksum = kwargs.get('checksum')
            checksum_type = kwargs.get('checksum_type')
            if checksum or checksum_type:
                if not checksum or not checksum_type:
                    cprint(f'Please give both checksum and checksum_type.', 'red')
                    return errno.EINVAL
        kwargs['workspace'] = self.workspace

        def __log(results: dict):
            self._stdout(results=[results], output='json')
            msg = f"Register {results['id']}  is complete."
            logging.info(msg)

        results = self._change(id, **kwargs)
        if isinstance(results, int):
            return results
        __log(results=results)
        return 0

    @staticmethod
    @exception_handler
    def _change(object_id: str, **kwargs) -> dict:
        api_backend = drs_register().load_register(kwargs.get('workspace'))
        return api_backend.change(drs_id=object_id, **kwargs)

    @command(aliases=["retrieve"])
    @argument("id",
              type=str,
              positional=True,
              description="drs object id.(Required)")
    def get(self, id: str) -> int:
        """
            get a drs object
        """
        if not self.workspace:
            cprint('Enter a valid workspace', 'red')
            return errno.EINVAL

        def __log(results: dict):
            self._stdout(results=[results], output='json')
            msg = f"Get {results['id']}  completely."
            logging.info(msg)

        results = self._get(id, self.workspace)
        if isinstance(results, int):
            return results
        __log(results=results)
        return 0

    @staticmethod
    @exception_handler
    def _get(id: str, workspace: str):
        api_backend = drs_register().load_register(workspace)
        return api_backend.get_drs(drs_id=id)


@command
class Datahub(BaseDatahub):
    """Data Hub commands"""
    def __init__(self, workspace: str = None):
        super().__init__(workspace=workspace)
