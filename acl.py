from kafka.admin import KafkaAdminClient, NewTopic, ACL, ResourcePattern, ResourceType, ACLOperation, ACLPermissionType
from kafka.errors import TopicAlreadyExistsError

def create_topic_with_acls(admin_client, topic_name, num_partitions, replication_factor, acl_principal):
  try:
    topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    admin_client.create_topics(new_topics=topic_list)
    print(f"Topic {topic_name} created successfully.")
  except TopicAlreadyExistsError:
    print(f"Topic {topic_name} already exists.")

  
  acl_resource = ResourcePattern(ResourceType.TOPIC, topic_name)
  acl_entry = ACL(principal=f"User:{acl_principal}", host="*", operation=ACLOperation.ALL, permission_type=ACLPermissionType.ALLOW, resource_pattern=acl_resource)

  admin_client.create_acls([acl_entry])
  print(f"ACL added for topic {topic_name} for principal {acl_principal}.")

admin_client = KafkaAdminClient(
  bootstrap_servers=['localhost:9092'],
  client_id='admin-client',
  sasl_mechanism="PLAIN",
  sasl_plain_username="admin",
  sasl_plain_password="admin-secret",
  security_protocol="SASL_PLAINTEXT"
)

topic_name = "topic-with-acl-test1"
num_partitions = 1
replication_factor = 1
acl_principal = "admin"

create_topic_with_acls(admin_client, topic_name, num_partitions, replication_factor, acl_principal)
