from ehelply_logger.Logger import Logger
import time
import asyncio


class AbstractTimerService:
    """
    A timed send/receive class without any batching
    """

    def __init__(self, name: str = "", delay_seconds: int = 2, logger: Logger = None):
        self.logger = logger.spinoff(name) if logger else Logger()

        self.name: str = str(name)

        self.delay_seconds: int = delay_seconds

        self.logger.info("Starting " + self.name + " service")
        self.logger.info("  * Delay: " + str(self.delay_seconds) + "s")

        self.logger.debug("Delegating control of this thread to " + self.name + " Service.")
        self.logger.debuggg("This thread will now be 'locked' by the " + self.name + " service.")
        self.logger.debuggg("  * If this is unintended, please start the " + self.name + " Service is a new thread.")

    async def run(self):
        await self._service()

    async def _service(self):
        while True:
            self.logger.debugg("Proc'd")
            await self.proc()
            await asyncio.sleep(self.delay_seconds)

    async def proc(self):
        pass
