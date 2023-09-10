from enum import Enum, auto


class SamsaraServiceError(Exception):
    pass


class SensorType(Enum):
    DOOR_SENSOR = auto()
    TEMPERATURE_SENSOR = auto()
    HUMIDITY_SENSOR = auto()
