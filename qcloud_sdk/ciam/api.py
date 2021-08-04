# -*- coding: utf-8 -*-

import requests


# ----- 鉴权客户端API -----

class CIAMAPIClient(object):
    def __init__(self, client_id, client_secret, custom_portal_name=None, custom_portal_domain=None):
        """
        访问某个用户目录下的某个应用鉴权API。

        :param client_id:
        :param client_secret:
        :param custom_portal_name: 腾讯云平台域名，填入控制台允许的自定义部分。
        :param custom_portal_domain: 自建域名，填入时覆盖腾讯云平台域名。注意不要带`/`后缀。
        """
        # 应用密钥
        self.client_id = client_id
        self.client_secret = client_secret
        # 用户目录API访问域名
        assert custom_portal_domain or custom_portal_name, '腾讯云平台域名或自建域名必须设置一个'
        self.portal_domain = custom_portal_domain or custom_portal_name + '.portal.tencentciam.com'
        self.portal_host = 'https://' + self.portal_domain
        # 用户目录OIDC公钥
        self._oidc_jwks = None

    def request_ciam_api(self, method, api, query_params=None, data=None, headers=None):
        api_url = self.portal_host + api
        r = requests.request(method, api_url, params=query_params, data=data, headers=headers, verify=r'./certs/tencentciam-com-chain.pem')
        return r.json()

    def get_oidc_jwks(self):
        return self.request_ciam_api('GET', '/oauth2/jwks')

    @property
    def odic_jwks(self):
        """
        JWT 公钥用于对 JWT 格式的 ID Token 和 Access Token 进行解密。
        JWT 密钥属于用户目录级，在创建用户目录时自动生成，不同用户目录的密钥不同。
        :return:
        """
        if self._oidc_jwks is None:
            self._oidc_jwks = self.get_oidc_jwks()
        return self._oidc_jwks

    def validate_oidc_id_token(self, id_token):
        pass


# ----- 函数式API -----

def oauth2_authorize():
    pass


def oauth2_login():
    pass


def oauth2_login_with_pkce():
    pass


def oauth2_login_with_auth_code():
    pass


def oauth2_register():
    pass


def oauth2_register_with_pkce():
    pass


def oauth2_register_with_auth_code():
    pass


def logout():
    pass


def get_oauth2_token():
    pass


def get_oauth2_token_with_pkce():
    pass


def get_oauth2_token_with_auth_code():
    pass


def get_oidc_jwks():
    pass


def validate_oauth2_access_token():
    pass


def validate_oidc_id_token() -> dict:
    pass


def get_and_validate_oauth2_access_token() -> dict:
    pass


def get_oidc_userinfo():
    pass
