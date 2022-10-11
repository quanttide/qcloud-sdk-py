# 数据校验

```python
class S3Object(object):
    def calculate_local_etag(self, chunk_size=1024) -> str:
        """
        Ref:
          - https://teppen.io/2018/10/23/aws_s3_verify_etags/
          - https://www.programminghunter.com/article/1321266330/
        :return:
        """
        md5_digests = []
        with open(self.local_file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                md5_digests.append(hashlib.md5(chunk).digest())
        return hashlib.md5(b''.join(md5_digests)).hexdigest() + '-' + str(len(md5_digests))

    def validate_etag(self, file_path, chunk_size=1024) -> bool:
        """
        验证文件的ETag是否与本地文件一致。仅可以在非分块上传和非加密的情况下使用。

        TODO：支持分块上传或加密模式的ETAG验证。

        Ref:
          - https://teppen.io/2018/10/23/aws_s3_verify_etags/

        :param file_path:
        :param chunk_size:
        :return:
        """

    def calculate_local_crc64(self) -> int:
        """
        Ref:
          - https://cloud.tencent.com/document/product/436/40334
          - https://help.aliyun.com/document_detail/43394.html
          - https://cloud.google.com/storage/docs/gsutil/addlhelp/CRC32CandInstallingcrcmod?hl=zh-cn
          - http://crcmod.sourceforge.net
        :return:
        """
        pass

    def validate_crc64(self) -> bool:
        """
        Ref:
          - https://cloud.tencent.com/document/product/436/40334
        :return:
        """
        pass

    def validate_content_md5(self) -> bool:
        """
        Ref:
          - https://datatracker.ietf.org/doc/html/rfc1864
          - https://help.aliyun.com/document_detail/31951.html?utm_content=g_1000230851&spm=5176.20966629.toubu.3.f2991ddcpxxvD1#title-u0s-z0b-imx
        :return:
        """
        pass
```