from flask import Flask
from flask_socketio import SocketIO
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

brokers = ['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094']

def start_kafka_consumer():
    consumer = KafkaConsumer(
        "my-best-topic",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest'
    )

    for message in consumer:
        print(f"LOG_massage: {message.value}")
        socketio.emit('kafka_message', message.value)

@app.route('/')
def index():
    return 'Kafka WebSocket Server'

if __name__ == '__main__':
    print("start consumer")
    kafka_thread = threading.Thread(target=start_kafka_consumer)
    kafka_thread.daemon = True
    kafka_thread.start()
    print("consumer started")

    socketio.run(app, debug=True, port=5001)