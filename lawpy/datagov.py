from .utils import session_builder

class datagov(object):

    def __init__(self):
        session_builder(self, "DATAGOV", "https://api.data.gov/regulations/v3/", 'API_Key', apikey_in_params=True)(self)

    def search_docs(self, searchmap):
        ep = "documents"
        return self.request(endpoint=ep, parameters = searchmap)
    # example: sess.search_docs({"comment": "abortion"})
    # searchable fields: https://regulationsgov.github.io/developers/fields/
