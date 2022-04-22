# -*- coding: utf-8 -*-

from functools import partial
import hashlib

import crcmod


def calculate_file_md5(file_path, chunk_size=1024):
    with open(file_path, 'rb') as f:
        md5_digests = [hashlib.md5(chunk).digest() for chunk in iter(lambda: f.read(chunk_size), b'')]
    md5_str = hashlib.md5(b''.join(md5_digests)).hexdigest() + '-' + str(len(md5_digests))
    return md5_str


def calculate_file_crc64(file_path, chunk_size=1024):
    """
    CRC64校验工具

    - https://cloud.tencent.com/document/product/436/40334
    - http://crcmod.sourceforge.net/crcmod.html#mkcrcfun-crc-function-factory

    :param file_path: 文件路径
    :param chunk_size: default 1024
    :return:
    """
    crc64 = crcmod.Crc(0x142F0E1EBA9EA3693, initCrc=0, xorOut=0xffffffffffffffff, rev=True)
    with open(file_path, 'rb') as f:
        # https://docs.python.org/3/library/functions.html#iter
        for chunk in iter(partial(f.read, 64), b''):
            crc64.update(chunk)
    return crc64.crcValue
