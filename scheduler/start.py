from sys import stdout
from logging import getLogger
from logging import StreamHandler
from logging import Formatter
from logging import INFO
from logging import WARNING

from . import scheduler

logger = getLogger()


def init_logger():
    logger.setLevel(INFO)
    handler = StreamHandler(stdout)
    handler.setFormatter(fmt=Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(hdlr=handler)
    getLogger('apscheduler.executors.default').setLevel(WARNING)


if __name__ == "__main__":
    init_logger()

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler exited")
