
###################################
# ETL WORKFLOWS AS DATA PIPELINES #
###################################

"""
To boost efficiency, data is fed through a data pipeline in smaller packets. While one packet
is being extracted, an earlier packet is being transformed, and another is being loaded. In this way,
data can keep moving through the workflow without interruption. By the time the third packet is
ingested, all three ETL processes are running simultaneously on different packets .
"""

#########################
# ETL WORKFLOWS AS DAGs #
#########################

"""
Airflow represents your workflow as a Directed Acyclic Graph (DAG). Airflow tasks can be expressed 
using predefined templates, called operators. 

Popular operators include Bash operators, for running Bash code, and Python operators for running 
Python code, which makes them extremely versatile for deploying ETL pipelines and many other kinds 
of workflows into production. 
"""

#############################
# ETL USING SHELL SCRIPTING #
#############################

# extracting data using 'cut' command
echo "database" | cut -c1-4  # shows first four chars - "data"

echo "database" | cut -c5-8  # shows chars 5-8 - "base"

echo "database" | cut -c1,5  # shows 1st and 5th chars - "db"

"""
We can extract a specific column/field from a delimited text file, by mentioning:
    - the delimiter using the -d option, or
    - the field number using the -f option.
    
The /etc/passwd is a ":" delimited file.
"""

# extracts user names (the first field) from /etc/passwd
cut -d":" -f1 /etc/passwd

# extracts multiple fields 1st, 3rd, and 6th (username, userid, and home directory) from /etc/passwd
cut -d":" -f1,3,6 /etc/passwd

# extracts a range of fields 3rd to 6th (userid, groupid, user desc. & home dir.) from /etc/passwd
cut -d":" -f3-6 /etc/passwd

"""
'tr' is a filter command used to translate, squeeze, and/or delete characters.
"""

# translates all lower case alphabets to upper case
echo "Shell Scripting" | tr "[a-z]" "[A-Z]"

# can also use the pre-defined character sets also for this purpose
echo "Shell Scripting" | tr "[:lower:]" "[:upper:]"

# translates all upper case alphabets to lower case
echo "Shell Scripting" | tr  "[A-Z]" "[a-z]"

"""
The -s option replaces a sequence of a repeated characters with a single occurrence of that character.
"""

# replaces repeat occurrences of 'space' in the output of ps command with one 'space'
ps | tr -s " "  # space char w/i quotes can be replaced with: "[:space:]"

"""
We can delete specified characters using the -d option.
"""

# deletes all digits
echo "My login pin is 5634" | tr -d "[:digit:]"  # outputs: 'My login pin is'

####################################
# FULL CODE OF ETL VIA SHELL SCRIPT:
####################################

# on terminal run command to start PostgreSQL db
start_postgres

# run thw following to login to postgres
psql --username=postgres --host=localhost

# psql gives 'postgres=#' promt, to connect run
\c template1

# create table
create table users(username varchar(50),userid int,homedirectory varchar(100));

# noq quit psql client to return to Linux shell
\q

# now create shell script from File -> New File and give name as 'csv2db.sh'

# extract required user information from /etc/passwd
#inside shell:
    # This script
    # Extracts data from /etc/passwd file into a CSV file.

    # The csv data file contains the user name, user id and
    # home directory of each user account defined in /etc/passwd

    # Transforms the text delimiter from ":" to ",".
    # Loads the data from the CSV file into a table in PostgreSQL database.
    # Extract phase

    echo "Extracting data"

    # Extract the columns 1 (user name), 2 (user id) and
    # 6 (home directory path) from /etc/passwd

    cut -d":" -f1,3,6 /etc/passwd

# run script with
bash csv2db.sh

# REDIRECT THE EXTRACTED OUTPUT INTO A FILE #

# replace the cut command at end of the script with the following command
cut -d":" -f1,3,6 /etc/passwd > extracted-data.txt

# run
bash csv2db.sh

# run to verify that the file extracted-data.txt is created & has the content
cat extracted-data.txt

# TRANSFORM DATA INTO CSV FORMAT #

"""
The extracted columns are separated by the original ":" delimiter.

We need to convert this into a "," delimited file.
"""

# add the below lines at the end of the script:
# inside shell:
    # Transform phase
    echo "Transforming data"
    # read the extracted data and replace the colons with commas.

    tr ":" "," < extracted-data.txt

# save, run

# verify that the output contains ',' in place of ":"
# replace the tr command at end of the script with the command below
tr ":" "," < extracted-data.txt > transformed-data.csv

# save, run

# run to verify that the file transformed-data.csv is created, and has the content
cat transformed-data.csv

# LOAD THE DATA INTO THE TABLE 'users' IN PSQL #

# the basic structure of the command which we will use in our script is:
COPY table_name FROM 'filename' DELIMITERS 'delimiter_character' FORMAT;

# add to shell script:
    # Load phase
    echo "Loading data"
    # Send the instructions to connect to 'template1' and
    # copy the file to the table 'users' through command pipeline.

    echo "\c template1;\COPY users  FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV;" | psql --username=postgres --host=localhost

# save, run

# run the command below to verify that the table users is populated with the data
echo '\c template1; \\SELECT * from users;' | psql --username=postgres --host=localhost

##################################
# INTRODUCTION TO DATA PIPELINES #
##################################

"""
A pipeline is:
    - a series of connected processes
    - output of one process is input of the next
    
Purpose of pipelines is to mvoe data from one place or form to another

Pipeline can be visualised as packets of data forming a queue to move through the data pipeline
where the length of the pipeline represents the latency (how long packets traverse) and the arrows
represent throughput delay (time between successive packet arrivals).

Data pipelines performance can be limited by latency and throughput:
    - Latency: the sum of the individual latencies (time spent of each 
    processing stage), this means pipelines are limited by the slowest processing stage.
    - Throughput: how much data can be fed through the pipe per unit of time (larger packets per
    time unit equals greater throughput
"""

###############################
# KEY DATA PIPELINE PROCESSES #
###############################

"""
Data Pipeline processes:
    - Extraction
    - Ingestion
    - Transformation
    - Loading
    - Scheduling/Triggering
    - Monitoring
    - Maintenance & Optimization
    
Key monitoring consideration:
    - Latency
    - Throughput
    - Warnings, errors, failures
    - Utilization Rate
    - Logging & alerting system

Load Balanced Pipelines:
    - just-in-time data packet relays
    - no upstream data flow bottlenecks
    - uniform packet throughput for each stage
    
Handling unbalanced loads:
    - if the process that is bottleneck the pipeline can be parallelized, then we can reduce
    overall latency
    - to parallelize we can replicate processes on multiple CPUs/cores/threads, the data packets are
    then distributed across these channels (these are called 'dynamic' or 'non-linear' pipelines)

Stage Synchronization:
    - I/O buffers: a holding are for data between processing stages, this can regulate the flow of 
    data to smooth out and improve throughput 
"""

##############################################
# BATCH VS STREAMING DATA PIPELINE USE CASES #
##############################################

"""
Batch Data Pipelines:
    - operate on batches of data
    - run periodically
    - can be initiated based on data size or other triggers
    - used when latest data is not needed
    - typical choice when accuracy is critical
    
Streaming Data Pipelines:
    - ingest data packets in rapid succession
    - for real-time results
    - records/events processed as they happen
    - event streams can be loaded to storage to build a history for later use
    - users publish/subscribe to event streams
    
Micro-Batch Data Pipelines:
    - smaller batches of data leads to faster processing which simulate real-time processing
    - smaller batches improve load balancing and low latency
    - useful when short windows of data are required
    
Batch vs Stream:
    - tradeoff b/w accuracy & latency
    - data cleaning improves quality but increased latency
    - lowering latency increase potential for errors
    
Lambda Architecture: 
    - is a hybrid between batch and streaming, used for dealing with Big Data. Historical
    data is sent to a 'batch layer' while real-time data is sent to the 'speed layer' - these two layers
    are then sent to the 'serving layer'
    - data stream ills in latency gap
    - used when data window is need but speed is critical
    - drawback is logical complexity
    - only use when accuracy and speed are required
    
Batch Data Pipeline use cases:
    - data backups
    - transaction history loading
    - billing and order processing
    - data modelling
    - forecasting sales or weather
    - retrospective data analysis
    - diagnostic medical image processing
    
Streaming Data Pipeline use cases:
    - media streaming
    - social medial feeds
    - fraud detection
    - user behaviour/advertising
    - stock market trading
    - real-time product pricing
    - recommender systems
"""

######################################
# DATA PIPELINE TOOLS & TECHNOLOGIES #
######################################

"""
Features of enterprise grade pipeline tools:
    - automation
    - ETL rule recommendations
    - GUI with 'no-code' (drag-and-drop)
    - assistance with complex calculations
    - security and compliance (encryption with HIPAA/GDPR)
    
Open Source Pipeline Tools:
    - Python Pandas: versatile, uses data frames, doesnt scale with Big Data
    - Airflow: scales to Big Data, integrates with cloud platforms
    - Talend: supports Big Data, warehousing and profiling, includes collaboration/monitoring/scheduling,
    drag-and-drop GUI, automatically generates Java, integrates with many data warehouses
    - AWS Glue: ETL service that simplified data prep for analytics, suggests schemas for storing data,
    create ETL jobs form the AWM console
    Panoply: ELT specific, no-code data integration, SQL-based view creation, emphasis shifts from
    data pipeline development to data analytics, integrates with dashboard and BI tools
    - Alteryx: self-service data analytics, drag-and-drop GUI,no SQL or coding to create pipelines
    - IBM Infosphere DataStage: tools for designing/developing and running ETL/ELT, it is the data
    integration component of IBM Infosphere Information Server, drag-and-drop GUI
    - IBM Streams: build real-time analytical applications (using SQL, Java, Python, C++), combine
    data in motion and at rest to deliver intelligence in real time, achieve end-to-end processing 
    with sub-millisecond latency
"""
