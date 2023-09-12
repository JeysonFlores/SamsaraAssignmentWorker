from dateutil.parser import parse

from worker.common.common_functions import (
    set_value_into_redis,
    get_value_from_redis,
    publish_value_to_redis_topic,
)

from .base_exporter import BaseExporter


class RedisExporter(BaseExporter):
    def is_newer(self, topic, message):
        newest_message_raw = get_value_from_redis(topic)

        if newest_message_raw is None:
            return True

        if message is None:
            return False

        newest_message_timestamp = parse(newest_message_raw).replace(tzinfo=None)
        message_timestamp = parse(message.get("timestamp")).replace(tzinfo=None)

        return message_timestamp > newest_message_timestamp

    def export(self, data):
        vehicle_id = data.get("id_vehicle")

        for key, value in data.get("sensors_data").items():
            event_key = f"vehicle/{vehicle_id}/{key}"

            if not self.is_newer(event_key, value):
                continue

            publish_value_to_redis_topic(event_key, value)
            set_value_into_redis(event_key, value.get("timestamp"))
