import pytest
from collections import namedtuple

PARAMS = {'duration': '1m'}

test_mesh = namedtuple('test_mesh', ['namespace', 'nodes', 'edges'])
test_box             = test_mesh('kiali-test-box', 5, 7)
test_breadth_sink    = test_mesh('kiali-test-breath-sink', 7, 10)
test_breath          = test_mesh('kiali-test-breath', 7, 6)
test_circle          = test_mesh('kiali-test-circle', 7, 7)
test_circle_callback = test_mesh('kiali-test-circle-callback', 7, 13)
test_depth_sink      = test_mesh('kiali-test-depth-sink', 7, 10)
test_hourglass       = test_mesh('kiali-test-hourglass', 6, 7)


def test_kiali_test_box(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_box.namespace, params=PARAMS).to_json_object(),
                    test_box)

def test_kiali_test_breadth_sink(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_breadth_sink.namespace, params=PARAMS).to_json_object(),
                    test_breadth_sink)

def test_kiali_test_breath(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_breath.namespace, params=PARAMS).to_json_object(),
                    test_breath)

def test_kiali_test_circle(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_circle.namespace, params=PARAMS).to_json_object(),
                    test_circle)

def test_kiali_test_circle_callback(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_circle_callback.namespace, params=PARAMS).to_json_object(),
                    test_circle_callback)

def test_kiali_test_depth_sink(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_depth_sink.namespace, params=PARAMS).to_json_object(),
                    test_depth_sink)

def test_kiali_test_hourglass(kiali_client):
    validate_counts(kiali_client.graph_namespace(namespace=test_hourglass.namespace, params=PARAMS).to_json_object(),
                    test_hourglass)

def validate_counts(json, mesh):
    assert json != None, "Json: {}".format(json)

    if len(json.get('elements').get('nodes')) == 0 and len(json.get('elements').get('edges')) == 0:
        pytest.skip("Skip test - Node and Edge Count Zero - most likely due to mesh not being deployed")

    # Validate Node count
    assert len(json.get('elements').get('nodes')) == mesh.nodes

    # Validate edge count
    assert len(json.get('elements').get('edges')) == mesh.edges
