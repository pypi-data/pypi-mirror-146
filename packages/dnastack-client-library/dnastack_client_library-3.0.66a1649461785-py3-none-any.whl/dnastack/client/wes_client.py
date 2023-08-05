import mimetypes
import os
from urllib.parse import urljoin

from requests_toolbelt import MultipartEncoder

from .base_client import BaseServiceClient
from ..configuration import ServiceEndpoint
from ..exceptions import ServiceException


class WesClient(BaseServiceClient):
    """
    A client for the Workflow Execution Service (WES) standard
    """

    def __init__(self, endpoint: ServiceEndpoint):
        if not endpoint.url.endswith('/'):
            endpoint.url += '/'
        super(WesClient, self).__init__(endpoint)

    @staticmethod
    def get_adapter_type() -> str:
        return 'wes'

    def info(self) -> dict:
        """
        Get the service info of the Workflow Execution Service (WES) instance

        :return: A dict containing the WES instance metadata
        """
        system_state_counts = None

        if self.auth:
            try:
                list_of_workflows = self.list()

                system_state_counts = {}

                for run in list_of_workflows["runs"]:
                    if system_state_counts.get(run["state"], None) is None:
                        system_state_counts[run["state"]] = 1
                    else:
                        system_state_counts[run["state"]] = (
                            system_state_counts[run["state"]] + 1
                        )
            # if we can't get the list of runs, we continue anyways
            except ServiceException:
                pass

        with self.request_session() as session:
            service_info_res = session.get(self.url + "ga4gh/wes/v1/service-info")

            if service_info_res.ok:
                response = service_info_res.json()

                if system_state_counts is not None:
                    response["system_state_counts"] = system_state_counts

                return response
            else:
                raise ServiceException(
                    url=self.url,
                    msg=f"Unable to get service info for the WES service "
                        f"(the WES service returned {service_info_res.status_code})",
                )

    def execute(
        self,
        workflow_url: str,
        attachment_files: list = None,
        input_params_file: str = None,
        engine_param: str = None,
        engine_params_file: str = None,
        tag: str = None,
        tags_file: str = None,
    ) -> dict:
        """
        Submit a workflow to be executed

        :param workflow_url: The url of the workflow to be executed. This can either be a relative path
        (in which case an attachment with that name must be present),
        or it can be an absolute path to a file on the internet
        :param attachment_files: If workflow_url is a relative path, this is the file to be executed
        :param input_params_file: A path to a JSON file containing all of the inputs of the workflow
        :param engine_param: A single engine parameter of the form "K=V"
        :param engine_params_file: A path to a JSON file containing all of the engine parameters of the workflow
        :param tag: A single tag value of the form "K=V"
        :param tags_file: A path to a JSON file containing all of the engine parameters of the workflow
        :return: A dict containing the response given by the WES instance
        """
        attachment_file_contents = []
        input_params = None
        engine_params_file_contents = None
        tags_file_contents = None

        form_param_fields = [("workflow_type", "WDL"), ("workflow_type_version", "1.0")]

        if input_params_file:
            with open(input_params_file, "r") as file:
                input_params = file.read()
                file.close()

        if engine_params_file:
            with open(engine_params_file, "r") as file:
                engine_params_file_contents = file.read()
                file.close()

        if tags_file:
            with open(tags_file, "r") as file:
                tags_file_contents = file.read()
                file.close()

        url = urljoin(self.url, "ga4gh/wes/v1/runs")

        form_param_fields.append(("workflow_url", workflow_url))

        if input_params:
            form_param_fields.append(
                ("workflow_params", (None, input_params, "application/json"))

            )

        if engine_param:
            form_param_fields.append(
                ("workflow_engine_parameters", engine_param,)
            )

        if engine_params_file_contents:
            form_param_fields.append(
                (
                    "workflow_engine_parameters",
                    (None, engine_params_file_contents, "application/json"),
                )
            )

        if tag:
            form_param_fields.append(
                ("tags", (None, tags_file_contents, "application/json"))
            )

        if tags_file_contents:
            form_param_fields.append(
                ("tags", (None, tags_file_contents, "application/json"))
            )

        for attachment_file in attachment_files:
            form_param_fields.append(
                (
                    "workflow_attachment",
                    (
                        os.path.basename(attachment_file),
                        open(attachment_file, 'rb'),
                        mimetypes.guess_type(os.path.basename(attachment_file))
                    )
                )
            )

        encoder = MultipartEncoder(fields=form_param_fields)
        with self.request_session() as session:
            response = session.post(url, headers={'Content-Type': encoder.content_type}, data=encoder)
            return response.json()

    def list(self, page_size: int = None, next_page_token: str = None) -> dict:
        """
        Get a list of all previously executed workflows, including current state

        :param page_size: Specify how many results to return on a single page (excluding a next page token)
        :param next_page_token: If given, get the results starting after the provided page token
        :return: A dict of the Run ID and current state of all previously run workflows
        """
        url = self.url + "ga4gh/wes/v1/runs"
        params = {}

        if page_size:
            params["page_size"] = page_size

        if next_page_token:
            params["page_token"] = next_page_token

        with self.request_session() as session:
            if not page_size and not next_page_token:
                result = {"runs": []}
                while True:
                    response = session.get(url, params=params)

                    if response.ok:
                        response = response.json()
                    else:
                        raise ServiceException(
                            url=self.url,
                            msg="Unable to get paginated response",
                        )

                    result["runs"].extend(response["runs"])

                    if response.get("next_page_token", None) is not None:
                        params["page_token"] = response["next_page_token"]
                    else:
                        return result
            else:
                runs_res = session.get(url, params=params)

                if not runs_res.ok:
                    raise ServiceException(
                        msg=f"The service return error code [{runs_res.status_code}]",
                        url=self.url,
                    )
                return runs_res.json()

    def get(self, run_id: str, status_only: bool = False) -> dict:
        """
        Get the details of a run including status

        :param run_id: The Run ID of the workflow
        :param status_only: Only return the status of the workflow
        :return: A dict containing run information
        """
        url = urljoin(self.url, f"ga4gh/wes/v1/runs/{run_id}")

        if status_only:
            url = url + "/status"

        with self.request_session() as session:
            return session.get(url).json()

    def cancel(self, run_id: str) -> dict:
        """
        Cancel a running workflow with a specified Run ID
        :param run_id: The Run ID of the workflow
        :return: A dict of the cancelled workflow's Run ID if successful
        """
        with self.request_session() as session:
            return session.post(urljoin(self.url, f"ga4gh/wes/v1/runs/{run_id}/cancel")).json()

    def run_logs(
        self,
        run_id: str = None,
        stdout: bool = False,
        stderr: bool = False,
        url: str = None,
        task: str = None,
        index: int = 0,
    ) -> str:
        """
        Get the logs of a workflow from either stdout or stderr

        :param run_id: The Run ID of the workflow
        :param stdout: Get the logs of stdout
        :param stderr: Get the logs of stderr
        :param url: Get the logs at a specified url. If this is specified, no other parameters are required
        :param task: The name of the task to get logs for. If unspecified, the logs for all tasks will be retrieved
        :param index: The (zero-based) index of the task to get logs for.
        If no index is provided, 0 will be used by default
        :return: The logs of the workflow's task and index as a str
        """
        if not (stdout or stderr or url):
            raise RuntimeError(
                "One of the following options must be used: stderr stdout url"
            )
        elif stdout and not task:
            raise RuntimeError("stdout option requires following argument: task")

        with self.request_session() as session:
            if url:
                return session.get(url).text

            url = urljoin(self.url + f"ga4gh/wes/v1/runs/{run_id}/logs")

            if task:
                url += f"/task/{task}/{index}"

            if stderr:
                url += "/stderr"
            elif stdout:
                url += "/stdout"

            return session.get(url).text
