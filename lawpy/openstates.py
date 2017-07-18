from .utils import session_builder

class openstates(object):

    def __init__(self):
        session_builder(self, "OPENSTATES", "https://openstates.org/api/v1/", keyheader='X-API-KEY')(self)

    def legislators_by_state(self, state, options=None):
        return self.request("legislators/", parameters={"state": state})
