from flask import Flask, request, jsonify
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import json

app = Flask(__name__)
brokers = ['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094']

def create_topic(topic_name, brokers, client):
  admin_client = KafkaAdminClient(
    bootstrap_servers=brokers, 
    client_id=client
  )
  create = True
  current_topics = admin_client.list_topics()
  for topic in current_topics:
    if topic == topic_name:
      create = False
  if create:
    topic_list = []
    topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=3))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    return True
  else: return False

producer = KafkaProducer(
    bootstrap_servers=brokers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/send', methods=['POST'])
def send_message():
    topic_name = "my-best-topic"
    client_id = "client3"
    data = request.get_json()
    for_logs = data
    print(str(for_logs))
    print(create_topic(topic_name, brokers, client_id))
    producer.send(topic_name, value=data)
    return jsonify({'status': 'success', 'data': data}), 200

if __name__ == '__main__':
    app.run(port=5000)
