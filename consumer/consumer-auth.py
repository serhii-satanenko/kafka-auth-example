from flask import Flask
from flask_socketio import SocketIO
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

brokers = ['localhost:9092', 'localhost:9093', 'localhost:9094']

def start_kafka_consumer():
    consumer = KafkaConsumer(
        "massages1",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username="client",
        sasl_plain_password="password"
    )

    while True:
        try:
            for message in consumer:
                print(f"LOG_message: {message.value}")
                socketio.emit('kafka_message', message.value)
        except Exception as e:
            print(f"Error in consumer: {e}")
            break

@app.route('/')
def index():
    return 'Kafka WebSocket Server'

if __name__ == '__main__':
    print("Start consumer")
    kafka_thread = threading.Thread(target=start_kafka_consumer)
    kafka_thread.daemon = True
    kafka_thread.start()
    print("Consumer started")

    socketio.run(app, debug=True, port=5001)
