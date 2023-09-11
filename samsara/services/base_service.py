import requests

from samsara.services.common import Configuration, SamsaraServiceError


class BaseService:
    def __init__(
        self, config: Configuration, endpoint: str, is_legacy: bool = False
    ) -> None:
        super().__init__()
        self.config = config
        self.endpoint = endpoint
        self.is_legacy = is_legacy
        self.headers = {"Authorization": f"Bearer {self.config.auth}"}

    def _prepare_request(self, method: str, body: dict = {}, params: dict = {}):
        """
        Generic request creation. Takes in consideration if the service uses a legacy endpoint.
        """
        url = f"{self.config.domain}{'/v1' if self.is_legacy else ''}{self.endpoint}"

        return requests.request(
            method, url, params=params, json=body, headers=self.headers
        )

    def _validate_response(self, response: requests.Response):
        """
        Validates response to generic filters and parses response into JSON format
        """
        if response.status_code not in [200, 201]:
            raise SamsaraServiceError(f"Error in Samsara request: {response.text}:")

        if "application/json" not in response.headers.get("Content-Type").lower():
            raise SamsaraServiceError(
                f"Samsara API responded with invalid format: {response.text}"
            )

        return response.json()

    def make_request(self, method: str, body: dict = {}, params: dict = {}):
        """
        Exposed method for chaining all generic private methods of the service.
        """
        return self._validate_response(self._prepare_request(method, body, params))
