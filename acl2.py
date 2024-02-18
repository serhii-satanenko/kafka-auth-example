from kafka.admin import KafkaAdminClient, NewTopic, ACL, ResourcePattern, ResourceType, ACLOperation, ACLPermissionType
from kafka.errors import TopicAlreadyExistsError

# connection
bootstraps = ['localhost:9092', 'localhost:9093', 'localhost:9094']
admin_user = "admin"; admin_secret = "admin-secret"
admin_client = KafkaAdminClient(
  bootstrap_servers=bootstraps, client_id='admin-client', sasl_mechanism="PLAIN",
  sasl_plain_username=admin_user, sasl_plain_password=admin_secret, security_protocol="SASL_PLAINTEXT"
)

# users & ACL
topic_name = "massages2"; num_partitions = 1; replication_factor = 1
acls = [
  {"user":"client", "permission_type": "ALLOW", "operation": "READ", "host": "*"},
  {"user":"client", "permission_type": "DENY", "operation": "WRITE", "host": "*"},
  {"user":"produser", "permission_type": "DENY", "operation": "READ", "host": "*"},
  {"user":"produser", "permission_type": "ALLOW", "operation": "WRITE", "host": "*"},
  {"user":"admin", "permission_type": "ALLOW", "operation": "ALL", "host": "*"},
]

def topic_acl(TOPIC_NAME, ACL_PRINCIPAL, HOST, OPERATION_TYPE, PERMISION):
  acl_resource = ResourcePattern(ResourceType.TOPIC, TOPIC_NAME)
  if PERMISION == "ALLOW":
    if OPERATION_TYPE == "ALL": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.ALL, permission_type=ACLPermissionType.ALLOW, resource_pattern=acl_resource)
    elif OPERATION_TYPE == "READ": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.READ, permission_type=ACLPermissionType.ALLOW, resource_pattern=acl_resource)
    elif OPERATION_TYPE == "WRITE": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.WRITE, permission_type=ACLPermissionType.ALLOW, resource_pattern=acl_resource)
    elif OPERATION_TYPE == "DESCRIBE": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.DESCRIBE, permission_type=ACLPermissionType.ALLOW, resource_pattern=acl_resource)
  elif PERMISION == "DENY":
    if OPERATION_TYPE == "ALL": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.ALL, permission_type=ACLPermissionType.DENY, resource_pattern=acl_resource)
    elif OPERATION_TYPE == "READ": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.READ, permission_type=ACLPermissionType.DENY, resource_pattern=acl_resource)
    elif OPERATION_TYPE == "WRITE": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.WRITE, permission_type=ACLPermissionType.DENY, resource_pattern=acl_resource)
    elif OPERATION_TYPE == "DESCRIBE": acl_entry = ACL(principal=f"User:{ACL_PRINCIPAL}", host=HOST, operation=ACLOperation.DESCRIBE, permission_type=ACLPermissionType.DENY, resource_pattern=acl_resource)
  
  admin_client.create_acls([acl_entry])
  print(f"ACL added for topic {topic_name} for principal {ACL_PRINCIPAL}.")


def create_topic_with_acls(admin_client, topic_name, num_partitions, replication_factor, acls):
  try:
    topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    admin_client.create_topics(new_topics=topic_list)
    print(f"Topic {topic_name} created successfully.")
  except TopicAlreadyExistsError:
    print(f"Topic {topic_name} already exists.")
  
  for acl in acls:
    topic_acl(topic_name, acl['user'], acl['host'], acl['operation'], acl['permission_type'])

create_topic_with_acls(admin_client, topic_name, num_partitions, replication_factor, acls)