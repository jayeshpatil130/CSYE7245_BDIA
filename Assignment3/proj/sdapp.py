from __future__ import absolute_import
from .celery import app

import pandas as pd
import sdgym
import numpy as np
#from sdgym import load_dataset, evaluate

from sdgym.synthesizers import IndependentSynthesizer, CLBNSynthesizer, IdentitySynthesizer, MedganSynthesizer, PrivBNSynthesizer, TableganSynthesizer, TVAESynthesizer,  UniformSynthesizer, VEEGANSynthesizer
from sdgym.evaluate import evaluate
from sdgym.data import load_dataset


@app.task
def synt():

    df = pd.read_csv('input.csv')
    df.to_numpy
    jsonParse = '{ "columns": ['
    for (columnName, columnData) in df.iteritems():
        print('Column Name : ', columnName)
#    print('Column Contents : ', columnData.values)
        if (pd.to_numeric(df[columnName], errors='coerce').notnull().all()):
            print ('Numeric')
            jsonParse = jsonParse + '{"max": ' + str(columnData.max()) + ',' + '"min": ' + str(columnData.min()) + ',' + '"name": "' + columnName + '" , "type": "continuous"},'    
            print (columnData.max())
            print (columnData.min())
        
        else:
            print ('NonNumeric')
            jsonParse = jsonParse +  ' {"i2s": ['
            for i in columnData.unique():
                print (i)
                jsonParse = jsonParse + '"' + i + '",'
        
            jsonParse = jsonParse[:-1] + '],' + '"name": "' + columnName + '", "size": '  + str(len(columnData.unique())) + ' , "type": "categorical"},'


    jsonParse = jsonParse[:-1] + '], "problem_type": "binary_classification"}'
    final_dictionary = eval(jsonParse) 

    with open('metadata.json', 'w') as outfile:
        json.dump(final_dictionary, outfile)
    
    t_train = df[:-500]
    t_test = df[-500:]
    np.savez("metadata.npz", train=t_train, test=t_test)
    


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

