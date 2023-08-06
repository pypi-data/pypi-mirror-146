from ehelply_logger.Logger import Logger

from ehelply_batcher.abstract_timer_service import AbstractTimerService


class SimulatedTimerService(AbstractTimerService):
    def __init__(self, name: str = "", delay_seconds: int = 2, logger: Logger = None):
        super().__init__(name, delay_seconds, logger)

    def proc(self):
        print("PROC'd")
