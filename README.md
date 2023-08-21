# Spark-Master-REST-API

In this guide, we will walk you through the process of deploying Spark applications 
on a standalone cluster using a Python client. Apache Spark is a powerful open-source 
data processing and analytics engine that supports various cluster managers, and 
one of them is the standalone cluster manager. We will use the Spark documentation 
as a reference (https://spark.apache.org/docs/latest/cluster-overview.html) and 
build a Python client to submit Spark applications to a standalone cluster.

This library abstracts the process of interacting with the Spark master's REST API to 
submit applications.

## Prerequisites

Before you begin, ensure that you have the following prerequisites in place:

- `Apache Spark`: Install Apache Spark on your machine or cluster. You can download it from the official website:
                  https://spark.apache.org/downloads.html

- `Standalone Cluster Manager`: Set up a Spark standalone cluster. Refer to the Spark documentation for detailed 
                                instructions on cluster setup: https://spark.apache.org/docs/latest/spark-standalone.html

- `Python`: Make sure you have Python installed on your machine.

## Usage

This guide will walk you through the process of using a Python script to submit a remote JAR file to a 
Spark standalone cluster.

```commandline
pip install spark_master_rest_api
```
[PyPi](https://pypi.org/project/spark-master-rest-api/)

```python
from spark_master_rest_api import Client

# Initialize the client with Spark master's hostname and version
client = Client('spark-master.example.com', '3.2.1')

# Define Spark application submission parameters
app_resource = "hdfs:///jars/app.jar"
spark_properties = {
    "spark.master": "spark://spark-master.example.com:7077",
    "spark.submit.deployMode": "cluster",
}
main_class = "com.example.Main"
app_args = []

# Submit the Spark application
response, submit_result = client.submit(
    app_resource=app_resource,
    spark_properties=spark_properties,
    main_class=main_class,
    app_args=app_args,
)

# Print the submission result
print(submit_result.submission_id)
print(submit_result.success)
```
