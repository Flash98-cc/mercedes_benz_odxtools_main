# created by Barry at 2022/5/31
from ..odx_cs.comparamsubset import ComparamSubset


class Comparam_subset_ref:
    def __init__(self,
                 id_ref,
                 doctype,
                 docref):
        self.id_ref = id_ref
        self.doctype = doctype
        self.docref = docref
        self.comparamsubset = None

    # PROT-STACK 引用了一个COMPARAM-SUBSET元素
    def _resolve_reference(self, id_lookup):
        pass

def read_comparam_subset_ref_from_odx(et_element):
    docref = et_element.get("DOCREF")
    doctype = et_element.get("DOCTYPE")
    id_ref = et_element.get("ID-REF")
    return Comparam_subset_ref(id_ref, doctype, docref)
