## ML Pipeline to train and deploy sentiment analysis model as a Service
How to train and deploy a machine learning pipeline in production.

## Report

https://codelabs-preview.appspot.com/?file_id=1WNt8YYhNIGRSNJVnYj8dVWI6AlLNzXr-WEkgTjDtDdM#1

## Prerequisites
What things you need to install the software:

Python3.5+\
AWS EC2, S3\
IBM Watson Natural Language understanding api 
https://cloud.ibm.com/apidocs/natural-language-understanding/natural-language-understanding \
Docker\
Postman\
Apache Airflow

## Setup For Running this Project:
#### Step 1
Clone this repo and edit the code with your AWS Credentials and path to your s3 bucket and setup the Apache Airflow

#### Step 2
Run the annotation pipeline and training pipeline in Apache Airflow, you will have the h5 model saved in your bucket.

#### Step 3
Build a Docker Image and create and run the a Docker Container and if all is working properly, we should be able to send HTTP POST requests to http://localhost:5000/predict and get results back from our model!

You can test this using Postman.


