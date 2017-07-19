from .utils import session_builder

class openstates(object):

    def __init__(self):
        session_builder(self, "OPENSTATES", "https://openstates.org/api/v1/", keyheader='X-API-KEY')(self)

    def legislators_by_state(self, state, options=None):
        return self.request("legislators/", parameters={"state": state})
    # need to implement options

    def bill_search(self, params):
        return self.request("bills/", parameters=params) # e.g. sess.bill_search({"state": "ia", "search_window": "term"})

    def bill_by_id(self, bill_id):
        return self.request("bills/" + bill_id) # e.g. sess.bill_by_id("IAB00009025")

