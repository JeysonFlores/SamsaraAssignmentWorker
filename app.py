import sys
import logging

from dotenv import load_dotenv

from worker import Worker
from worker.services.exporters.redis_exporter import RedisExporter


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    load_dotenv()

    exporter = RedisExporter()

    app_worker = Worker(exporter)
    app_worker.start()
