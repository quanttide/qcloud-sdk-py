# -*- coding: utf-8 -*-

import crcmod


def calculate_file_crc64(file_path):
    crc64_func = crcmod.mkCrcFun(0x142F0E1EBA9EA3693, initCrc=0, xorOut=0xffffffffffffffff, rev=True)
    with open(file_path, 'rb') as f:
        result = crc64_func(f.read())
    return result
