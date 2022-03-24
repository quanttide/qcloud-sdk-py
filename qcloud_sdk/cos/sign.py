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
    # 遍历 HTTP 请求参数，生成 key 到 value 的映射 Map 及 key 的列表 KeyList：
    #   - key 使用 UrlEncode 编码并转换为小写形式。
    #   - value 使用 UrlEncode 编码。若无 value 的参数，则认为 value 为空字符串。例如请求路径为/?acl，则认为是/?acl=。
    params = {quote_plus(str(key).lower()): quote_plus(str(value)) for key, value in params.items()}
    # 将 KeyList 按照字典序排序。
    params = dict(sorted(params.items()))
    # 按照 KeyList 的顺序拼接 KeyList 中的每一项，格式为key1;key2;key3，即为 UrlParamList。
    encoded_keys = ';'.join(params.keys())
    # 按照 KeyList 的顺序拼接 Map 中的每一个键值对，格式为key1=value1&key2=value2&key3=value3，即为 HttpParameters。
    encoded_params = '&'.join([f'{key}={value}' for key, value in params.items()])
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
