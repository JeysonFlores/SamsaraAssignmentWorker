import os
import redis
import logging


logger = logging.getLogger("worker")
logger.setLevel(logging.INFO)


def create_connection_to_redis():
    """
    Creates a connection to a Redis database.
    """
    host = os.environ.get("REDIS_HOST")
    port = int(os.environ.get("REDIS_PORT"))
    username = os.environ.get("REDIS_USERNAME")
    password = os.environ.get("REDIS_PASSWORD")
    return redis.Redis(
        host=host,
        port=port,
        username=username,
        password=password,
        decode_responses=True,
    )


def get_logger():
    return logger
