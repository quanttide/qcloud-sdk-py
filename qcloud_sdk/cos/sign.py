"""
对象存储请求签名

参考资料：
- 签名算法文档：https://cloud.tencent.com/document/product/436/7778
- 签名工具：https://cloud.tencent.com/document/product/436/30442
"""

import hmac
import hashlib
import time
from urllib.parse import quote_plus, urlencode


def join_key_time(begin_time=None, expire=None):
    """
    步骤1：生成KeyTime

    :param begin_time:
    :param expire: 默认为3600秒（1小时）
    :return:
    """
    begin_time = begin_time or int(time.time())
    expire = expire or 3600
    end_time = begin_time + expire
    return f"{begin_time};{end_time}"


def calculate_sign_key(key_time, secret_key):
    """
    步骤2：生成SignKey

    :param key_time:
    :param secret_key:
    :return:
    """
    return hmac.new(secret_key.encode('utf-8'), key_time.encode('utf-8'), hashlib.sha1).hexdigest()


def join_http_params(params):
    """
    步骤3和4的通用函数
    - 步骤3：生成UrlParamList和HttpParameters
    - 步骤4：生成HeaderList和HttpHeaders
    :return:
    """
    encoded_keys = ';'.join(sorted([quote_plus(param.lower()) for param in params.keys()]))
    encoded_params = urlencode(dict(sorted(params.items())))
    return encoded_keys, encoded_params


def join_http_string(method, path, http_parameters, headers):
    """
    步骤5：生成HttpString
    """
    return f'{method.lower()}\n{path}\n{http_parameters}\n{headers}\n'


def calculate_string_to_sign(key_time, http_string):
    """
    步骤6
    :return:
    """
    sha1 = hashlib.sha1()
    sha1.update(http_string.encode('utf-8'))
    http_string_sha1 = sha1.hexdigest()
    return f'sha1\n{key_time}\n{http_string_sha1}\n'


def calculate_signature(sign_key, string_to_sign):
    """
    步骤7
    :param secret_key:
    :param string_to_sign:
    :return:
    """
    return hmac.new(sign_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).hexdigest()


def join_auth_string(secret_id, key_time, header_list, url_param_list, signature):
    """
    步骤8：生成签名
    :return:
    """
    return '&'.join(['q-sign-algorithm=sha1', f'q-ak={secret_id}', f'q-sign-time={key_time}',
                     f'q-key-time={key_time}', f'q-header-list={header_list}', f'q-url-param-list={url_param_list}',
                     f'q-signature={signature}'])


def calculate_auth_string(method, path, query_params, headers, secret_id, secret_key, begin_time=None, expire=None):
    # 步骤1：生成KeyTime
    key_time = join_key_time(begin_time=begin_time, expire=expire)
    # 步骤2：生成SignKey
    sign_key = calculate_sign_key(key_time=key_time, secret_key=secret_key)
    # 步骤3：生成UrlParamList和HttpParameters
    url_param_list, http_parameters = join_http_params(query_params)
    # 步骤4：生成HeaderList和HttpHeaders
    header_list, http_headers = join_http_params(headers)
    # 步骤5：生成HttpString
    http_string = join_http_string(method, path, http_parameters, http_headers)
    # 步骤6：生成StringToSign
    string_to_sign = calculate_string_to_sign(key_time=key_time, http_string=http_string)
    # 步骤7：生成Signature
    signature = calculate_signature(sign_key=sign_key, string_to_sign=string_to_sign)
    # 步骤8：生成签名
    return join_auth_string(secret_id, key_time, header_list, url_param_list, signature)
