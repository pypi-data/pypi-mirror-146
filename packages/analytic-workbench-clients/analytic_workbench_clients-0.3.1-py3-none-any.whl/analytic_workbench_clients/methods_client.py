from typing import Any
from clients_core.service_clients import E360ServiceClient


class MethodsClient(E360ServiceClient):

    service_endpoint = ""

    def get_method_schema(self, method_id: str, **kwargs: Any) -> str:
        """
        Returns method schema json
        """
        url = f'{method_id}/schema'
        response = self.client.get(url, raises=True, **kwargs)
        return response.json()
