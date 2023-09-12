import os
import asyncio

from samsara.services.common import Configuration
from samsara.services.sensor_service import SensorService
from samsara.services.vehicle_service import VehicleService

from worker.common.util_functions import get_logger
from worker.common.common_functions import get_value_from_redis

from worker.services.exporters.base_exporter import BaseExporter


logger = get_logger()


class Worker:
    def __init__(self, exporter: BaseExporter) -> None:
        self.exporter = exporter
        self.config = Configuration(
            os.environ.get("SAMSARA_ENDPOINT"), os.environ.get("SAMSARA_AUTH_TOKEN")
        )
        self.input_key = os.environ.get("WORKER_INPUT")
        self.refresh_rate = int(os.environ.get("WORKER_REFRESH_RATE", 5))
        self.loop = asyncio.get_event_loop()
        self.vehicles = []

    def _process_input(self):
        input = get_value_from_redis(self.input_key)

        vehicle_ids = input.get("vehicles")

        sensors = SensorService.get_all(self.config)

        for vehicle_id in vehicle_ids:
            self.vehicles.append(VehicleService(self.config, vehicle_id, sensors))

    async def _synchronize_services(self):
        self._process_input()
        sync_pool = [svc.sync_sensors(self.exporter.export) for svc in self.vehicles]
        await asyncio.gather(*sync_pool)

    async def _inner_loop(self):
        while True:
            await self._synchronize_services()
            await asyncio.sleep(self.refresh_rate)

    def start(self):
        main_task = self.loop.create_task(self._inner_loop())
        self.loop.run_until_complete(main_task)


if __name__ == "__main__":
    app_worker = Worker()
    app_worker.start()
