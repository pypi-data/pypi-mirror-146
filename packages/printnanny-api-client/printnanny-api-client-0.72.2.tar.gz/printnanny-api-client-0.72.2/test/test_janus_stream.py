# coding: utf-8

"""
    printnanny-api-client

    Official API client library forprintnanny.ai print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import printnanny_api_client
from printnanny_api_client.models.janus_stream import JanusStream  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestJanusStream(unittest.TestCase):
    """JanusStream unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JanusStream
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.janus_stream.JanusStream()  # noqa: E501
        if include_optional :
            return JanusStream(
                id = 56, 
                auth = None, 
                api_domain = '', 
                api_port = 56, 
                api_url = '', 
                admin_url = '', 
                admin_port = 56, 
                rtp_domain = '', 
                ws_url = '', 
                ws_port = 56, 
                config_type = '', 
                created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                active = True, 
                secret = '', 
                pin = '', 
                info = {
                    'key' : null
                    }, 
                rtp_port = 56, 
                device = 56
            )
        else :
            return JanusStream(
                id = 56,
                auth = None,
                api_domain = '',
                api_port = 56,
                api_url = '',
                admin_url = '',
                admin_port = 56,
                rtp_domain = '',
                ws_url = '',
                ws_port = 56,
                config_type = '',
                created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                active = True,
                secret = '',
                pin = '',
                info = {
                    'key' : null
                    },
                rtp_port = 56,
                device = 56,
        )

    def testJanusStream(self):
        """Test JanusStream"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
