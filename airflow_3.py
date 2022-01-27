###########################
# APACHE AIRFLOW OVERVIEW #
###########################

"""
Apache Airflow:
    - open-source
    - Airflow lets you build and run workflows
    - workflow is represented as a DAG (directed acyclic graph)

Airflow's Architecture:
    - 'Scheduler' handles triggering of scheduled workflows, submits individual tasks to the
    'Executor' which itself handles the running of the tasks by assigning them to 'Workers'
    - 'Web Server' servers Airflow's 'User Interface' from the UI you can inspect, trigger and debug the
    DAGs from the 'DAG Directory'
    - 'Metadata Database' stores the state of each DAG and its tasks which can be accessed by the
    Scheduler, Executor and Web Server

Sample DAG:

Ingest -> Analyse -> Check_Integrity -> (error found) Describe_Integrity -> Email_Error -> Report
                                     -> (no errors) Save -> Report

Apache Airflow Features:
    - pure Python = flexibility
    - useful UI = full insight
    - integration = plug and play
    - easy to use = unlimited pipeline scope
    - open source = community of developers

Airflow Principles:
    - scalable: modular and has arbitrary number of workers
    - dynamic: pipelines defined in Python and can handle multiple simultaneous tasks
    - extensible: define your own operators
    - lean: explicit, parametrisation is built into core using Jinja templating engine

Airflow Use Cases (company examples given):
    - define and organise ML pipeline dependencies (sift)
    - increase visibility of batch processes and decoupling them (seniorlink)
    - deploying as an enterprise scheduling tool (experity)
    - orchestrating SQL transformations in data warehouses (onefootball)
"""

#########################################################
# ADVANTAGES OF USING DATA PIPELINES AS DAGs IN AIRFLOW #
#########################################################

"""
- Directed Acyclic Graph (DAG) is a graph where the edges have direction but no loops (acyclic)
- The nodes in DAGs are tasks and the edges are the dependencies
- Edges fine the order in which the tasks run
- DAGs are defined in Python script
- Tasks implement 'operators', eg.g Python, SQL or Bash operators
- Operators determine what a task does
- 'Sensor' operator poll for a certain time or condition, there are also email and HTTP request operators
"""

"""
Airflow DAG consists of the following logical blocks:
    - library imports
    - DAG arguments
    - DAG definition
    - task definitions
    - task pipeline
"""

#################################
# DAG DEFINITION SCRIPT EXAMPLE #
#################################

# library imports
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import datetime as dt

# DAG arguments
default_args = {
    'owner': 'me',  # name of dag
    'start_date': dt.datetime(2021, 7, 28),  # start time for task
    'retries': 1,  # how many times to retry if failed
    'retry_delay': dt.timedelta(minutes=5)  # time between failure and retry
}

# DAG definition (instantiating)
dag = DAG('simple_example',
          description = 'A simple example DAG'
          default_args = default_args,
          schedule_interval = dt.timedelta(seconds=5),
)

# task definitions
task1 = BashOperator(
    task_id = 'print_hello',
    bash_command = 'echo' \'Greetings. The date and time are \'',
    dag = dag,
)

task2 = BashOperator(
    task_id = 'print_date',
    bash_command = 'date',
    dag = dag,
)

# task pipeline (setting up dependency)
task1 >> task2

"""
'Airflow Scheduler' deploys the scripted DAG:
    - deploys on worker array
    - follows specified DAG
    - DAG runs on the start date specified
    - subsequent runs depend on specified dates
    
Advantages of workflows as code:
    - maintainable
    - version control
    - collaborative
    - testable
"""

#####################
# APACHE AIRFLOW UI #
#####################

"""
- You can visualise DAG in graph or tree mode'
- You can review Python code for DAG
- You can analyse individual task duration timelines
- You can select content metadata for any task instance
"""

#######################################
# GETTING STARTED WITH APACHE AIRFLOW #
#######################################

# list all DAGs
airflow dags list

# list tasks in a DAG
airflow task list example_bash_operator  # lists the DAG named 'example_bash_operator'

# command to unpause/pause DAG named 'tutorial'
airflow dags unpause tutorial
airflow dags pause tutorial

###################################
# CREATE A DAG FOR APACHE AIRFLOW #
###################################

"""
Below is some example code for creating a DAG.
"""

# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Ramesh Sannareddy',
    'start_date': days_ago(0),
    'email': ['ramesh@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='sample-etl-dag',
    default_args=default_args,
    description='Sample ETL DAG using Bash',
    schedule_interval=timedelta(days=1),
)

# define the tasks
# define the first task named extract
extract = BashOperator(
    task_id='extract',
    bash_command='echo "extract"',
    dag=dag,
)


# define the second task named transform
transform = BashOperator(
    task_id='transform',
    bash_command='echo "transform"',
    dag=dag,
)

# define the third task named load
load = BashOperator(
    task_id='load',
    bash_command='echo "load"',
    dag=dag,
)

# task pipeline
extract >> transform >> load

"""
To then submit a DAG we copt the Python file with the DAG code in it to the Airflow Home directory.
"""

# in the terminal run
cp my_first_dag.py $AIRFLOW_HOME/dags

# verify DAG submission
airflow dags list

# verify the DAG is part of the output
airflow dags list | grep "my-first-dag"

# run to list all tasks in DAG
airflow tasks list my-first-dag

################################
# AIRFLOW MONITORING & LOGGING #
################################

"""
- logging is required to diagnose and debug issues
- airflow logs are saved to local log files or cloud storage/search engine/dashboard

default log file location:
    logs/dag_id/task_id/execution_date/try_number.log
    
Monitoring Metrics:
    - Counters: metrics always increase
        - total count of task instances failures/success
    - Gauges: metrics that fluctuate
        - number of running tasks
        - DAG bag size
    - Timers: metrics related to time duration
        - milliseconds to finish task
        - milliseconds to reach a success/failed state
        
Sorting & Analysing Metrics:
    - Airflow metrics -collect-> StatsD -send-> Prometheus -aggregate & visualise-> Dashboard
"""
