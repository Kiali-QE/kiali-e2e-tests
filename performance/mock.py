import base64
from influxdb import InfluxDBClient
from kiali import KialiClient
import yaml

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


ENV_FILE = '../config/env.yaml'

class mock(object):
    def __init__(self):
        super(mock, self).__init__()

    def create_database(self):
        config = self.get_environment_config(ENV_FILE)
        return self.get_influxClient().query("CREATE DATABASE " + config.get("influx_database"))


    def get_minWait(self):
        config = self.get_environment_config(ENV_FILE)
        return int(config.get("min_wait"))

    def get_maxWait(self):
        config = self.get_environment_config(ENV_FILE)
        return int(config.get("max_wait"))

    def get_graph_url(self, hostname, namespace, params):
        kiali_client = self.get_kiali_client(hostname)
        base_url = kiali_client._get_graph_namespace_url(namespace)
        return self.format_url_params(params,base_url)


    def get_influxClient(self):
        config = self.get_environment_config(ENV_FILE)
        return InfluxDBClient(
            **{'host': config.get("influx_hostname"), 'username': config.get("influx_username"),
               'port': config.get("influx_port"), 'database': config.get("influx_database"),
               'password': config.get("influx_password")})


    def get_headers(self):
        config = self.get_environment_config(ENV_FILE)
        return {'Authorization': "Basic %s" % base64.b64encode(
            config.get('kiali_username') + ":" + config.get('kiali_password')), "Content-Type":
             "application/json"}

    def get_kiali_client(self, hostname):
        config = self.get_environment_config(ENV_FILE)
        return KialiClient(host=hostname,
                           username=config.get('kiali_username'), password=config.get('kiali_password'))

    def get_environment_config(self, env_file):
        with open(env_file) as yamlfile:
            config = yaml.load(yamlfile)
        return config


    def format_url_params(self,url_params, base_url):
        params = urlencode(url_params)
        if len(params) > 0:
            final_url = '{0}?{1}'.format(base_url, params)
        return final_url