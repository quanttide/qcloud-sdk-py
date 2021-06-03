# -*- coding: utf-8 -*-

import json
import hashlib
import hmac
from datetime import datetime

algorithm = 'TC3-HMAC-SHA256'  # 签名方法V3
http_method = "POST"
canonical_query_string = ""
canonical_uri = "/"
signed_headers = "content-type;host"


def cal_hashed_payload(api_params):
    return hashlib.sha256(json.dumps(api_params).encode('utf-8')).hexdigest()


def join_canonical_request(endpoint, api_params):
    canonical_headers = "content-type:application/json\nhost:{endpoint}\n".format(endpoint=endpoint)
    hashed_payload = cal_hashed_payload(api_params)
    canonical_request = '\n'.join(
        [http_method, canonical_uri, canonical_query_string, canonical_headers, signed_headers, hashed_payload])
    return canonical_request


def gen_canonical_scope(date, service):
    credential_scope = "{date}/{service}/tc3_request".format(date=date, service=service)
    return credential_scope


def join_unsigned_string(timestamp, credential_scope, canonical_request):
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    unsigned_string = '\n'.join([algorithm, str(timestamp), credential_scope, hashed_canonical_request])
    return unsigned_string


def sign(secret_key, service, unsigned_string, date):
    sign_func = lambda key, msg: hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    secret_date = sign_func(("TC3" + secret_key).encode('utf-8'), date)
    secret_service = sign_func(secret_date, service)
    secret_signing = sign_func(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, unsigned_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def join_auth(secret_id: str, secret_key: str, endpoint: str, service: str, api_params: dict, timestamp: int) -> str:
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    credential_scope = gen_canonical_scope(date, service)
    canonical_request = join_canonical_request(endpoint, api_params)
    unsigned_string = join_unsigned_string(timestamp, credential_scope, canonical_request)
    signature = sign(secret_key, service, unsigned_string, date)
    auth = algorithm + " " + "Credential=" + secret_id + "/" + credential_scope + ", " + "SignedHeaders=" + signed_headers + ", " + "Signature=" + signature
    return auth
