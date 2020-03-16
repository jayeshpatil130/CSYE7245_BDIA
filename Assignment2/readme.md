## ML Pipeline to train and deploy sentiment analysis model as a service
How to train and deploy a machine learning pipeline in production.

## Report

https://codelabs-preview.appspot.com/?file_id=1WNt8YYhNIGRSNJVnYj8dVWI6AlLNzXr-WEkgTjDtDdM#1

## Prerequisites
Things you need to install:

Python3.5+\
AWS EC2, S3\
IBM Watson Natural Language understanding api 
https://cloud.ibm.com/apidocs/natural-language-understanding/natural-language-understanding \
Docker\
Postman\
Apache Airflow

## Setup For Running this Project:
#### Step 1
Clone this repo and edit the code with your AWS Credentials and your s3 bucket path and then setup the Apache Airflow

#### Step 2
Run the annotation pipeline and training pipeline in Apache Airflow, you will have the h5 model saved in your bucket.

#### Step 3
Build a Docker Image, create a Docker Container and run the container. If everything is working properly, you should be able to send HTTP POST requests to http://localhost:5000/predict and get results back from the model!

You can test this using Postman.

## Collaborators
<b>[Sharvari Karnik](https://www.linkedin.com/in/sharvarikarnik25/)</b> 

<b>[Kunal Jaiswal](https://www.linkedin.com/in/kunaljaiswal4393/)</b> 

<b>[Jayesh Patil](https://www.linkedin.com/in/jayeshpatil130/)</b> 
