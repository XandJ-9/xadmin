from kafka import KafkaConsumer

def create_kafka_consumer(bootstrap_servers, group_id, auto_offset_reset='earliest'):
    """
    创建一个 Kafka 消费者实例。

    :param bootstrap_servers: Kafka 服务器地址列表
    :param group_id: 消费者组 ID
    :param auto_offset_reset: 当没有初始偏移量或当前偏移量在服务器上不存在时的行为
    :return: KafkaConsumer 实例
    """
    config = {
        'bootstrap_servers': bootstrap_servers,
        'group_id': group_id,
        'auto_offset_reset': auto_offset_reset
    }
    return KafkaConsumer(**config)

def consume_messages(consumer, timeout_ms=1000):
    """
    消费 Kafka 主题中的消息。

    :param consumer: KafkaConsumer 实例
    :param timeout_ms: 轮询超时时间（毫秒）
    """
    while True:
        data = consumer.poll(timeout_ms=timeout_ms)
        if not data:
            print("No messages received.")
        else:
            for topic_partition, messages in data.items():
                for message in messages:
                    print(f"Received message: {message.value.decode('utf-8')}")

if __name__ == "__main__":
    # 配置 Kafka 连接参数
    bootstrap_servers = '39.108.175.203:9092'
    group_id = 'test'

    # 创建 Kafka 消费者
    consumer = create_kafka_consumer(bootstrap_servers, group_id)
    consumer.subscribe(['test'])
    print("Starting consumer...\n \
          connected : %s \n \
          topics: %s \n"
          %(consumer.bootstrap_connected(), consumer.topics()))
    try:
        # 开始消费消息
        consume_messages(consumer)
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        # 关闭消费者
        consumer.close()