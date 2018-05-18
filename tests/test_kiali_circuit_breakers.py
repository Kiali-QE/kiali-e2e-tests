import os
import conftest
from utils.timeout import timeout
import time

PARAMS = {'duration': '1m'}

def test_kiali_circuit_breakers(kiali_client):
    environment_configmap = conftest.__get_environment_config__(conftest.ENV_FILE)
    circuit_breaker_configmap = conftest.__get_environment_config__(conftest.CIRCUIT_BREAKER_FILE)

    add_command_text = "oc apply -n " + environment_configmap.get('mesh_bookinfo_namespace') + " -f " + os.path.abspath(os.path.realpath(conftest.CIRCUIT_BREAKER_FILE))

    add_command_result = os.popen(add_command_text).read()

    assert add_command_result.__contains__("created") or add_command_result.__contains__("configured")

    graph = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)

    assert graph is not None

    with timeout(seconds=30, error_message='Timed out waiting for Circuit Breaker to be Created'):
        while True:

            nodes = kiali_client.graph_namespace(namespace=environment_configmap.get('mesh_bookinfo_namespace'), params=PARAMS)["elements"]['nodes']

            assert nodes is not None

            circuit_breaker = 0
            for node in nodes:
                if 'hasCB' in node["data"] and  node["data"]["hasCB"] == "true":
                    circuit_breaker = circuit_breaker +1

            if circuit_breaker is 1:
                break

            time.sleep(1)

    delete_command_text = "oc delete destinationpolicies " + circuit_breaker_configmap['metadata']['name'] + " -n " +  environment_configmap.get('mesh_bookinfo_namespace')

    delete_command_result = os.popen(delete_command_text).read()

    assert delete_command_result.__contains__("deleted")
