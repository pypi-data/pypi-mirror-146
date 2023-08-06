# -*- coding: UTF-8 -*-
# @Time : 2021/12/2 下午5:55 
# @Author : 刘洪波
from retry import retry
import pika
from pika import exceptions
from concurrent.futures import ThreadPoolExecutor
import loguru


class Connection(object):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = None

    def consumer(self, channel, task, thread_count):
        """
        消费者
        :param channel:  处理消息的业务功能
        :param task:  处理消息的业务功能
        :param thread_count:
        :return:
        """
        if thread_count:
            pool = ThreadPoolExecutor(max_workers=thread_count)

        def callback(ch, method, properties, body):
            body = body.decode('utf8')
            if thread_count:
                pool.submit(task, body)
            else:
                task(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        channel.basic_consume(queue=self.queue_name, auto_ack=False, on_message_callback=callback)
        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()

    def send(self, message_list: list, exchange, routing_key, durable=False, heartbeat=60):
        """
        发送数据
        :param message_list:
        :param exchange:
        :param routing_key:
        :param durable:
        :param heartbeat: 心跳检测，默认60秒检测一次心跳
        :return:
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=pika.PlainCredentials(self.username, self.password),
            heartbeat=heartbeat)
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=durable)
        for message in message_list:
            channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        connection.close()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3), logger=loguru.logger)
    def receive(self, exchange, routing_key, task, durable=False, thread_count=None, heartbeat=60):
        """
        消费者消费
        :param exchange:
        :param routing_key:
        :param task:
        :param durable:
        :param thread_count: 当thread_count 有值的时候，可以进行多线程并行消费
        :param heartbeat: 心跳检测，默认60秒检测一次心跳
        :return:
        """
        loguru.logger.info('开始连接rabbitmq')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=pika.PlainCredentials(self.username, self.password),
            heartbeat=heartbeat)
        )
        loguru.logger.info('已连接至rabbitmq')
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=durable)
        self.queue_name = routing_key
        try:
            channel.queue_declare(queue=self.queue_name, passive=True)
        except Exception as e:
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=durable)
            channel.queue_declare(queue=self.queue_name)
            channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key=routing_key)
        self.consumer(channel=channel, task=task, thread_count=thread_count)

    def service(self, task, consumer_exchange, consumer_routing_key,
                producer_exchange, producer_routing_key, durable=False, thread_count=None, heartbeat=60):
        """
        rabbitmq 服务
        1. 订阅rabbitmq
        2. 处理消费的数据
        3. 发送得到的结果
        :param task:
        :param consumer_exchange:
        :param consumer_routing_key:
        :param producer_exchange:
        :param producer_routing_key:
        :param thread_count:
        :param durable:
        :param heartbeat: 心跳检测，默认60秒检测一次心跳
        :return:
        """
        def callback(body):
            result = task(body)
            if result:
                self.send(result, producer_exchange, producer_routing_key, durable, heartbeat)
        self.receive(consumer_exchange, consumer_routing_key, callback, durable, thread_count, heartbeat)

