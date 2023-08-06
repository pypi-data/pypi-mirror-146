import errno
import json
import logging
import os
import zipfile
from functools import lru_cache

import requests
from nubia import argument
from nubia import command
from nubia import context
from requests_toolbelt.multipart.encoder import MultipartEncoder
from seqslab.auth.commands import BaseAuth
from seqslab.wes import __version__, API_HOSTNAME
from tenacity import retry, wait_fixed, stop_after_attempt
from termcolor import cprint

from seqslab.trs.register.base import TRSregister
from .internal.common import get_factory
from .template.base import WorkflowParamsTemplate, WorkflowBackendParamsTemplate, WorkflowBackendParamsClusterTemplate
from seqslab.runsheet.runsheet import RunSheet, Run

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


@command
class Jobs:
    """Workflow execution commands"""
    WES_PARAMETERS_URL = f"https://{API_HOSTNAME}/wes/{__version__}/schedules/parameters/"
    OPERATOR_PIPELINE_URL = f"https://{API_HOSTNAME}/wes/{__version__}/operator-pipelines/{{pipeline_id}}/"

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    @lru_cache(maxsize=16)
    def parameter(primary_descriptor: str, zip_file: str):
        token = BaseAuth.get_token().get('tokens').get('access')
        files = {'file': (f"{os.path.basename(zip_file)}",
                          open(zip_file, 'rb'),
                          'application/zip'),
                 "PRIMARY_DESCRIPTOR": ("", primary_descriptor)}
        with requests.patch(url=Jobs.WES_PARAMETERS_URL,
                            files=files,
                            headers={"Authorization": f"Bearer {token}"}) as response:
            if response.status_code not in [requests.codes.ok]:
                raise requests.HTTPError(response.text)
            return json.loads(response.content)

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    @lru_cache(maxsize=16)
    def get_operator_pipeline(pipeline_id: str):
        token = BaseAuth.get_token().get('tokens').get('access')
        with requests.patch(url=Jobs.OPERATOR_PIPELINE_URL.format(pipeline_id=pipeline_id),
                            headers={"Authorization": f"Bearer {token}"}) as response:
            if response.status_code not in [requests.codes.ok]:
                raise requests.HTTPError()
            return json.loads(response.content)

    def __init__(self,
                 workspace: str = None,
                 multiprocessing: int = 1,
                 concurrency: int = 0):
        self._workspace = workspace
        self._multiprocessing = multiprocessing
        self._concurrency = concurrency

    @property
    def proxy(self) -> str:
        """web proxy server"""
        return context.get_context().args.proxy

    @property
    def workspace(self) -> str:
        return self._workspace

    @property
    def multiprocessing(self) -> int:
        return self._multiprocessing

    @property
    def concurrency(self) -> int:
        """Maximum number of parallel connections to use in copying a single file"""
        return self._concurrency

    @argument("exec_json",
              type=str,
              description="Absolute file path of exec.json. ")
    @argument("runtimes",
              type=str,
              description="key:value pairs indicating workflow name -> SeqsLab supported runtime_options names. "
                          "Multiple configuration pairs can be provided with '#' as separator, "
                          "e.g. main=acu-m8:subworkflow=acu-m4"
                          "(Default = None, indicating running the whole workflow.wdl using acu-m8 for "
                          "single node cluster on Azure backend) ")
    def _workflow_backend_params(self,
                                 exec_json: str,
                                 runtimes: str = None
                                 ) -> dict:
        """
        create workflow_backend_params.json
        """
        if not os.path.isfile(exec_json):
            cprint(f"{exec_json} does not exist", "red")
            return errno.ENOENT
        try:
            with open(exec_json, 'r') as f:
                execs = json.loads(f.read())
                workflow = execs.get('workflows')
                primary_obj = [item for item in workflow if item.get('file_type') == 'PRIMARY_DESCRIPTOR'][0]
                primary_workflow_name = primary_obj.get('workflow_name') if primary_obj.get(
                    'workflow_name') else primary_obj.get('name').replace('.wdl', '')
                call_names_list = execs.get('calls', None)
                # use sub-workflow names if no call section given
                if not call_names_list:
                    calls = [item.get('name').replace('.wdl', '') for item in workflow
                             if item.get('file_type') == 'SECONDARY_DESCRIPTOR'] + [primary_workflow_name]
                else:
                    calls = call_names_list
        except json.JSONDecodeError as error:
            cprint(f"{error}", "red")
            return errno.EPIPE

        rt_dict = {}
        if not runtimes:
            rt_dict = {primary_workflow_name: 'acu-m8'}
        else:
            rtcs = runtimes.split(':')
            for rtc in rtcs:
                c = rtc.split('=')
                rt_dict[c[0]] = c[1]

        resource = get_factory().load_resource(self.workspace)
        clusters = []
        for k, v in rt_dict.items():
            if k not in calls:
                raise RuntimeError(f'given call name {k} not in TRS registered call name list {calls}!')
            clusters.append(WorkflowBackendParamsClusterTemplate(run_time=resource.get_runtime_setting(v),
                                                                 workflow_name=k))

        bk_template = WorkflowBackendParamsTemplate(
            clusters=clusters,
            workspace=self.workspace
        )
        return bk_template

    @command(aliases=[])
    @argument("working_dir",
              type=str,
              positional=False,
              description="working directory path containing request.json"
              )
    @argument("response_path",
              type=str,
              positional=False,
              description="The relative path of response.json compared to working_dir"
              )
    def run(self,
            working_dir: str,
            response_path: str = 'response.json'
            ) -> int:
        """
        run workflow by calling seqslab-api/wes/runs api
        """
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Invalid workspace name", "red")
            return errno.EINVAL

        if not os.path.isdir(working_dir):
            logging.error("working dir is not a directory")
            cprint("working dir is not a directory", "red")
            return errno.EINVAL

        reqs = [os.path.join(working_dir, f) for f in os.listdir(working_dir) if
                os.path.isfile(os.path.join(working_dir, f)) and f.endswith('request.json')]

        run_list = []
        for op in reqs:
            try:
                with open(op, 'r') as f:
                    request = json.load(f)
            except json.decoder.JSONDecodeError as e:
                cprint(f"given request not in json format - {e}", "red")

            mp = MultipartEncoder(
                fields={
                    "name": request.get('name'),
                    "workflow_type": request.get('workflow_type'),
                    "workflow_type_version": request.get('workflow_type_version'),
                    "workflow_url": request.get('workflow_url'),
                    'workflow_params': json.dumps(request.get('workflow_params')),
                    'workflow_backend_params': json.dumps(request.get('workflow_backend_params'))
                }
            )
            resource = get_factory().load_resource(self.workspace)
            ret = resource.sync_run_jobs(data=mp,
                                         headers={'Content-Type': mp.content_type},
                                         run_request_id=None,
                                         run_name=request.get('name'))
            res = json.loads(ret.content.decode('utf-8'))
            res['run_name'] = request.get('name')
            run_list.append(res)
            cprint(f"{res}", "yellow")
        with open(os.path.join(working_dir, response_path), 'w') as f:
            json.dump(run_list, f, indent=4)
        return 0

    @command(aliases=["schedule"])
    @argument("run_request_id",
              type=str,
              positional=False,
              description="previously scheduled run_request_id. "
              )
    @argument("schedule_tag",
              type=str,
              positional=False,
              description="a tag marked on previously uploaded samples for schedule job. "
              )
    def run_schedule(self,
                     run_request_id: str,
                     schedule_tag: str
                     ) -> int:
        """
        run job based on a previously registered run_request.  Typically the run_request is designed for schedule job,
        where the FQN-DRS connection of sequencing samples are left blank for future run-time sample-resolving.
        Thus, by specifying sample-resolving rule, the run_request can be used to serve schedule job use case
        """
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Invalid workspace name", "red")
            return errno.EINVAL

        mp = MultipartEncoder(fields={})
        resource = get_factory().load_resource(self.workspace)
        ret = resource.sync_run_jobs(data=mp,
                                     headers={'Content-Type': mp.content_type},
                                     run_request_id=run_request_id,
                                     run_name=schedule_tag)
        cprint(f"{ret.content.decode('utf-8')}", "yellow")
        return 0

    @command(aliases=["state"])
    @argument("run_id",
              type=str,
              positional=False,
              description="previously executed WES run_id"
              )
    def run_state(self, run_id: str) -> int:
        """
        get WES run information based on run_id
        """
        result = get_factory().load_resource(self.workspace).get_run_status(run_id)
        cprint(json.dumps(result), "yellow")

        return 0

    @argument("exec_json",
              type=str,
              description="The file path of exec.json. ")
    def _workflow_params(self, exec_json: str) -> dict:
        """
            create workflow_params.json
        """
        # TODO: write DRS id to workflow_params based run_sheet content
        if not os.path.isfile(exec_json):
            cprint(f"{exec_json} does not exist", "red")
            return errno.ENOENT

        try:
            with open(exec_json, 'r') as f:
                t_content = json.loads(f.read())

            params = WorkflowParamsTemplate().create(
                ex_template=t_content,
                api_hostname=API_HOSTNAME
            )
            return params
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

    @command(aliases=["runsheet"])
    @argument("working_dir",
              type=str,
              description="Absolute output directory for generated jobs params. ",
              aliases=["o"])
    @argument("run_sheet",
              type=str,
              description="Absolute output path for run_sheet. ",
              aliases=["r"])
    @argument("execs",
              type=str,
              description="execs.json needed for create WES request.  If not given, the command will get the "
                          "execs.json from the TRS object specified by the workflow_url.  If given, the given "
                          "execs.json will be used to create all the WES run requests specified in the run_sheet ("
                          "Default = None)")
    def request_runsheet(self,
                         working_dir: str,
                         run_sheet: str,
                         execs: str = None
                         ):
        """
        parse run_sheet.csv and create jobs execution request.json for each job runs.
        """
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Invalid workspace name", "red")
            return errno.EINVAL
        if not os.path.isdir(working_dir):
            logging.error("working dir is not a directory")
            cprint("working dir is not a directory", "red")
            return errno.EINVAL
        run_sheet = RunSheet(run_sheet)
        for run in run_sheet.runs:
            self._runs_routine(run=run, working_dir=working_dir, execs=execs)
        return 0

    def _runs_routine(self, run: Run, working_dir: str, execs: str = None):
        exec_path = f'{working_dir}/{run.run_name}-exec.json'
        request_path = f'{working_dir}/{run.run_name}-request.json'
        wf_info = run.workflow_url.split('versions')[1].strip('/').split('/')

        if not execs:
            TRSregister.get_exec_json(
                workflow_url=run.workflow_url,
                download_path=exec_path
            )
        else:
            exec_path = f'{working_dir}/{execs}'

        params = self._workflow_params(exec_path)
        if not isinstance(params, dict):
            raise Exception(f'Unable to generate workflow_params based on given exec_path, with error code {params}')

        request = {
            "name": run.run_name,
            'workflow_params': params,
            'workflow_backend_params': self._workflow_backend_params(exec_path, run.runtimes),
            'workflow_url': run.workflow_url,
            "workflow_type_version": wf_info[0],
            'workflow_type': wf_info[1],
        }
        with open(request_path, 'w') as f:
            json.dump(request, f, indent=4)

    @command(aliases=[])
    @argument("run_name",
              type=str,
              description="Defined Run Name for this single run. ",
              aliases=["name"])
    @argument("working_dir",
              type=str,
              description="Working Directory includes exec.json. ",
              aliases=["dir"])
    @argument("workflow_url",
              type=str,
              description="TRS url used for this single run. ",
              aliases=["url"])
    @argument("execs",
              type=str,
              description="execs.json needed for create WES request.  If not given, the command will get the "
                          "execs.json from the TRS object specified by the workflow_url (Default = None)")
    def request(self, run_name: str, working_dir: str, workflow_url: str, execs=None):
        """
        create WES run request
        """
        if not self.workspace:
            logging.error("Invalid workspace name")
            cprint("Invalid workspace name", "red")
            return errno.EINVAL
        if not os.path.isdir(working_dir):
            logging.error("working dir is not a directory")
            cprint("working dir is not a directory", "red")
            return errno.EINVAL
        single_run = Run(list(), run_name, workflow_url, None)
        self._runs_routine(run=single_run, working_dir=working_dir, execs=execs)
        return 0

    @command(aliases=["get-run"])
    @argument("run_id",
              type=str,
              positional=False,
              description="previously executed WES run_id"
              )
    def get(self, run_id: str) -> int:
        """
        get WES run information based on run_id
        """
        result = get_factory().load_resource(self.workspace).get_run_id(run_id)
        cprint(json.dumps(result, indent=4), "yellow")

        return 0
