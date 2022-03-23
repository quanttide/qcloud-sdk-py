"""
签名算法V3

https://cloud.tencent.com/document/product/213/30654
"""

import json
import hashlib
import hmac
from datetime import datetime


# 签名方法配置，支持的签名方法为V3
ALGORITHM = 'TC3-HMAC-SHA256'
HTTP_METHOD = "POST"
CANONICAL_QUERY_STRING = ""
CANONICAL_URI = "/"
SIGNED_HEADERS = "content-type;host"


def calculate_hashed_payload(api_params):
    return hashlib.sha256(json.dumps(api_params).encode('utf-8')).hexdigest()


def join_canonical_request(endpoint, api_params):
    canonical_headers = f"content-type:application/json\nhost:{endpoint}\n"
    hashed_payload = calculate_hashed_payload(api_params)
    canonical_request = '\n'.join(
        [HTTP_METHOD, CANONICAL_URI, CANONICAL_QUERY_STRING, canonical_headers, SIGNED_HEADERS, hashed_payload])
    return canonical_request


def gen_canonical_scope(date, service):
    credential_scope = f"{date}/{service}/tc3_request"
    return credential_scope


def join_unsigned_string(timestamp, credential_scope, canonical_request):
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    unsigned_string = '\n'.join([ALGORITHM, str(timestamp), credential_scope, hashed_canonical_request])
    return unsigned_string


def sign(secret_key, service, unsigned_string, date):
    sign_func = lambda key, msg: hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    secret_date = sign_func(("TC3" + secret_key).encode('utf-8'), date)
    secret_service = sign_func(secret_date, service)
    secret_signing = sign_func(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, unsigned_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def calculate_auth_string(secret_id: str, secret_key: str, endpoint: str, service: str, api_params: dict, timestamp: int) -> str:
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    credential_scope = gen_canonical_scope(date, service)
    canonical_request = join_canonical_request(endpoint, api_params)
    unsigned_string = join_unsigned_string(timestamp, credential_scope, canonical_request)
    signature = sign(secret_key, service, unsigned_string, date)
    auth = ALGORITHM + " " + "Credential=" + secret_id + "/" + credential_scope + ", " + "SignedHeaders=" + SIGNED_HEADERS + ", " + "Signature=" + signature
    return auth
