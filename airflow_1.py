
##############
# ETL vs ELT #
##############

"""
ETL is rigid as piplines are engineered to user spec., but ELT is flexible
in that the end user is able to build their own transformations.

ETL handle structured relational data, but ELT solves the issue of
scalability - being able to hand un/structured data (Big Data).

ELT addresses the following ETL issues:
    - lengthy time-to-insight
    - Big Data
    - demand for siloed information (info. not avail. to everyone)
"""

##############################
# DATA EXTRACTION TECHNIQUES #
##############################

"""
Data Extraction Techniques:
    - OCR: Optical Character Recognition, used to interpret and digitise
        data scanned from paper documents
    - ADC: Analog to Digital Converters, used to digitise analog recordings
    - Polling or Census Data
    - Cookies or User Logs
    - Web Scraping
    - APIs
    - Database Querying
    - Edge Computing
    - Biomedical Devices
    
Use Cases:
    - integrating disparate structured data sources via APIs
    - capturing events via APIs and recording them in history
    - monitoring with edge computing
    - data migration for further processing
    - diagnosing health problems with medical devices
"""

##################################
# DATA TRANSFORMATION TECHNIQUES #
##################################

"""
Data Transforming involves formatting the data to suit the end users needs.

Data Transformations can include operations such as:
    - Data Typing: casting data to appropriate types
    - Data Structuring: converting one format to another 
    - Anonymising/Encrypting: ensures privacy and security
    - Cleaning: remove duplicates/missing values
    - Normalising: converting data to common units
    - Filtering, sorting, aggregating and binning
    - Merging disparate data sources
    
Schema-on-write: 
    - applies to ETL where data conforms to a defined schema before loading (relational database)
    - consistent and efficient
    - limited versatility
Schema-on-read: 
    - applies to ELT, where scheme is applied to the raw data
    after loading
    - more versatile
    - more storage flexibility
                
Information Loss:
    - in ETL the lost data is not recoverable
    - in ELT the raw data can be readily accessed
                
Examples of data loss:
    - lossy compression
    - filtering
    - aggregation
    - edge computing devices
"""

###########################
# DATA LOADING TECHNIQUES #
###########################

"""
Data Loading techniques:
    - Full/Incremental
    - Scheduled/On-demand
    - Batch/Stream
    - Push/Pull
    - Parallel/Serial
    
Full:
    - load data in one large batch
    - used to start tracking transaction in a new data warehouse
    - used for porting over transaction history
    
Incremental:
    - data is appended to, not overwritten
    - used for accumulating transaction history
    - depends on the volume and velocity of data, can be batch/stream
    
Scheduled:
    - periodic loading such as daily transaction
    - windows task scheduler, cron

On-demand:
    - triggered by measures such as size, event detection (motion, sound etc), or user requests 
    (video/music streaming)
    
Batch:
    - loads data in chunks defined by time
    
Micro-Batch:
    - short time windows used to access older data
    
Stream:
    - continuous updates as data arrives

Push:
    - server pushes data to client (push notifications, instant messaging services)

Pull:
    - requests data from a server (RSS feeds, email)
    
Parallel:
    - can be employed on multiple data streams (useful for large amounts of data)
    
Series:
    - file partitioning, source split into smaller chunks then sent to destination
"""
