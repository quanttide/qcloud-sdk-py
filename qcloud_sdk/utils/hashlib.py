# -*- coding: utf-8 -*-

import hashlib


def calculate_file_md5(file_path, chunk_size=1024):
    with open(file_path, 'rb') as f:
        md5_digests = [hashlib.md5(chunk).digest() for chunk in iter(lambda: f.read(chunk_size), b'')]
    md5_str = hashlib.md5(b''.join(md5_digests)).hexdigest() + '-' + str(len(md5_digests))
    return md5_str
