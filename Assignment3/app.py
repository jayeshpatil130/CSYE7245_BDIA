from flask import Flask, request, jsonify, abort
import json
import pandas as pd
import sdgym
#from sdgym import load_dataset, evaluate
from sdgym.synthesizers import IndependentSynthesizer, CLBNSynthesizer, IdentitySynthesizer, MedganSynthesizer, PrivBNSynthesizer, TableganSynthesizer, TVAESynthesizer,  UniformSynthesizer, VEEGANSynthesizer
from sdgym.evaluate import evaluate
from sdgym.data import load_dataset
#BUCKET_NAME = 'team2bdia'
#MODEL_FILE_NAME = 'model.h5'
from flask import Flask

app = Flask(_name_)

ACCESS_KEY = ''
SECRET_KEY = ''
#s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


@app.route('/sdgym', methods=['POST'])
def index():
    body_dict = request.get_json(silent=True)
    link = body_dict['link']
    synthesizer = body_dict['synthesizer']
    task = body_dict['task']
    final_result = predict(link, synthesizer, task)
	if task == "Data Synthesis":
	#final_result = numpy.ndarray
		np.savetxt('test.txt', final_result, delimiter=',')
	elif task == "Benchmark":
	#final_result = dataframe
		df = pd.DataFrame(final_result)
		df.to_csv('benchmark.csv', index = False)
    # result = {'prediction': prediction}
    return "File Generated"


def predict(link, synthesizer, task_done):
    if link:
        if synthesizer == 'IndependentSynthesizer':
            if task_done == 'Benchmark':
                result = independent_benchmark()
            if task_done == 'Data Synthesis':
                result = independent_synthesis()
        if synthesizer == 'CLBNSynthesizer':
            if task_done == 'Benchmark':
                result = clbn_benchmark()
            if task_done == 'Data Synthesis':
                result = clbn_synthesis()
        if synthesizer == 'IdentitySynthesizer':
            if task_done == 'Benchmark':
                result = identity_benchmark()
            if task_done == 'Data Synthesis':
                result = identity_synthesis()
        if synthesizer == 'UniformSynthesizer':
            if task_done == 'Benchmark':
                result = uniform_benchmark()
            if task_done == 'Data Synthesis':
                result = uniform_synthesis()
        return result

def independent_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = IndependentSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    #st.dataframe(scores)
    return scores

def independent_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = IndependentSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    return sampled

def clbn_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = CLBNSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    #st.dataframe(scores)
    return scores

def clbn_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = CLBNSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    return sampled

def identity_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = IdentitySynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    #st.dataframe(scores)
    return scores

def identity_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = IdentitySynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    return sampled
	
def uniform_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = UniformSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    #st.dataframe(scores)
    return scores

def uniform_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = UniformSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    return sampled
	

if _name_ == '_main_':
    # listen on all IPs
    app.run()