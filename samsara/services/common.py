import requests
from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class Configuration:
    domain: str
    auth: str


class SamsaraServiceError(Exception):
    pass


class SensorType(Enum):
    DOOR_SENSOR = auto()
    TEMPERATURE_SENSOR = auto()
    HUMIDITY_SENSOR = auto()


def make_samsara_request(
    config: Configuration,
    endpoint: str,
    is_legacy: bool = False,
    method: str = "GET",
    body: dict = {},
    params: dict = {},
):
    """
    Generic (functional) request creation for a Samsara endpoint.
    """
    headers = {"Authorization": f"Bearer {config.auth}"}

    url = f"{config.domain}{'/v1' if is_legacy else ''}{endpoint}"

    response = requests.request(method, url, params=params, json=body, headers=headers)

    if response.status_code not in [200, 201]:
        raise SamsaraServiceError(f"Error in Samsara request: {response.text}:")

    if "application/json" not in response.headers.get("Content-Type").lower():
        raise SamsaraServiceError(
            f"Samsara API responded with invalid format: {response.text}"
        )

    return response.json()
