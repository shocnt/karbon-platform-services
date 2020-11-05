from kafka import KafkaConsumer

def main():
    consumer = KafkaConsumer(
            'shuchida-dp-mqtt-kafka', 
            bootstrap_servers=['10.42.10.83:32093'])

    for message in consumer:
        print(message.value.decode())

if __name__ == '__main__':
    main()
