# created by Barry at 2022.6.15
from .database import Database
from .globals import logger


def load_odx_cs_file(odx_cs_file_name: str, enable_candela_workarounds=True):
    container = Database(odx_file_name=odx_cs_file_name, enable_candela_workarounds=enable_candela_workarounds)
    logger.info(f"--- --- --- Done with parsing --- --- ---")
    return container

