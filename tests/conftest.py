import pytest
import yaml
from kiali import KialiClient

@pytest.fixture(scope="session")

def kiali_json():

    with open('config/env.yaml', 'r') as yamlfile:
        config = yaml.load(yamlfile)

        client = KialiClient(host=config.get('kiali_hostname'),
                             username=config.get('kiali_username'), password=config.get('kiali_password'))

    return client.graph_namespace(namespace=config.get('mesh_bookinfo_namespace'),
                                  params={'duration': '1m'}).to_json_object()

