import requests
from collections import namedtuple

class rest():
    rest_url = None
    response = namedtuple('response', ['status', 'json'])

    def __init__(self, url=None):
        assert url, "URL Required."
        self.rest_url = url
        print "rest_url: {}".format(self.rest_url)

    def get_json(self):
        r = self.get()

        self.response.status = r.status_code
        self.response.json = r.json() if r.status_code == 200 else None

        return self.response

    def get(self, params=None, headers=None, auth=None, timeout=60):
        assert self.rest_url
        return  requests.get(self.rest_url, params=params, headers=headers, auth=auth, timeout=timeout)
