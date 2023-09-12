from .base_service import BaseService
from .sensor_service import SensorService
from .common import Configuration, SensorType


class VehicleService(BaseService):
    def __init__(self, config: Configuration, vehicle_id: int, sensors: list[dict]):
        super().__init__(config, "/fleet/vehicles", is_legacy=False)
        self.vehicle_id = vehicle_id
        self._parse_sensors(sensors)

    def _parse_sensors(self, sensors: list[dict]):
        DOOR_SENSOR = "Door Monitor"
        ENVIRONMENT_SENSOR = "Environment Sensor"

        for sensor in sensors:
            if sensor.get("vehicleId") != self.vehicle_id:
                continue

            if sensor.get("name") == DOOR_SENSOR:
                self.door_sensor = SensorService(
                    self.config, sensor.get("id"), SensorType.DOOR_SENSOR
                )

            if sensor.get("name") == ENVIRONMENT_SENSOR:
                self.temperature_sensor = SensorService(
                    self.config, sensor.get("id"), SensorType.TEMPERATURE_SENSOR
                )
                self.humidity_sensor = SensorService(
                    self.config, sensor.get("id"), SensorType.HUMIDITY_SENSOR
                )

    async def sync_sensors(self, callback):
        sensors_data = {
            "door_data": None,
            "temperature_data": None,
            "humidity_data": None,
        }

        if self.door_sensor is not None:
            sensors_data["door_data"] = self.door_sensor.get_data()

        if self.temperature_sensor is not None:
            sensors_data["temperature_data"] = self.temperature_sensor.get_data()

        if self.humidity_sensor is not None:
            sensors_data["humidity_data"] = self.humidity_sensor.get_data()

        callback(sensors_data)
