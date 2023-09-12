import json

from worker.common.util_functions import create_connection_to_redis


redis_connection = create_connection_to_redis()


def get_value_from_redis(redis_key, to_dict=True):
    """
    Retrieves a value from the module-scoped redis connection.
    """
    try:
        value = redis_connection.get(redis_key)
        if to_dict and value:
            value = json.loads(value)
    except Exception as _:
        value = None

    return value


def set_value_into_redis(redis_key, payload, ttl=None):
    redis_connection.set(redis_key, json.dumps(payload))
    if ttl is not None and type(ttl) is int:
        redis_connection.expire(redis_key, ttl)


def publish_value_to_redis_topic(topic, payload):
    redis_connection.publish(topic, json.dumps(payload))
