import time
import conftest
import os
from utils.timeout import timeout

PARAMS = {'duration': '1m'}


def _test_kiali_route_rules(kiali_client):
    environment_configmap = conftest.__get_environment_config__(conftest.ENV_FILE)
    route_rule_configmap = conftest.__get_environment_config__(conftest.ROUTE_RULE_FILE)

    add_command_text = "oc apply -n " + environment_configmap.get('mesh_bookinfo_namespace') + " -f " + os.path.abspath(os.path.realpath(conftest.ROUTE_RULE_FILE))

    add_command_result = os.popen(add_command_text).read()

    assert add_command_result.__contains__("created") or add_command_result.__contains__("configured")

    graph = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)

    assert graph is not None

    nodes = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)["elements"]['nodes']

    assert nodes is not None

    with timeout(seconds=30, error_message='Timed out waiting for RouteRule to be Created'):
        while True:
            if get_route_rule_count(kiali_client, environment_configmap) > 0:
                break

            time.sleep(1)

    delete_command_text = "oc delete routerule " + route_rule_configmap['metadata'][
        'name'] + " -n " + environment_configmap.get('mesh_bookinfo_namespace')

    delete_command_result = os.popen(delete_command_text).read()

    assert delete_command_result.__contains__("deleted")

    with timeout(seconds=300, error_message='Timed out waiting for RouteRule to be Deleted'):
        while True:
            # Validate that JSON no longer has Route Rules
            if get_route_rule_count(kiali_client, environment_configmap) == 0:
                break

            time.sleep(1)

def get_route_rule_count(kiali_client, environment_configmap):

    nodes = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)[
        "elements"]['nodes']

    assert nodes is not None

    route_rule_count = 0
    for node in nodes:
        if 'hasRR' in node["data"] and node["data"]["hasRR"] == "true":
            route_rule_count = route_rule_count + 1

    return route_rule_count
