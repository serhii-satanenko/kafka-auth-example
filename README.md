cd kafka-cluster-auth
docker-compose -f my-kafka-m-zoo-sing-authorization.yml up -d 

# first run 

python3 acl2.py

python3 consumer/consumer-auth.py

python3 producer/producer-auth.py

python3 tester.py


kafka-ui localhost:8080
zoonavigator localhost:9000
endpoints ['localhost:9092', 'localhost:9093', 'localhost:9094']