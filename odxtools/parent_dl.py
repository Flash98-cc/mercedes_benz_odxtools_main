# created by Barry at 2022.6.29

# create a class which has some dict element, in order to resolve snref references
from dataclasses import dataclass
from typing import Dict, Any


@dataclass()
class Parent_Dl:
    def __init__(self):
        self.protocols: Dict[str, Any] = {}
        self.prot_stacks: Dict[str, Any] = {}
        self.data_object_properties: Dict[str, Any] = {}
        self.diag_comms: Dict[str, Any] = {}



