from dateutil.parser import parse

from worker.common.common_functions import (
    set_value_into_redis,
    get_value_from_redis,
    publish_value_to_redis_topic,
)

from worker.common.util_functions import get_logger

from .base_exporter import BaseExporter


logger = get_logger()


class RedisExporter(BaseExporter):
    def is_newer(self, topic, message):
        """
        Compares if a message is newer than the last message published.
        """
        newest_message_raw = get_value_from_redis(topic)

        if newest_message_raw is None:
            return True

        if message is None:
            return False

        newest_message_timestamp = parse(newest_message_raw).replace(tzinfo=None)
        message_timestamp = parse(message.get("timestamp")).replace(tzinfo=None)

        return message_timestamp > newest_message_timestamp

    def export(self, data):
        """
        Validates a sensor event message and publish it through redis pub/sub.
        """
        vehicle_id = data.get("id_vehicle")

        for key, value in data.get("sensors_data").items():
            event_key = f"vehicle/{vehicle_id}/{key}"

            if not self.is_newer(event_key, value):
                continue

            logger.info(f"Message to export {value}")

            publish_value_to_redis_topic(event_key, value)
            set_value_into_redis(event_key, value.get("timestamp"))
