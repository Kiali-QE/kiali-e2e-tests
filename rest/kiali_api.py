import requests
from rest.rest_client import rest

class kiali_api():
    rest_url = None

    def __init__(self, url=None, endpoint=None, namespace=None):

        assert url, "URL Required."
        assert endpoint, "API Entrypoint Required"
        assert namespace, "Namespace Required"

        self.rest_url = '{}/{}'.format(url, endpoint).format(namespace)

    def get_service_graph_json(self):
        response = rest(url=self.rest_url).get_json()
        return response

    def get_kiali_service_graph_json(self, debug=False):
        response = self.get_service_graph_json()

        if debug:
            assert response.json, "JSON: {}".format(response.json)

            print "\n\nKiali Service Graph Node List:"
            for n in response.json.get('elements').get('nodes'):
                print n.get('data')

            print "\n\nKiali Service Graph Edge List:"
            for n in response.json.get('elements').get('edges'):
                print n.get('data')

        return response
