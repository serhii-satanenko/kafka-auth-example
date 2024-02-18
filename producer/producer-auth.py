from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)
brokers = ['localhost:9092', 'localhost:9093', 'localhost:9094']

producer = KafkaProducer(
  bootstrap_servers=brokers,
  value_serializer=lambda v: json.dumps(v).encode('utf-8'),
  security_protocol="SASL_PLAINTEXT",
  sasl_mechanism="PLAIN",
  sasl_plain_username="produser",
  sasl_plain_password="password"
)

@app.route('/send', methods=['POST'])
def send_message():
  topic_name = "massages1"
  data = request.get_json()
  
  try:
    # Відправляємо повідомлення та чекаємо на результат
    future = producer.send(topic_name, value=data)
    result = future.get(timeout=10)  # Чекаємо на завершення до 10 секунд
    print(f"Message sent: {result}")
    return jsonify({'status': 'success', 'data': data}), 200
  except Exception as e:
    print(f"Failed to send message: {e}")
    return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
  app.run(port=5000)
