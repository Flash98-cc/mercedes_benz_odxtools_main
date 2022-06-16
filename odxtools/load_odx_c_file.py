# created by Barry at 2022.6.1

from .database import Database
from .globals import logger


def load_odx_c_file(odx_c_file_name: str, enable_candela_workarounds: bool = True):
    container = Database(odx_file_name=odx_c_file_name,
                         enable_candela_workarounds=enable_candela_workarounds)
    logger.info(f"--- --- --- Done with parsing --- --- ---")
    return container
