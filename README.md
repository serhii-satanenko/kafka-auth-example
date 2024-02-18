docker-compose -f kafka-cluster-auth/my-kafka-m-zoo-sing-authorization.yml up -d 


kafka-ui localhost:8080
zoonavigator localhost:9000
endpoints ['localhost:9092', 'localhost:9093', 'localhost:9094']