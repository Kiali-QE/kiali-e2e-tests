import pytest
import json

# Note: Number of services +1 Views Group Node
# Note: Node and Edge counts are based on traffic origainating from the Ingress
BOOKINFO_EXPECTED_NODES=7
BOOKINFO_EXPECTED_EDGES=6


def test_service_graph_rest_endpoint(kiali_json):

    assert kiali_json != None, "Json: {}".format(kiali_json)

    # Validate Node count
    print "Node count: {}".format(len(kiali_json.get('elements').get('nodes')))
    assert len(kiali_json.get('elements').get('nodes')) >= 1

    # Validate edge count
    assert len(kiali_json.get('elements').get('edges')) >= 1

def test_service_graph_bookinfo_namespace_(kiali_json):

    # Validate Node count
    assert len(kiali_json.get('elements').get('nodes')) == BOOKINFO_EXPECTED_NODES
    
    # validate edge count
    edges = kiali_json.get('elements').get('edges')
    assert len(edges) >= BOOKINFO_EXPECTED_EDGES
    #assert json.dumps(edges, ensure_ascii=False, cls=ApiJsonEncoder).count('green') == BOOKINFO_EXPECTED_EDGES
