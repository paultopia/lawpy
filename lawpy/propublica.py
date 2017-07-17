from .utils import session_builder, request_builder

class propublica(object):

    def __init__(self):
        session_builder(self, "PROPUBLICA")(self)

    def request(self, endpoint="", headers={}, parameters=None):
        return request_builder(self, "https://api.propublica.org/congress/v1/")(self, endpoint, headers, parameters)

    def bill_info_by_stub(self, congress, bill):
        ep = str(congress) + "/bills/" + bill + ".json"
        return self.request(endpoint=ep)
