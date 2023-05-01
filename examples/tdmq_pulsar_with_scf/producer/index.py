"""
生产者示例
"""

from datetime import timedelta

import os
import pulsar


PULSAR_SERVICE_URL = os.environ.get('PULSAR_SERVICE_URL')
PULSAR_AUTHENTICATION = os.environ.get('PULSAR_AUTHENTICATION')
PULSAR_TOPIC = os.environ.get('PULSAR_TOPIC')


def main_handler(event, context):
    # 创建客户端
    client = pulsar.Client(
        authentication=pulsar.AuthenticationToken(PULSAR_AUTHENTICATION),
        service_url=PULSAR_SERVICE_URL
    )
    # 创建生产者
    producer = client.create_producer(topic=PULSAR_TOPIC)
    # 发送消息
    message_id = producer.send(
        # 消息内容
        'Hello python client, this is a delay msg'.encode('utf-8'),
        # 设置延迟时间
        deliver_after=timedelta(seconds=10)
    )
    print(f"已发布消息：{message_id}")
    # 关闭客户端
    client.close()
