from worker import Worker
from worker.services.exporters.redis_exporter import RedisExporter


if __name__ == "__main__":
    exporter = RedisExporter()

    app_worker = Worker(exporter)
    app_worker.start()
