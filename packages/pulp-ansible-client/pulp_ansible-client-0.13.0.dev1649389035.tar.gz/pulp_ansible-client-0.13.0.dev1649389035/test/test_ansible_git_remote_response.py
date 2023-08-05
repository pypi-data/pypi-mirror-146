# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.models.ansible_git_remote_response import AnsibleGitRemoteResponse  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException

class TestAnsibleGitRemoteResponse(unittest.TestCase):
    """AnsibleGitRemoteResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AnsibleGitRemoteResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ansible.models.ansible_git_remote_response.AnsibleGitRemoteResponse()  # noqa: E501
        if include_optional :
            return AnsibleGitRemoteResponse(
                headers = [
                    None
                    ], 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                proxy_url = '0', 
                ca_cert = '0', 
                total_timeout = 0.0, 
                connect_timeout = 0.0, 
                tls_validation = True, 
                rate_limit = 56, 
                download_concurrency = 1, 
                pulp_last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                sock_read_timeout = 0.0, 
                max_retries = 56, 
                url = '0', 
                pulp_href = '0', 
                sock_connect_timeout = 0.0, 
                pulp_labels = pulpcore.client.pulp_ansible.models.pulp_labels.pulp_labels(), 
                client_cert = '0', 
                name = '0', 
                metadata_only = True, 
                git_ref = '0'
            )
        else :
            return AnsibleGitRemoteResponse(
                url = '0',
                name = '0',
        )

    def testAnsibleGitRemoteResponse(self):
        """Test AnsibleGitRemoteResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
