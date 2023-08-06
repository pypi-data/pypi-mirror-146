import time
from typing import Dict, Any, Generator, List, Union
from clients_core.service_clients import E360ServiceClient
from clients_core.exceptions import ClientValueError  # noqa: F401
from pydantic import parse_obj_as

from analytic_workbench_clients.methods_client import MethodsClient
from .models import JobCreateModel, JobModel, JobResultPath, State, TaskStatusModel
from jsonschema import validate


CHUNK_SIZE = 1024 * 1024  # 1MB


class AWJobsClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """
    service_endpoint = ""
    extra_headers = {"accept": "application/json"}

    def create(self, payload: Dict[str, Any], user_id: str, for_model: Dict[str, Any] = None, **kwargs: Any) -> JobModel:
        """
        Create a new AW job.

        Args:
            payload: job submission payload, as dict
            user_id: user_id, as str
            for_model: optional dict for the creation model
        Raises:
            pydantic.ValidationError: when the model creation fails validation

        """
        model = JobCreateModel(userId=user_id, payload=payload, **(for_model or {}))
        response = self.client.post('', json=model.dict(), raises=True, **kwargs)
        return JobModel.parse_obj(response.json())

    def get_by_id(self, job_id: str, **kwargs: Any) -> JobModel:
        url = f'{job_id}/'
        response = self.client.get(url, raises=True, **kwargs)
        return JobModel.parse_obj(response.json())

    def submit_job_by_id(self, job_id: str, **kwargs: Any) -> bool:
        url = f'{job_id}/submit/'
        response = self.client.post(url, raises=True, **kwargs)
        return response.ok

    def job_task_status_by_id(self, job_id: str, **kwargs: Any) -> TaskStatusModel:
        url = f'{job_id}/task/'
        response = self.client.get(url, raises=True, **kwargs)
        return TaskStatusModel.parse_obj(response.json())

    def job_get_results_by_id(self, job_id: str, **kwargs: Any) -> List[JobResultPath]:
        url = f'{job_id}/results/'
        response = self.client.get(url, raises=True, **kwargs)
        return parse_obj_as(List[JobResultPath], response.json())

    def job_get_binary_results_by_name(self, job_id: str, name: str, **kwargs: Any) -> Generator[bytes, None, None]:
        url = f'{job_id}/results/{name}'
        response = self.client.get(url, raises=True, stream=True, **kwargs)
        return response.iter_content(chunk_size=CHUNK_SIZE)

    def submit_method_payload(self, method_id: str, payload: Dict[str, Any], user_id: str, sleep_time: float, max_retries: int, **kwargs: Any) -> Union[List[JobResultPath], None]:
        """
        Validates method payload against method schema and submits it as a job. Waits for method completion then returns job results.
        """
        methods_client = MethodsClient(client=self.client, user_id=user_id)
        method_schema = methods_client.get_method_schema(method_id)
        validate(instance=payload, schema=method_schema)
        job = self.create(payload, user_id, **kwargs)
        if job.id:
            self.submit_job_by_id(job.id)
            self._wait_for_method(job.id, sleep_time, max_retries)
            return self.job_get_results_by_id(job.id)
        return None

    def _wait_for_method(self, job_id: str, sleep_time: float, max_retries: int) -> None:
        """
        Poll Job Status GET endpoint until status is complete
        """
        for _ in range(max_retries):
            state = self.job_task_status_by_id(job_id).state
            if state in (State.SUCCESS, State.FAILED):
                return
            time.sleep(sleep_time)

        raise TimeoutError("Polling limit reached before method completion")
