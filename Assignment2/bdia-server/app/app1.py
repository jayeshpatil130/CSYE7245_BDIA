





from flask import Flask, request, jsonify,abort
import boto3
import tensorflow as tf
import tensorflow_hub as hub
import keras
#import tensorflow_datasets as tfds

app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def create_task():
    if not request.json or not 'data' in request.json:
        return abort(400)

    sentences = request.json['data']
    output = dict()
    output["input"] = {"data": sentences}
    output["pred"] = []


    #model_h5_file = get_model_from_s3()
    checkpoint = load_model_on_keras()
    for s in sentences:
        result = predict(checkpoint,s)
        output["pred"].append([result])

    return jsonify(output), 201


def get_model_from_s3():
    ACCESS_KEY = ''
    SECRET_KEY = ''
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    model_h5_file = s3.download_file('team2bdia', 'model.h5', 'model.h5')
    return model_h5_file

def load_model_on_keras():
    checkpoint = tf.keras.models.load_model(r'C:\Users\kunal\Downloads\model.h5',
                                            custom_objects={'KerasLayer': hub.KerasLayer}, compile=True)
    #checkpoint = model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return checkpoint

def predict(checkpoint, sentence):
    metric_result = checkpoint.predict(sentence)
    #metric_result = metric_result.tolist()
    return metric_result

if __name__ == '__main__':
   app.run()