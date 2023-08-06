import json
import os
import zipfile
from nubia import argument
from nubia import command
from .internal.utils import create_zip
from .template.base import TrsCreateTemplate
from .template.base import TrsImagesTemplate
from pathlib import Path
from yarl import URL
from termcolor import cprint
import errno
from zipfile import ZipFile
from .resource.common import trs_resource
from seqslab.exceptions import exception_handler
from .register.common import trs_register

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


class BaseTools:
    """Tools register commands"""

    @staticmethod
    @exception_handler
    def _tool(tool_name: str, **kwargs) -> str:
        backend = trs_register().load_resource()
        return backend.tool(tool_name=tool_name, **kwargs)['id']

    @staticmethod
    @exception_handler
    def _version(tool_id: str, version_name: str, version_id: str,
                 descriptor_type: str, images: str, **kwargs) -> str:
        image_list = []
        if images:
            images_json = json.loads(images)
            for image in images_json:
                if image.get('checksum'):
                    if len(image.get('checksum').split(':')) == 2:
                        image_list.append({
                            **image,
                            "checksum_type": image.get('checksum').split(':')[0],
                            "checksum": image.get('checksum').split(':')[1]})
                    else:
                        raise ValueError(f"Wrong checksum format {image.get('checksum')} in image")
                else:
                    raise ValueError(f"No checksum in image")

        backend = trs_register().load_resource()
        version_id = backend.version(tool_id=tool_id, version_name=version_name,
                                     version_id=version_id, images=image_list,
                                     descriptor_type=descriptor_type, **kwargs)["version_id"]
        return version_id

    @staticmethod
    @exception_handler
    def _file(tool_id: str, version_id: str, descriptor_type: str, file_info: str, zip_file: str) -> str:

        if os.path.isfile(file_info):
            with open(file_info, 'r') as f:
                toolfile_json = json.loads(f.read())
        else:
            toolfile_json = BaseTools.validate_bundle_info_keys(json.loads(file_info))

        # delete name key for each dictionary
        for dic in toolfile_json:
            if dic.get('name', None):
                del dic['name']

        if not os.path.exists(zip_file):
            raise OSError(f"{zip_file} does not exist")

        backend = trs_register().load_resource()
        return backend.file(tool_id=tool_id, version_id=version_id, descriptor_type=descriptor_type,
                            toolfile_json=toolfile_json, zip_file=zip_file)

    @staticmethod
    def validate_bundle_info_keys(bundle_info: list) -> list:
        keys_desc = ['path', 'file_type', 'image_name']
        keys_other = ['path', 'file_type', ]
        ret = []
        for item in bundle_info:
            res = {}
            if 'DESCRIPTOR' in item['file_type']:
                for k in keys_desc:
                    res[k] = item[k]
            else:
                for k in keys_other:
                    res[k] = item[k]
            ret.append(res)
        return ret

    @command(aliases=[])
    @argument("name",
              type=str,
              description="The name of tool you want to register. (Required)", )
    @argument("id",
              type=str,
              description="The optional custom identifier for the tool. (Optional) "
                          "The identifier must only contain alphanumeric, hyphen, and underline.", )
    @argument("toolclass_name",
              type=str,
              description="The type of tool you want to register. (Optional)")
    @argument("toolclass_description",
              type=str,
              description="The type of tool you want to register. (Optional)")
    @argument("description",
              type=str,
              description="The description of tool you want to register. (Optional)", )
    @argument("aliases",
              type=list,
              description="The aliases of tool you want to register. (Optional)", )
    @argument("checker_url",
              type=URL,
              description="The checker_url of tool you want to register. (Optional)", )
    @argument("has_checker",
              type=bool,
              description="Whether this tool has a checker tool associated with it. (Optional)", )
    def tool(self, name: str, **kwargs) -> int:
        """
                register trs tool object.
        """
        tool_id = self._tool(tool_name=name, **kwargs)
        if isinstance(tool_id, int):
            return tool_id
        cprint(f"trs tool object - {tool_id} create complete", "yellow")
        return 0

    @command(aliases=[])
    @argument("workspace",
              type=str,
              description="The workspace according to the sign-in account.")
    @argument("tool_id",
              type=str,
              description="The id of tool you have already registered, "
                          "you plan to register the version in. (Required)", )
    @argument("name",
              type=str,
              description="The name of version you want to register. (Optional)", )
    @argument("id",
              type=str,
              description="The version of tool you want to register. (Required)"
                          "e.g. 0.1, 0.1.2, 1.0, 1.1, etc....")
    @argument("descriptor_type",
              type=str,
              description="The descriptor_type of tool you want to register in this version. (Required)",
              choices=["WDL", "CWL", "NFL"])
    @argument("images",
              type=str,
              description="The images of tool you want to register in this version. (Required)", )
    @argument("author",
              type=list,
              description="The author of tool you want to register in this version. (Optional)", )
    @argument("verified",
              type=bool,
              description="This version of tool you want to register is verified or not. Default: False (Optional)", )
    @argument("verified_source",
              type=list,
              description="The verified_source of tool you want to register in this version. (Optional)", )
    @argument("included_apps",
              type=list,
              description="The included_apps of tool you want to register in this version. (Optional)", )
    @argument("signed",
              type=bool,
              description="This version of tool you want to register is signed or not. Default: False (Optional)", )
    @argument("is_production",
              type=bool,
              description="This version of tool you want to register is production or not. Default: False (Optional)", )
    def version(self, workspace: str, tool_id: str, id: str, descriptor_type: str, images: str,
                version_name: str = "", **kwargs) -> int:
        """
            register trs version object.
        """
        if not workspace:
            cprint("Enter a valid workspace", "red")
            return errno.EIO
        kwargs = {'workspace': workspace}
        id = self._version(tool_id=tool_id, version_name=version_name, version_id=id,
                           descriptor_type=descriptor_type, images=images, **kwargs)
        cprint(f"trs version object - {tool_id}: {id} create complete", "yellow")
        return 0

    @command(aliases=[])
    @argument("tool_id",
              type=str,
              description="The id of tool you have already registered, "
                          "you plan to register the file in. (Required)", )
    @argument("version_id",
              type=str,
              description="The id of version you have already registered, "
                          "you plan to register the file in. (Required)", )
    @argument("descriptor_type",
              type=str,
              description="The descriptor_type of tool have already registered in the following version, "
                          "you plan to register the file in. (Required)",
              choices=["WDL", "CWL", "NFL"])
    @argument("working_dir",
              type=str,
              description="The path of working directory. (Required)")
    @argument("file_info",
              type=str,
              description="Files description used to register trs, default value extracted from workflow section of "
                          "exec.json. (Optional)")
    def file(self, tool_id: str, version_id: str, descriptor_type: str, working_dir: str,
             file_info: str = "default") -> int:
        """
            register trs file object.
        """
        if not file_info:
            cprint(f'Enter a valid file_info.', 'red')
            return errno.EINVAL
        exec_path = f'{working_dir}/exec.json' if file_info == "default" else f'{working_dir}/{file_info}'
        try:
            with open(os.path.abspath(os.path.expanduser(exec_path)), 'r') as file:
                exec = json.loads(file.read())
                file_info = json.dumps(exec['workflows'])
            zip_file = create_zip(target=working_dir, wdl_only=False)
        except FileNotFoundError as err:
            cprint(err, 'red')
            return errno.EINVAL
        except json.JSONDecodeError as err:
            cprint(f'Given a valid exec.json. Workflow content must be a json format.', 'red')
            return errno.EINVAL
        files = self._file(tool_id=tool_id, version_id=version_id, descriptor_type=descriptor_type,
                           file_info=file_info, zip_file=zip_file)
        if isinstance(files, int):
            Path(zip_file).unlink(missing_ok=True)
            return files
        cprint(f"trs file object - {tool_id} : {version_id} : {descriptor_type} create complete", "yellow")
        cprint(f"workflow url - {files} ", "yellow")
        return 0

    @command(aliases=[])
    @argument("workspace",
              type=str,
              description="The workspace according to the sign-in account.")
    def images(self, workspace) -> int:
        """
            List Docker images in the workspace.container_registry
        """
        if not workspace:
            cprint("Enter a valid workspace", "red")
            return errno.EIO
        try:
            resource = trs_resource().load_resource(workspace)
            ret = resource.container_registry(workspace)
            images_info = TrsImagesTemplate().create(ret)
            cprint(f'workspace {workspace} image list:\n----------------------------------------------', 'yellow')
            for img in images_info:
                cprint(json.dumps(img), 'yellow')
            return 0
        except Exception as error:
            cprint(f"{error}", "red")
            return errno.ESRCH

    @command(aliases=[])
    @argument("working_dir",
              type=str,
              description="Absolute working directory path hosting all wdl files, e.g. /home/ubuntu/wdl/. ")
    @argument("inputs",
              type=str,
              description="The relative path of inputs.json compared to working_dir, e.g. inputs.json. ")
    @argument("main_wdl",
              type=str,
              description="The relative path of main wdl compared to working_dir, e.g. main.wdl. ")
    @argument("output",
              type=str,
              description="The relative path of exec.json compared to working_dir. ")
    def execs(self, working_dir: str, inputs: str, main_wdl: str,
              output: str = "working_dir + exec.json") -> int:
        """
            create SeqsLab exec.json
        """
        if not os.path.isdir(working_dir):
            cprint(f"{working_dir} does not exist or is not a directory", "red")
            return errno.ENOENT
        if not os.path.isfile(f"{working_dir}/{inputs}"):
            cprint(f"{inputs} does not exist", "red")
            return errno.ENOENT

        try:
            # zip preparation
            zip_file = create_zip(target=working_dir, wdl_only=True)

            with ZipFile(zip_file, 'r') as z:
                primary_descriptor = [e for e in z.namelist() if e == main_wdl]
                if not primary_descriptor:
                    cprint(f"No match main_wdl name in working_dir.", "red")
                    return errno.ENOENT
                if len(primary_descriptor) != 1:
                    cprint(f"Duplicate main_wdl name in working_dir. {primary_descriptor}", "red")
                    return errno.EBADF
            with open(f"{working_dir}/{inputs}", 'r') as f:
                inputs_content = json.load(f)

            exec_json = TrsCreateTemplate().create(
                zip_file=zip_file,
                primary_descriptor=primary_descriptor[0],
                inputs_json=inputs_content
            )

            if output == "working_dir + exec.json":
                output = f'{working_dir.rstrip("/")}/exec.json'
            else:
                wdl_path = os.path.abspath(working_dir)
                output = os.path.join(wdl_path, output)

            with open(output, 'w') as f:
                json.dump(exec_json, f, indent=4)
            return 0
        except zipfile.BadZipfile as error:
            cprint(f"{error}", "red")
            return errno.EPIPE
        except json.JSONDecodeError as error:
            cprint(f"{error}", "red")
            return errno.EPIPE
        except KeyError as error:
            cprint(f"{error}", "red")
            return errno.ESRCH
        except LookupError as error:
            cprint(f"{error}", "red")
            return errno.ESRCH
        except Exception as exception:
            cprint(f"{exception}", "red")
            return errno.ESRCH
        finally:
            Path(zip_file).unlink(missing_ok=True)

    @command(aliases=[])
    @argument("output",
              type=str,
              positional=False,
              description="The format of the stdout. (Default = json)",
              choices=['json', 'table'])
    def list(self, output='json') -> int:
        """
            list existing tools
        """
        try:
            backend = trs_register().load_resource()
            r = backend.get_tool()
            BaseTools._stdout(r['results'], output)
            return 0
        except Exception as error:
            cprint(f"{error}", "red")
            return errno.ESRCH

    @command(aliases=[])
    @argument("tool_id",
              type=str,
              description="TRS ID. ")
    @argument("version_id",
              type=str,
              description="TRS version. ")
    def delete_version(self, tool_id: str, version_id: str) -> int:
        """
            delete TRS tool version based on tool_id and tool_version_id
        """
        try:
            cprint(tool_id)
            cprint(version_id)
            backend = trs_register().load_resource()
            r = backend.delete_version(tool_id, version_id)
            cprint(r, "yellow")
            return 0
        except Exception as error:
            cprint(f"{error}", "red")
            return errno.ESRCH

    @staticmethod
    def _stdout(results, output: str) -> int:
        from tabulate import tabulate
        """
            stdout:: TODO: support different format ex: json, tsv, table
        """
        if output == "json":
            cprint(json.dumps(results, indent=4))
        elif output == 'table':
            table_header = list(results[0].keys())
            table_datas = [result.values() for result in results]
            cprint(tabulate(
                tabular_data=table_datas,
                headers=table_header,
                tablefmt='pipe'
            ))
        return 0

    @command(aliases=[])
    @argument("tool_id",
              type=str,
              description="TRS ID. ")
    @argument("version_id",
              type=str,
              description="TRS version. ")
    @argument("descriptor_type",
              type=str,
              description="TRS type. ",
              choices=['WDL', 'CWL'])
    @argument("download_path",
              type=str,
              description="The file path of the downloaded tool zip file. ")
    def get(self, tool_id: str, version_id: str, download_path: str, descriptor_type: str = 'WDL') -> int:
        """
            get tool files with SeqsLab API /trs/v2/tools/{id}/versions/{version_id}/{type}/files/
        """
        try:
            backend = trs_register().load_resource()
            backend.get_file(
                tool_id=tool_id,
                version_id=version_id,
                descriptor_type=descriptor_type,
                download_path=download_path
            )
            return 0
        except Exception as error:
            cprint(f"{error}", "red")
            return errno.ESRCH


@command
class Tools(BaseTools):
    """Tools register commands"""

    def __init__(self):
        pass
