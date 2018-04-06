import pytest
import json
from rest.kiali_api import kiali_api

# Note: Number of services +1 Views Group Node
BOOKINFO_EXPECTED_NODES=8
BOOKINFO_EXPECTED_EDGES=7

def test_service_graph_rest_endpoint(config):

    kiali = kiali_api(url=config.get('kiali_url'),
                      endpoint=config.get('kiali_service_graph_json_endpoint'),
                      namespace=config.get('kiali_namespace'))

    response = kiali.get_kiali_service_graph_json(debug=True)

    validate_response(response)

    # validate node count
    nodes = json.dumps(response.json.get('elements'))
    assert json.dumps(nodes, ensure_ascii=False).count('nodes') >= 1

    # validate edge count
    nodes = json.dumps(response.json.get('elements'))
    assert json.dumps(nodes, ensure_ascii=False).count('edges') >= 1


def test_service_graph_bookinfo_namespace(config):
    kiali = kiali_api(url=config.get('kiali_url'),
                      endpoint=config.get('kiali_service_graph_json_endpoint'),
                      namespace=config.get('mesh_bookinfo_namespace'))

    response = kiali.get_kiali_service_graph_json(debug=True)

    validate_response(response)

    # validate node count
    nodes = json.dumps(response.json.get('elements').get('nodes'))
    assert json.dumps(nodes, ensure_ascii=False).count('data') == BOOKINFO_EXPECTED_NODES

    # validate edge count
    edges = json.dumps(response.json.get('elements').get('edges'))
    assert json.dumps(edges, ensure_ascii=False).count('data') == BOOKINFO_EXPECTED_EDGES
    assert json.dumps(edges, ensure_ascii=False).count('green') == BOOKINFO_EXPECTED_EDGES

def validate_response(response):
    assert response.status == 200, "Status: {}".format(response.status)
    assert response.json != None, "Json: {}".format(response.json)