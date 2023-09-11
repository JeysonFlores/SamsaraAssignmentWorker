from samsara.services.base_service import BaseService
from samsara.services.common import Configuration, SensorType, make_samsara_request


sensor_endpoints_dispatcher = {
    SensorType.DOOR_SENSOR: "door",
    SensorType.TEMPERATURE_SENSOR: "temperature",
    SensorType.HUMIDITY_SENSOR: "humidity",
}


class SensorService(BaseService):
    def __init__(self, config: Configuration, sensor_id: int, sensor_type: SensorType):
        super().__init__(
            config,
            f"/sensors/{sensor_endpoints_dispatcher[sensor_type]}",
            is_legacy=True,
        )
        self.sensor_id = sensor_id

    def get_data(self):
        payload = {"sensors": [self.sensor_id]}

        sensor_results = self.make_request("POST", payload).get("sensors")

        if len(sensor_results) < 1:
            return None

        return sensor_results[0]

    @staticmethod
    def get_all(config: Configuration):
        sensors_raw = make_samsara_request(
            config, "/sensors/list", is_legacy=True, method="POST"
        ).get("sensors", [])

        sensor_ids = [sensor.get("id") for sensor in sensors_raw]

        return make_samsara_request(
            config,
            "/sensors/cargo",
            is_legacy=True,
            method="POST",
            body={"sensors": sensor_ids},
        ).get("sensors")
