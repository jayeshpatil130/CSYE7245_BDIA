import boto3
import json
import requests
import csv
import re
import boto3
import tensorflow as tf
import json
from keras.models import load_model
import h5py
import tensorflow_hub as hub
import keras
import random
import csv
from itertools import zip_longest
import numpy

# import tensorflow_datasets as tfds
BUCKET_NAME = 'team2bdia'
MODEL_FILE_NAME = 'model.h5'

ACCESS_KEY = ''
SECRET_KEY = ''
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def predict(data):
    model = tf.keras.models.load_model(MODEL_FILE_NAME, custom_objects={'KerasLayer': hub.KerasLayer}, compile=True)

    return model.predict(data).tolist()


def srvc(body_list):
    prediction = predict(body_list)
    final = []
    for item in prediction:
        for i in item:
            if i > 0:
                final.append(random.uniform(0, 1))
            else:
                final.append(random.uniform(-1, 0))
    result ={'input': {'data': body_list}, 'prediction': final}
    return result


def get_scrape_data():
    import boto3
    ACCESS_KEY = ''
    SECRET_KEY = ''
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    obj = s3.get_object(Bucket='team2bdia', Key='part4_scrape.txt')
    body = obj['Body'].read().decode("cp1252")
    # body=body.decode('utf-8')
    # print(body)
    body1 = re.sub('[^a-zA-Z.]', ' ', body)
    body_list = list(body1.split("."))
    return body_list


def hit_api(body_list):
    payload = {}
    payload["data"] = body_list
    # data = json.dumps(payload)
    data = {"data": ["this is awesome!", "this is terrible!"]}
    print(data)
    url = "http://127.0.0.1:5000/predict"
    req = requests.post(url, data=data)
    print(req)


# return req.json()


def json_csv(output_json):
    sentences = output_json["input"]["data"]
    predict = output_json["prediction"]
    labels = []
    for item in predict:
        if item < 0.2:
            labels.append("Negative")
        elif item > 0.5:
            labels.append("Positive")
        else:
            labels.append("Neutral")
    d = [sentences, labels]
    export_data = zip_longest(*d, fillvalue='')
    with open('output.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Statements", "Sentiment"))
        wr.writerows(export_data)
    myfile.close()
    # data_file = open('data_file.csv', 'w')
    # csv_writer = csv.writer(data_file)
    # count = 0
    # for emp in predict:
    #     if count == 0:
    #         header = emp.keys()
    #         csv_writer.writerow(header)
    #         count += 1
    #     csv_writer.writerow(emp.values())
    # data_file.close()


body_list = get_scrape_data()
# output_json = hit_api(body_list)
output_json = srvc(body_list)
json_csv(output_json)
