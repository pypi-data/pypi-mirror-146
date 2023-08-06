import asyncio
import requests
import os
from seqslab.tests.util import TestShell
from seqslab.drs.commands import BaseDatahub
from os.path import abspath, dirname
from unittest import TestCase, main
from unittest.mock import patch
from yarl import URL
from functools import lru_cache
from typing import NoReturn, List
from tenacity import retry, wait_fixed, stop_after_attempt
from seqslab.drs.api.azure import AzureDRSregister
from seqslab.drs.storage.azure import BlobStorage


async def mock_drs_search(names: List[str], labels: List[str], **kwargs) -> dict:
    return {
        "objects": [
            {
                "id": "drs_lw5rvMjltsMN1Eb",
                "name": "all.zip",
                "self_uri": "drs://dev-api.seqslab.net/drs_aqaynlKB7mDSJKV",
                "size": 9277,
                "created_time": "2022-02-20T13:33:09.129376Z",
                "updated_time": "2022-02-20T13:33:09.129376Z",
                "version": "2022-02-21T05:41:49.633329Z",
                "mime_type": "application/octet-stream",
                "file_type": "zip",
                "description": None,
                "aliases": [],
                "metadata": {
                    "sample": {
                        "host": None,
                        "specimen": None,
                        "phenotype": None
                    },
                    "sequence": {
                        "library": {
                            "name": None,
                            "layout": None,
                            "strategy": None
                        },
                        "quality": {
                            "gtFP": None,
                            "score": None,
                            "fscore": None,
                            "method": None,
                            "recall": None,
                            "queryFP": None,
                            "queryTP": None,
                            "truthFN": None,
                            "truthTP": None,
                            "precision": None
                        },
                        "platform": {
                            "udi": None,
                            "model": None
                        },
                        "readCount": None,
                        "readCoverage": None,
                        "referenceSeq": {
                            "url": None,
                            "genomeBuild": None
                        }
                    },
                    "investigation": {
                        "center": None,
                        "project": None,
                        "internalReviewBoard": None
                    }
                },
                "tags": ['andy']
            }]
    }


async def mock_drs_crud(drs_id: str, method: str, **kwargs) -> dict or NoReturn:
    if method == 'delete':
        return None
    else:
        return [
            {
                "id": "drs_lw5rvMjltsMN1Eb",
                "name": "all.zip",
                "mime_type": "application/octet-stream",
                "file_type": "zip",
                "description": None,
                "self_uri": "drs://dev-api.seqslab.net/drs_lw5rvMjltsMN1Eb",
                "size": 9277,
                "version": "2022-02-21T10:01:05.102849Z",
                "created_time": "2022-02-20T13:33:09.129376Z",
                "updated_time": "2022-02-20T13:33:09.129376Z",
                "metadata": {
                    "investigation": {
                        "center": None,
                        "internalReviewBoard": None,
                        "project": None
                    },
                    "sample": {
                        "specimen": None,
                        "host": None,
                        "phenotype": None
                    },
                    "sequence": {
                        "readCoverage": None,
                        "readCount": None,
                        "library": {
                            "name": None,
                            "strategy": None,
                            "layout": None
                        },
                        "platform": {
                            "model": None,
                            "udi": None
                        },
                        "referenceSeq": {
                            "genomeBuild": None,
                            "url": None
                        },
                        "quality": {
                            "score": None,
                            "method": None,
                            "truthTP": None,
                            "queryTP": None,
                            "truthFN": None,
                            "queryFP": None,
                            "gtFP": None,
                            "precision": None,
                            "recall": None,
                            "fscore": None
                        }
                    }
                },
                "aliases": [],
                "tags": [],
                "checksums": [
                    {
                        "type": "sha256",
                        "checksum": "598ad6f0c6130fb506a530d006f6cfe970c13e1a8aee76881ec2191704fe83b1"
                    }
                ],
                "access_methods": [
                    {
                        "type": "https",
                        "region": "westus",
                        "access_tier": "Hot",
                        "access_url": {
                            "headers": {},
                            "url": "https://atgxtestws62fccstorage.blob.core.windows.net/seqslab/drs/usr_0iDOO3rOr5Q7503/all.zip"
                        },
                        "access_id": 5480
                    }
                ]
            }
        ]


class mock_DRSregister(AzureDRSregister):
    def __init__(self, workspace: str = None):
        super(mock_DRSregister, self).__init__(workspace=workspace)
        self.pay_load = [
            {
                "id": "drs_lw5rvMjltsMN1Eb",
                "name": "all.zip",
                "mime_type": "application/octet-stream",
                "file_type": "zip",
                "description": None,
                "self_uri": "drs://dev-api.seqslab.net/drs_lw5rvMjltsMN1Eb",
                "size": 9277,
                "version": "2022-02-21T10:01:05.102849Z",
                "created_time": "2022-02-20T13:33:09.129376Z",
                "updated_time": "2022-02-20T13:33:09.129376Z",
                "metadata": {
                    "investigation": {
                        "center": None,
                        "internalReviewBoard": None,
                        "project": None
                    },
                    "sample": {
                        "specimen": None,
                        "host": None,
                        "phenotype": None
                    },
                    "sequence": {
                        "readCoverage": None,
                        "readCount": None,
                        "library": {
                            "name": None,
                            "strategy": None,
                            "layout": None
                        },
                        "platform": {
                            "model": None,
                            "udi": None
                        },
                        "referenceSeq": {
                            "genomeBuild": None,
                            "url": None
                        },
                        "quality": {
                            "score": None,
                            "method": None,
                            "truthTP": None,
                            "queryTP": None,
                            "truthFN": None,
                            "queryFP": None,
                            "gtFP": None,
                            "precision": None,
                            "recall": None,
                            "fscore": None
                        }
                    }
                },
                "aliases": [],
                "tags": [],
                "checksums": [
                    {
                        "type": "sha256",
                        "checksum": "598ad6f0c6130fb506a530d006f6cfe970c13e1a8aee76881ec2191704fe83b1"
                    }
                ],
                "access_methods": [
                    {
                        "type": "https",
                        "region": "westus",
                        "access_tier": "Hot",
                        "access_url": {
                            "headers": {},
                            "url": "https://atgxtestws62fccstorage.blob.core.windows.net/seqslab/drs/usr_0iDOO3rOr5Q7503/all.zip"
                        },
                        "access_id": 5480
                    }
                ]
            }
        ]

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def get_drs(self, drs_id):
        """
        api drs object
        :response: drs object json
        """
        return self.pay_load[0]

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def post_drs(self, data):
        """
        api drs object
        :param: data
        :response: drs object json
        """
        return self.pay_load

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def patch_drs(self, data, drs_id) -> dict:
        """
        partial update drs object
        :param: data
        :response: drs object json
        """
        return self.pay_load[0]


class mock_BlobStorage(BlobStorage):
    def __init__(self, workspace):
        super(mock_BlobStorage, self).__init__(workspace=workspace)

    @lru_cache(maxsize=16)
    def refresh_token(self, uri: URL, **kwargs):
        return {
            "url": f"{str(uri)}",
            "headers": {
                "Authorization": "st=9999-02-23T03%3A00%3A42Z&se=9999-02-23T04%3A00%3A42Z&sp=racwle&spr=https&sv=2020"
                                 "-06-12&sr=d&sdd=3&sig=D3XkB69gGPqNmbXLYy59X5xwrLLRIKz1brYHhCYlk0k%3D"
            }}

    @lru_cache(maxsize=16)
    def get_token(self, path: str) -> dict:
        return {
            "url": f"https://atgxtestws62fccstorage.blob.core.windows.net/seqslab/drs/usr_0iDOO3rOr5Q7503/{path}",
            "headers": {
                "Authorization": "st=9999-02-23T03%3A00%3A42Z&se=9999-02-23T04%3A00%3A42Z&sp=racwle&spr=https&sv=2020"
                                 "-06-12&sr=d&sdd=3&sig=D3XkB69gGPqNmbXLYy59X5xwrLLRIKz1brYHhCYlk0k%3D"
            }}

    @lru_cache(maxsize=16)
    def get_block_list(self, uri: URL) -> iter:
        return

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    @lru_cache(maxsize=16)
    def workspace(name) -> dict:
        return {'location': 'westus2',
                'resources': [
                    {'type': 'abfss'}
                ]}

    async def put_block(self, uri: URL, data: open, position: int, size: int,
                        base64_message: str, md5_check: bool, *args, **kwargs) -> int:
        await asyncio.sleep(1)
        return len(data)

    async def put_blocklist(
            self, uri: URL, block_id: str, *args, **kwargs
    ) -> NoReturn:
        await asyncio.sleep(1)
        return

    @staticmethod
    @lru_cache(maxsize=16)
    async def expand_blob(drs_id, **kwargs) -> list[dict] or requests.HTTPError:
        await asyncio.sleep(1)
        return {
            "access_url": "https://atgxtestws62fccstorage.blob.core.windows.net/seqslab/drs/usr_0iDOO3rOr5Q7503"
                          "/make_hg19.sh",
            "token": {
                "Authorization": "st=2022-03-14T08%3A10%3A58Z&se=2022-03-17T08%3A10%3A58Z&sp=rle&spr=https&sv=2020-06"
                                 "-12&sr=b&sig=Ha7To%2BUywhRzW8h0cDqc7qjUDaCwCt32gZBIj2PxY1A%3D "
            },
            "checksum": "sha256:29c12002dbbbcf83d56f0418020c4b83a8240b17b7373731525d44c7200bd35c",
            "files": [
                {
                    "size": 3189,
                    "path": "https://atgxtestws62fccstorage.blob.core.windows.net/seqslab/drs/usr_0iDOO3rOr5Q7503"
                            "/make_hg19.sh "
                }
            ]
        }

    async def get_blob(self, url: URL, file: str, start: int, end: int, **kwargs) -> int:
        o_fd = os.open(file, os.O_WRONLY | os.O_CREAT)
        os.lseek(o_fd, start, os.SEEK_CUR)
        os.write(o_fd, b'andy')
        os.close(o_fd)
        await asyncio.sleep(1)
        return end - start + 1


class mock_Datahub(BaseDatahub):
    """Mock Data Hub commands"""

    def __init__(self, workspace: str = None):
        super(mock_Datahub, self).__init__(workspace=workspace)


class CommandSpecTest(TestCase):
    def setUp(self) -> None:
        self.workspace = "atgxtestws"
        self.drs_id = "drs_lw5rvMjltsMN1Eb"

    @patch('seqslab.drs.storage.azure.BlobStorage', mock_BlobStorage)
    def test_command_upload(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.upload])
        # dst = absolute url file path --file_upload
        file_path = f'{dirname(abspath(__file__))}/upload/all.zip'
        value = shell.run_cli_line(
            f"test_shell upload --src {file_path} --dst abfss://seqslab@atgxtestws62fccstorage.dfs.core.windows.net"
            f"/drs/usr_0iDOO3rOr5Q7503/upload/upload/upload/all.zip")
        self.assertEqual(0, value)
        # dst = absolute url dir path --file_upload
        file_path = f'{dirname(abspath(__file__))}/upload/all.zip'
        value = shell.run_cli_line(
            f"test_shell upload --src {file_path} --dst abfss://seqslab@atgxtestws62fccstorage.dfs.core.windows.net"
            f"/drs/usr_0iDOO3rOr5Q7503/upload/upload/upload/")
        self.assertEqual(0, value)
        # dst = relative file path --file_upload
        file_path = f'{dirname(abspath(__file__))}/upload/all.zip'
        value = shell.run_cli_line(
            f"test_shell upload --src {file_path} --dst upload/upload/upload/all.zip")
        self.assertEqual(0, value)
        # dst = relative dir path --file_upload
        file_path = f'{dirname(abspath(__file__))}/upload/all.zip'
        value = shell.run_cli_line(
            f"test_shell upload --src {file_path} --dst upload/upload/upload/")
        self.assertEqual(0, value)
        # dst = absolute url dir path --folder_upload
        dir_path = f'{dirname(abspath(__file__))}/upload'
        value = shell.run_cli_line(
            f"test_shell upload --src {dir_path} --dst abfss://seqslab@atgxtestws62fccstorage.dfs.core.windows.net"
            f"/drs/usr_0iDOO3rOr5Q7503/upload/upload/upload -r")
        self.assertEqual(0, value)

    @patch('seqslab.drs.storage.azure.BlobStorage', mock_BlobStorage)
    @patch('seqslab.drs.api.azure.AzureDRSregister', mock_DRSregister)
    def test_command_download(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.download])
        dir_path = f'{dirname(abspath(__file__))}/download/'
        drs_id = '12345'
        value = shell.run_cli_line(f"test_shell download --drs-ids {drs_id} --dst {dir_path} --overwrite")
        self.assertEqual(0, value)

    @patch('seqslab.drs.api.azure.AzureDRSregister', mock_DRSregister)
    def test_command_drs_register(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.register])
        value = shell.run_cli_line(
            f"test_shell register file-blob --checksum-type sha256 --checksum "
            f"598ad6f0c6130fb506a530d006f6cfe970c13e1a8aee76881ec2191704fe83b1 --mime-type application/octet-stream "
            f"--regions westus --urls https://atgxtestws62fccstorage.blob.core.windows.net/seqslab/drs"
            f"/usr_0iDOO3rOr5Q7503/all.zip --file-type zip --name all.zip --size 9277 --access-tiers Hot "
            f"--created-time 2022-02-20T13:33:09.129376")
        self.assertEqual(0, value)

    @patch('seqslab.drs.api.azure.AzureDRSregister', mock_DRSregister)
    def test_command_drs_get(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.get])
        value = shell.run_cli_line(
            f"test_shell get {self.drs_id}")
        self.assertEqual(0, value)

    @patch('seqslab.drs.api.azure.AzureDRSregister', mock_DRSregister)
    def test_command_drs_update(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.update])
        checksum = "598ad6f0c6130fb506a530d006f6cfe970c13e1a8aee76881ec2191704fe83b1"
        updated_time = "2022-02-20T13:33:09.129376Z"
        value = shell.run_cli_line(
            f"test_shell update {self.drs_id} --name andy --tags andy2 andy3 --updated-time {updated_time} "
            f"--checksum {checksum} --checksum-type sha256")
        self.assertEqual(0, value)

    @patch('seqslab.drs.internal.utils.drs_search', mock_drs_search)
    @patch('seqslab.drs.internal.utils.drs_crud', mock_drs_crud)
    def test_command_drs_delete(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.delete])
        value = shell.run_cli_line(
            f"test_shell delete {self.drs_id} --tags andy")
        self.assertEqual(0, value)

    @patch('seqslab.drs.internal.utils.drs_search', mock_drs_search)
    def test_command_drs_search(self):
        datahub = mock_Datahub(workspace=self.workspace)
        shell = TestShell(commands=[datahub.search])
        value = shell.run_cli_line(
            f"test_shell search {self.drs_id} --tags andy")
        self.assertEqual(0, value)


if __name__ == "__main__":
    test = CommandSpecTest()
    test.setUp()
    # test.test_command_upload()
    test.test_command_download()
    # test.test_command_drs_search()
    # test.test_command_drs_delete()
    # test.test_command_drs_register()
    # test.test_command_drs_update()
    # test.test_command_drs_get()
