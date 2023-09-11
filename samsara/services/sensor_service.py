from samsara.services.common import SensorType
from samsara.services.base_service import BaseService


sensor_endpoints_dispatcher = {
    SensorType.DOOR_SENSOR: "door",
    SensorType.TEMPERATURE_SENSOR: "temperature",
    SensorType.HUMIDITY_SENSOR: "humidity",
}


class SensorService(BaseService):
    def __init__(self, auth_token: str, sensor_id: int, sensor_type: SensorType):
        super().__init__(
            f"/sensors/{sensor_endpoints_dispatcher[sensor_type]}",
            auth_token,
            is_legacy=True,
        )
        self.sensor_id = sensor_id

    def get_data(self):
        payload = {"sensors": [self.sensor_id]}

        sensor_results = self.make_request("POST", payload).get("sensors")

        if len(sensor_results) < 1:
            return None

        return sensor_results[0]
