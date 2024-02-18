from flask import Flask, jsonify
from kafka import KafkaConsumer
import json

app = Flask(__name__)
brokers = ['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094']


consumer = KafkaConsumer(
    "my-best-topic",
    bootstrap_servers=brokers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

@app.route('/receive', methods=['GET'])
def receive_message():
    messages = []
    for message in consumer:
        messages.append(message.value)
        break  # Remove this line if you want to consume more than one message at a time.
    return jsonify(messages)

if __name__ == '__main__':
    app.run(port=5001)
