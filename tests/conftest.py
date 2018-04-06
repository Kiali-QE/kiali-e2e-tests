import pytest
import yaml

@pytest.fixture(scope="session")
def config():
    with open('config/env.yaml', 'r') as yamlfile:
        config = yaml.load(yamlfile)
    return config
