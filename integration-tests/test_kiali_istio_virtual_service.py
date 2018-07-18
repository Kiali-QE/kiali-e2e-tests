import time
import conftest
import os
from utils.timeout import timeout

PARAMS = {'duration': '1m'}

def test_kiali_virtual_service(kiali_client):
    environment_configmap = conftest.__get_environment_config__(conftest.ENV_FILE)
    bookinfo_namespace = environment_configmap.get('mesh_bookinfo_namespace')

    add_command_text = "oc apply -n " + bookinfo_namespace + " -f " + os.path.abspath(os.path.realpath(conftest.VIRTUAL_SERVICE_FILE))
    add_command_result = os.popen(add_command_text).read()

    assert add_command_result.__contains__("created") or add_command_result.__contains__("configured")

    graph = kiali_client.graph_namespace(namespace=bookinfo_namespace, params=PARAMS)

    assert graph is not None

    nodes = kiali_client.graph_namespace(namespace=bookinfo_namespace, params=PARAMS)["elements"]['nodes']

    assert nodes is not None

    with timeout(seconds=30, error_message='Timed out waiting for VirtualService to be Created'):
        while True:
            if get_vs_count(kiali_client, bookinfo_namespace) > 0:
                break

            time.sleep(1)

    delete_command_text = "oc delete -n {} -f {}".format(bookinfo_namespace, conftest.VIRTUAL_SERVICE_FILE)
    delete_command_result = os.popen(delete_command_text).read()

    assert delete_command_result.__contains__("deleted")

    with timeout(seconds=30, error_message='Timed out waiting for VirtualService to be Deleted'):
        while True:
            # Validate that JSON no longer has Virtual Service
            if get_vs_count(kiali_client, bookinfo_namespace) == 0:
                break

            time.sleep(1)

def get_vs_count(kiali_client, bookinfo_namespace):

    nodes = kiali_client.graph_namespace(namespace=bookinfo_namespace, params=PARAMS)["elements"]['nodes']

    assert nodes is not None

    vs_count = 0
    for node in nodes:
        if 'hasVS' in node["data"] and node["data"]["hasVS"]:
            vs_count = vs_count + 1

    return vs_count
