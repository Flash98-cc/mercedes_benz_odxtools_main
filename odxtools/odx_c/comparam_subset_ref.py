# created by Barry at 2022/5/31

class Comparam_subset_ref:
    def __init__(self,
                 id_ref,
                 doctype,
                 docref):
        self.id_ref = id_ref
        self.doctype = doctype
        self.docref = docref


def read_comparam_subset_ref_from_odx(et_element):
    docref = et_element.get("DOCREF")
    doctype = et_element.get("DOCTYPE")
    id_ref = et_element.get("ID-REF")
    return Comparam_subset_ref(id_ref, doctype, docref)
