import unittest


from tests.client import APIClientTestCase


class CosAPITestCase(APIClientTestCase):
    def setUp(self):
        self.method = 'GET'
        self.host = 'service.cos.myqcloud.com'
        self.path = '/'
        self.query_params = {}
        self.headers = {}

    def test_generate_cos_request_headers(self):
        headers = self.client.generate_cos_request_headers(self.method, self.host, self.path, self.query_params, self.headers)
        self.assertTrue('Authorization' in headers)

    def test_request_cos_api(self):
        response = self.client.request_cos_api(self.method, self.host, self.path, self.query_params, self.headers)
        self.assertTrue(response.data)


if __name__ == '__main__':
    unittest.main()
