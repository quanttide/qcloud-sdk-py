"""
消费者示例
"""

import os

import pulsar


PULSAR_SERVICE_URL = os.environ.get('PULSAR_SERVICE_URL')
PULSAR_AUTHENTICATION = os.environ.get('PULSAR_AUTHENTICATION')
PULSAR_TOPIC = os.environ.get('PULSAR_TOPIC')
PULSAR_SUBSCRIPTION_NAME = os.environ.get('PULSAR_SUBSCRIPTION_NAME')


def main_handler(event, context):
    # 创建客户端
    client = pulsar.Client(
        authentication=pulsar.AuthenticationToken(PULSAR_AUTHENTICATION),
        service_url=PULSAR_SERVICE_URL
    )
    # 订阅消息
    consumer = client.subscribe(
        topic=PULSAR_TOPIC,
        subscription_name=PULSAR_SUBSCRIPTION_NAME,
        # 指定订阅类型为共享模式
        consumer_type=pulsar.ConsumerType.Shared
    )
    # 处理消息
    try:
        # 消费消息。没有消息时等待1s之后抛出Timeout异常。
        msg = consumer.receive(timeout_millis=1000)
        print(f'Received message: {msg.data()}')
        try:
            # 标记消息已处理
            consumer.acknowledge(msg)
        except Exception as e:
            # 处理消息时发生异常，将消息标记为处理失败
            consumer.negative_acknowledge(msg)
    except Exception as e:
        # Note：Pulsar未封装C++的Exception类为Python类供程序使用。
        # 如果超时，消费者应自动解除订阅
        print(f'No message received. TimeoutException: {e}')
    finally:
        # 关闭消费者和客户端
        consumer.close()
        client.close()
