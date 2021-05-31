# -*- coding: utf-8 -*-

import json
import hashlib
import hmac
from datetime import datetime


algorithm = 'TC3-HMAC-SHA256'
canonical_uri = "/"
signed_headers = "content-type;host"


def cal_hashed_payload(api_params):
    return hashlib.sha256(json.dumps(api_params).encode('utf-8')).hexdigest()


def join_canonical_request(endpoint, api_params):
    http_method = "POST"
    canonical_query_string = ""
    canonical_headers = "content-type:application/json; charset=utf-8\nhost:{endpoint}\n".format(endpoint=endpoint)
    hashed_payload = cal_hashed_payload(api_params)
    canonical_request = '\n'.join([http_method, canonical_uri, canonical_query_string, canonical_headers, signed_headers, hashed_payload])
    return canonical_request


def gen_canonical_scope(date, service):
    credential_scope = "{date}/{service}/tc3_request".format(date=date, service=service)
    return credential_scope


def join_unsigned_string(timestamp, credential_scope, canonical_request):
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    unsigned_string = '\n'.join([algorithm, timestamp, credential_scope, hashed_canonical_request])
    return unsigned_string


def cal_sign(secret_key, service, unsigned_string, date):
    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    secret_date = sign(("TC3"+secret_key).encode('utf-8'), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    sign = hmac.new(secret_signing, unsigned_string, hashlib.sha256).hexdigest()
    return sign


def cal_auth(secret_id, secret_key, endpoint, service, api_params, timestamp):
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    credential_scope = gen_canonical_scope(date, service)
    canonical_request = join_canonical_request(endpoint, api_params)
    unsigned_string = join_unsigned_string(service, credential_scope, canonical_request)
    sign = cal_sign(secret_key, service, unsigned_string, date)
    auth = algorithm + " " + "Credential=" + secret_id + "/" + credential_scope + ", " + "SignedHeaders=" + signed_headers + ", " + "Signature" + sign
    return auth
