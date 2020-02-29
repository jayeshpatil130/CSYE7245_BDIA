from flask import Flask, request, jsonify, abort
import boto3
import tensorflow as tf
import json
from keras.models import load_model
import h5py
import tensorflow_hub as hub
import keras

# import tensorflow_datasets as tfds
BUCKET_NAME = 'team2bdia'
MODEL_FILE_NAME = 'model.h5'

app = Flask(__name__)

ACCESS_KEY = ''
SECRET_KEY = ''
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


@app.route('/predict', methods=['POST'])
def index():
    body_dict = request.get_json(silent=True)
    data = body_dict['data']

    prediction = predict(data)

    result = {'prediction': prediction}
    return json.dumps(result)


@memoize
def load_model(key):
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    model_str = response['Body'].read()

    #model = pickle.loads(model_str)

    return model_str


def predict(data):
    model = tf.keras.models.load_model(MODEL_FILE_NAME, custom_objects={'KerasLayer': hub.KerasLayer}, compile=True)

    return model.predict(data).tolist()


if __name__ == '__main__':
    # listen on all IPs
    app.run()
