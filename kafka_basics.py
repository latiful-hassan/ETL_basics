
###################################################
# DISTRIBUTED EVENT STREAMING PLATFORM COMPONENTS #
###################################################

"""
Events: describe an entity's observable state updates over time:
    - GPS, temperature, blood pressure, RAM usage

Common Event Formats:
    - Primitive: "Hello"
    - Key-value pair
    - Key-value pair with timestamp

Event Streaming:
    - is the constant feed of data from event sources that produce large amounts of data to the
    event destination

Event Streaming Platform (ESP):
    - if we are dealing with multiple event sources and destinations (all with different communication
    protocols) we implement ESP
    - ESP: acts as a middle-layer and provides a unified interface for event-based ETL
    - this means event sources 'send' to ESP and event destinations 'subscribe' to ESP and then
    'consume' the events sent from ESP rather than individual sources

Components of ESP:
    - Event Broker: Ingester -> Processor -> Comsumption
    - Event Storage
    - Analytic & Query Engine

Event Broker:
    - Ingester receives events from multiple sources
    - Processor performs operations on data (de/serialise, de/compression, de/encryption etc.)
    - Consumption retrieves events from event storage and distributes them to subscribed event
    destinations

Popular ESPs:
    - Apache Kafka, Amazon Kinesis, Apache Spark, Apache Flink, Apache Storm
"""

#########################
# APACHE KAFKA OVERVIEW #
#########################

"""
Common Use Cases:
    - user activities, metrics, logs, financial transactions
    - subscriptions: databases, real-time analytics, notifications, governance & auditing
    
Kakfa Architecture:
    - Distributed Servers: multiple event brokers which are managed by Apache ZooKeeper
    - Network Protocol: kakfa uses TCP (transmission control protocol) to exchange data between
    clients and servers
    - Distributed Clients: kafka CLI, high-level programming APIs
    
Main Features of Kafka:
    - distribution system
    - scalable (multiple brokers, event streaming in parallel)
    - reliable (multiple partitions)
    - permanent persistence (stores permanently)
    - open source
    
Event streaming as a service:
    - kakfa clusters are difficult to set up, the following provide a service for this:
        - Confluent Cloud, IBM Event Streams, Amazon MSK
"""

##################################################
# BUILDING EVENT STREAMING PIPELINES USING KAFKA #
##################################################

"""
Kafka utilises many brokers. These brokers can be seen as dedicated server, to receive, store and 
process events. These brokers are then managed by Apache Zookeeper.

The individual brokers contain 'topics' which store the event data e.g. trans_topic will contain
transaction data. The brokers save the events into topics which are distributed to subscribed consumers.

Kafka uses partition and replications to improve fault tolerance as well as  enable is to run
multiple brokers in parallel. For example, a log_topic will be partitioned twice and then both 
partitions are replicated.

Kafka CLI is used to build ESP pipeline, kafka topics script is used to manage topics in a 
kafka cluster.
"""

# create topic
kafka-topics --bootstrap-server localhost:9092 --topic log_topic --create

# list topics
--list

# topic details
--describe log_topic

# delete topic
--topic logtopic --delete

"""
Kafka Producers:
    - client applications that publish events to topic partition
    - an event can be optionally associated with a key
    - events associated with the same key will be published to the same topic partition
    - events not associated with any key will be published to topic partitions in rotation
"""

# start producer to a topic without keys
kafka-console-producer --broker-list localhost:9092 --topic log_topic # producer points to topic

# with keys
--property parse.key=true -property key.separator=,

"""
Kafka Consumers:
    - consumers are clients subscribed to topics
    - consumer data in same order of published events
    - store an offset record for each partition
    - offset consumers can read events as they occur
    - offset can be reset to zero to read all events from the beginning again
    - producers and consumers are de-coupled so subscribers can consume when needed
"""

# read new events from log_topic, offset 1 (consumer reads from offset 2)
kafka-console-consumer --bootstrap-server localhost:9092 --topic log_topic

# offset 0
kafka-console-consumer --bootstrap-server localhost:9092 --topic log_topic
--from-beginning

"""
Weather Pipeline Example:
weather events -> weather producer -> weather topic -> weather consumer -> DB writer -> RDBMS -> Dashboard 
"""

###########################
# KAFKA STREAMING PROCESS #
###########################

"""
Ad hoc weather stream processing:
data -> producer1 -> raw data topic -> consumer1 -> data processor -> producer2 -> processed data topic
-> consumer2 -> dashboard

Kafka Streams API:
    - simple client library to facilitate data processing in event streaming pipelines
    - processes & analyses data stored in kafka topics
    - record only processed once
    - processing one record at a time
    
Using Kafka Streams API instead of ad hoc:
data -> producer1 -> raw data topic -> consumer1 -> 
source processor -> stream processor (filter) -> sink processor
-> producer2 -> processed data topic -> consumer2 -> dashboard
"""

###########################################
# WORKING WITH STREAMING DATA USING KAFKA #
###########################################

# install kafka
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz

# extract kafka
tar -xzf kafka_2.12-2.8.0.tgz

# start ZooKeeper server
cd kafka_2.12-2.8.0
bin/zookeeper-server-start.sh config/zookeeper.properties

# start Kafka message broker service
cd kafka_2.12-2.8.0
bin/kafka-server-start.sh config/server.properties

# create topic
cd kafka_2.12-2.8.0
bin/kafka-topics.sh --create --topic news --bootstrap-server localhost:9092

# start producer
bin/kafka-console-producer.sh --topic news --bootstrap-server localhost:9092

# run command to list to messages in the topic news
cd kafka_2.12-2.8.0
bin/kafka-console-consumer.sh --topic news --from-beginning --bootstrap-server localhost:9092

# delete kafka installation
rm kafka_2.12-2.8.0.tgz
