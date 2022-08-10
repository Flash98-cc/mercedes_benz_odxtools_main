# created by Barry at 2022.06.22
from enum import Enum
from dataclasses import dataclass


class DATAFORMAT_SELECTION(Enum):
    INTEL_HEX = "INTEL-HEX"
    MOTOROLA_S = "MOTOROLA-S"
    BINARY = "BINARY"
    # USER-DEFINED is used for non-normative extensions
    USER_DEFINED = "USER-DEFINED"


# DATAFORMAT specifies the format in which data is represented in the current data or the referenced file
@dataclass()
class DataFormat:

    def __init__(self,
                 selected: str,
                 user_selection: str):
        self.selected = selected
        assert self.selected in ['INTEL-HEX', 'MOTOROLA-S', 'BINARY', 'USER-DEFINED'], \
            "selected must be one of 'INTEL-HEX', 'MOTOROLA-S', 'BINARY', 'USER-DEFINED'"
        self.user_selection = user_selection


def read_dataformat_from_flashdata(et_element):
    if et_element is None:
        return None

    selected = et_element.get("SELECTION")
    user_selection = et_element.text
    return DataFormat(selected, user_selection)
