from __future__ import absolute_import
from .celery import app

import pandas as pd
import sdgym
import numpy as np
from google.cloud import storage
#from sdgym import load_dataset, evaluate

from sdgym.synthesizers import IndependentSynthesizer, CLBNSynthesizer, IdentitySynthesizer, MedganSynthesizer, PrivBNSynthesizer, TableganSynthesizer, TVAESynthesizer,  UniformSynthesizer, VEEGANSynthesizer
from sdgym.evaluate import evaluate
from sdgym.data import load_dataset

storage_client = storage.Client.from_service_account_json('/<path-to-credentials>/<appl_credentials>.json')

	# Define storage bucket with name
bucket = storage_client.get_bucket('datateam2')

@app.task
def synt():
	
    df = pd.read_csv("gs://datateam2/input.csv", dtype='str', header=-1)
    #df = df.apply(lambda x: x.str.strip(' \t.'))

    col_type = [
        ("gender", CATEGORICAL),
        ("race/ethnicity", ORDINAL, ["group A", "group B", "group B"]),
        ("parental level of education", CATEGORICAL),
        ("lunch", CATEGORICAL),
        ("test preparation course", CATEGORICAL),
        ("math score", CONTINUOUS),
        ("reading score", CONTINUOUS),
        ("writing score", CONTINUOUS)
    ]

    meta = []
    for id_, info in enumerate(col_type):
        if info[1] == CONTINUOUS:
            meta.append({
                "name": info[0],
                "type": info[1],
                "min": np.min(df.iloc[:, id_].values.astype('float')),
                "max": np.max(df.iloc[:, id_].values.astype('float'))
            })
        else:
            if info[1] == CATEGORICAL:
                value_count = list(dict(df.iloc[:, id_].value_counts()).items())
                value_count = sorted(value_count, key=lambda x: -x[1])
                mapper = list(map(lambda x: x[0], value_count))
            else:
                mapper = info[2]

            meta.append({
                "name": info[0],
                "type": info[1],
                "size": len(mapper),
                "i2s": mapper
            })


    tdata = project_table(df, meta)

    np.random.seed(0)
    np.random.shuffle(tdata)

    t_train = tdata[:-10000]
    t_test = tdata[-10000:]
	
	# Initialize a storage client
	storage_client = storage.Client.from_service_account_json('/<path-to-credentials>/<appl_credentials>.json')

	# Define storage bucket with name
	bucket = storage_client.get_bucket('datateam2')

    name = "student"
    with open("student.json", 'w') as f:
        blob = bucket.blob(json.dump(meta, f, sort_keys=True, indent=4, separators=(',', ': '))_
		blob.upload_from_filename('student.json', content_type='json')
	blob = bucket.blob(np.savez("student.npz"), train=t_train, test=t_test))
	blob = bucket.upload_from_filename(np.savez("student.npz"), train=t_train, test=t_test))
	return name, meta
    

@app.task
def independent_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = IndependentSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    return scores

@app.task
def independent_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = IndependentSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    print(sampled)
    np.savetxt('test.txt', sampled, delimiter=',') 
    return sampled

@app.task
def clbn_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = CLBNSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    return scores


@app.task
def clbn_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = CLBNSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    print(sampled)
    np.savetxt('test.txt', sampled, delimiter=',') 
    return sampled

@app.task
def identity_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = IdentitySynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    return scores


@app.task
def identity_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = IdentitySynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    print(sampled)
    np.savetxt('test.txt', sampled, delimiter=',') 
    return sampled


@app.task
def uniform_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = UniformSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    return scores


@app.task
def uniform_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = UniformSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    print(sampled)
    np.savetxt('test.txt', sampled, delimiter=',') 
    return sampled

@app.task
def call_benchmark():
    independent = independent_benchmark()
    clbn = clbn_benchmark()
    identity = identity_benchmark()
    uniform = uniform_benchmark()

   # arr=[max(independent["accuracy"]),2,3,4];

    arr=[max(independent["accuracy"]),max(clbn["accuracy"]),max(identity["accuracy"]),max(uniform["accuracy"])]
    max_val=max(arr)
    print('arr',arr)
    print('max_val',max_val)
    index_bench=arr.index(max_val)
    print(index_bench)
    if index_bench == 0:
        sample = independent_synthesis()
    if index_bench == 1:
        sample = clbn_synthesis()
    if index_bench == 2:
        sample = identity_synthesis()
    if index_bench == 3:
        sample = uniform_synthesis()

