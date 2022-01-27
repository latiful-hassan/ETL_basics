
#######################
# KAFKA PYTHON CLIENT #
#######################

"""
'kafka-python' is a Python client for Apache Kafka which allows you to interact with your Kafka
server - managing topics, publish and consume messages in Python.
"""

# istall kafka-python in terminal
pip install kafka-python

"""
The 'KafkaAdminClient is a class that allows for fundamental administrative management operations
on a kafka server - creating/deleting topics, retrieving and updating topic configurations etc.
"""

####################
# CREATE NEW TOPIC #
####################

# create KafkaAdminClient object
# bootstrap argument specifies host/IP
# client_id specified id of current client
admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='test')

# to create a new topic, define an empty list
topic_list = []

# use NewTopic class to create a topic
new_topic = NewTopic(name="bankbranch", num_partitions= 2, replication_factor=1)
topic_list.append(new_topic)

# use create_topics(...) method to create new topics
# equivalent to using  kafka-topics.sh --topic in Kafka CLI
admin_client.create_topics(new_topics=topic_list)

####################
# DESCRIBE A TOPIC #
####################

# once new topics are created, we can check configuration details using 'describe_configs()' method
# equivalent to using kafka-topics.sh --describe in Kafka CLI
config_resources = [ConfigResource(ConfigResourceType.TOPIC, "bankbranch")])

##################
# KAFKA PRODUCER #
##################

"""
Since we have the 'bankbranch' example topic created we can use KafkaProducer class to produce 
messages. Below is using JSON format.
"""

# define and create KafkaProducer
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

"""
Since Kafka produces and consumes messages in raw bytes, we need to encode our JSON messages and 
serialize them into bytes.

For the value_serializer argument, we define a lambda function to take a Python dict/list object 
and serialize it into bytes.

Then, with the KafkaProducer created, we can use it to produce two ATM transaction messages in 
JSON format as follows:
"""

# equivalent to using  kafka-console-producer.sh --topic
producer.send("bankbranch", {'atmid':1, 'transid':100})
producer.send("bankbranch", {'atmid':2, 'transid':101})

"""
The first argument specifies the topic bankbranch to be sent, and the second argument represents the message value in a
Python dict format and will be serialized into bytes.
"""

##################
# KAFKA CONSUMER #
##################

"""
We published two JSON messages, now we can use the KafkaConsumer class to consume them.
"""

# define and create a KafkaConsumer subscribing to the topic bankbranch
consumer = KafkaConsumer('bankbranch')

"""
Once the consumer is created, it will receive all available messages from the topic bankbranch.
"""

# we can iterate and print the messages#
# equivalent to using kafka-console-consumer.sh --topic in Kafka CLI
for msg in consumer:
    print(msg.value.decode("utf-8"))
