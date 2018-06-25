"""
Copyright 2015-2017 Red Hat, Inc. and/or its affiliates
and other contributors as indicated by the @author tags.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

author Guilherme Baufaker Rego

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
"""
import json
import random

import locust.events
import locust.stats
from locust import HttpLocust, TaskSet, task
from mock import mock


class KialiEvent(TaskSet):
    def count_valid_services(self, nodes):
        nodes_with_version = 0
        for node in nodes:
            if 'version' in node["data"] and node["data"]["version"] != "unknown":
                nodes_with_version = nodes_with_version + 1
        return nodes_with_version



    @task(1)
    def check_api_graph(self):
        utils = mock()
        additionalParams = {'duration': '1m'}
        global response_json, response_code, number_of_services


        response_code = None
        response_json = None
        number_of_services = None

        url = utils.get_graph_url(namespace="all", hostname=self.locust.host, params=additionalParams)

        try:
            with self.client.get(url=url, headers=utils.get_headers(), catch_response=True) \
                as response:
                response_json = json.loads(response.content)
                response_code = response.status_code
                number_of_services = self.count_valid_services(response_json.get('elements').get('nodes'))
        except ValueError:
            response.failure("Something Wrong happened")

class KialiUser(HttpLocust):
    task_set = KialiEvent

    def __init__(self):
        super(KialiUser, self).__init__()
        self.utils = mock()
        self.identifier = random.getrandbits(128)
        self.influxClient = self.utils.get_influxClient()
        self.min_wait = self.utils.get_minWait()
        self.max_wait = self.utils.get_maxWait()
        self.utils.create_database()
        locust.events.request_success += self.hook_request_success
        locust.events.request_failure += self.hook_request_fail
        locust.events.quitting += self.hook_locust_quit

    def hook_request_success(self, request_type, name, response_time, response_length):
        metrics = {}

        tags = {'execution': self.identifier, "path": name, 'response_code': response_code}
        metrics['measurement'] = "request"
        fields = {'request_type': request_type, 'response_time': response_time, 'response_length': response_length,"number_of_services": number_of_services}
        metrics['fields'] = fields
        metrics['tags'] = tags
        self.influxClient.write_points([metrics])

    def hook_request_fail(self, request_type, name, response_time, exception):
        metrics = {}
        tags = {'execution': self.identifier, "path": name, 'response_code': response_code}
        metrics['measurement'] = "fail"
        fields = {'request_type': request_type, 'name': name}
        metrics['fields'] = fields
        metrics['tags'] = tags
        self.influxClient.write_points([ metrics])

    def hook_locust_quit(self):
        print "Quitting Locust"