# created by Barry at 2022.06.24

from .database import Database
from .globals import logger


def load_odx_f_file(odx_f_file_name: str, enable_candela_workarounds=False):
    container = Database(odx_file_name=odx_f_file_name,
                         enable_candela_workarounds=enable_candela_workarounds)
    logger.info(f"---------- Done with Parsing-------------")
    return container
