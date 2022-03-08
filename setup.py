from setuptools import setup, find_packages

setup(
    name='qcloud-sdk-py',
    version='0.1.0-alpha.1',
    packages=find_packages(exclude=["tests", "tests.*"]),
    url='quanttide.com',
    license='Apache 2.0',
    author='QuantTide Inc.',
    author_email='tech@quanttide.com',
    description='腾讯云Python服务端SDK',
    install_requires=[
        'requests'
    ],
)
