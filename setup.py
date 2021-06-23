from setuptools import setup, find_packages

setup(
    name='qcloud-sdk-py',
    version='0.0.1',
    packages=find_packages(exclude=["cloudbase", "cloudbase.*"]),
    url='quanttide.com',
    license='Apache 2.0',
    author='QuantTide Inc.',
    author_email='tech@quanttide.com',
    description='TencentCloud Python SDK for Humans',
    install_requires=[
        'requests'
    ],
)
