import os
import conftest

PARAMS = {'duration': '1m'}


def test_kiali_route_rules(kiali_client):
    environment_configmap = conftest.__get_environment_config__(conftest.ENV_FILE)
    route_rule_configmap = conftest.__get_environment_config__(conftest.ROUTE_RULE_FILE)

    add_command_text = "oc apply -n " + environment_configmap.get('mesh_bookinfo_namespace') + " -f " + os.path.abspath(os.path.realpath(conftest.ROUTE_RULE_FILE))

    add_command_result = os.popen(add_command_text).read()

    assert add_command_result.__contains__("created") or add_command_result.__contains__("configured")

    graph = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)

    assert graph is not None

    nodes = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)["elements"]['nodes']

    assert nodes is not None

    route_rule = 0
    for node in nodes:
        if 'hasRR' in node["data"] and  node["data"]["hasRR"] == "true":
            route_rule = route_rule +1

    assert route_rule is 2

    delete_command_text = "oc delete routerule " + route_rule_configmap['metadata']['name'] + " -n " +  environment_configmap.get('mesh_bookinfo_namespace')

    delete_command_result = os.popen(delete_command_text).read()

    assert delete_command_result.__contains__("deleted")
