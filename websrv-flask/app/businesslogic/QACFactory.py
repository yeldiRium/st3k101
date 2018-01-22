from model.query_access_control.AGBQAC import AGBQAC
from model.query_access_control.QACModule import QACModule


def create_qac_module(name: str) -> QACModule:
    if name == "AGBQAC":
        return AGBQAC()
    return None
