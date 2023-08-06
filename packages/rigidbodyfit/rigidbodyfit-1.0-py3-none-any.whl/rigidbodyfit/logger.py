import logging

import rich.logging


def create_rich_logger(level="INFO"):
    FORMAT = "%(message)s"
    logging.basicConfig(level=level,
                        format=FORMAT,
                        datefmt="[%X]",
                        handlers=[rich.logging.RichHandler()])
    return logging.getLogger("rich")
