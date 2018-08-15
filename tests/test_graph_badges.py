import os
import conftest
from utils.timeout import timeout
import time

DURATION = '60s'
VERSIONED_APP_PARAMS = {'graphType': 'versionedApp', 'duration': DURATION}
WORKLOAD_PARAMS      = {'graphType': 'workload', 'duration': DURATION}

def test_kiali_circuit_breakers_versioned_app(kiali_client):
    assert do_test(kiali_client, VERSIONED_APP_PARAMS, conftest.CIRCUIT_BREAKER_FILE)

def test_kiali_circuit_breakers_workload(kiali_client):
    assert do_test(kiali_client, WORKLOAD_PARAMS, conftest.CIRCUIT_BREAKER_FILE)

def test_kiali_virtual_service_versioned_app(kiali_client):
    assert do_test(kiali_client, VERSIONED_APP_PARAMS, conftest.VIRTUAL_SERVICE_FILE)

def test_kiali_virtual_service_workload(kiali_client):
    assert do_test(kiali_client, WORKLOAD_PARAMS, conftest.VIRTUAL_SERVICE_FILE)


def do_test(kiali_client, graph_params, yaml_file):
    environment_configmap = conftest.__get_environment_config__(conftest.ENV_FILE)
    bookinfo_namespace = environment_configmap.get('mesh_bookinfo_namespace')

    appType = kiali_client.graph_namespace(namespace=bookinfo_namespace, params=graph_params)['graphType']
    assert appType == graph_params.get('graphType')

    cb_count = get_cb_count(kiali_client, bookinfo_namespace, graph_params)

    add_command_text = "oc apply -n " + bookinfo_namespace + " -f " + os.path.abspath(os.path.realpath(yaml_file))
    add_command_result = os.popen(add_command_text).read()
    assert add_command_result.__contains__("created") or add_command_result.__contains__("configured")

    graph = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=graph_params)
    assert graph is not None

    with timeout(seconds=60, error_message='Timed out waiting for Create'):
        while True:
            if get_cb_count(kiali_client, bookinfo_namespace, graph_params) >= cb_count:
                break

    time.sleep(1)
    delete_command_text = "oc delete -n " + bookinfo_namespace + " -f " + os.path.abspath(os.path.realpath(yaml_file))
    delete_command_result = os.popen(delete_command_text).read()
    assert delete_command_result.__contains__("deleted")

    with timeout(seconds=30, error_message='Timed out waiting for Delete'):
        while True:
            # Validate that JSON no longer has Virtual Service
            if get_cb_count(kiali_client, bookinfo_namespace, graph_params) <= cb_count:
                break

            time.sleep(1)

    return True

def get_cb_count(kiali_client, bookinfo_namespace, graph_params):

    nodes = kiali_client.graph_namespace(namespace=bookinfo_namespace, params=graph_params)["elements"]['nodes']
    assert nodes is not None

    cb_count = 0
    for node in nodes:
        if 'hasCB' in node["data"] and node["data"]["hasCB"]:
            cb_count = cb_count + 1

    return cb_count