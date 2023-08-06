import sys
import logging


class Log:

    def __init__(self) -> None:
        log_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(funcName)s] [%(lineno)d] [%(message)s]",
            "%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger('bn2vec')
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)


logger = Log()
