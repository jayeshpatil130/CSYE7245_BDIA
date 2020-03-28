import streamlit as st
import pandas as pd
import sdgym
#from sdgym import load_dataset, evaluate

from sdgym.synthesizers import IndependentSynthesizer, CLBNSynthesizer, IdentitySynthesizer, MedganSynthesizer, PrivBNSynthesizer, TableganSynthesizer, TVAESynthesizer,  UniformSynthesizer, VEEGANSynthesizer
from sdgym.evaluate import evaluate
from sdgym.data import load_dataset


st.title("Assignment 3")

link = st.text_input('Enter the metadata link')
#json = st.text_input('Dataset')
synthesizer = st.text_input('Synthesizer to use')
task_done = st.text_input('Task to be done')


def independent_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = IndependentSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    st.dataframe(scores)


def independent_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = IndependentSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    sampled


def clbn_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = CLBNSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    st.dataframe(scores)


def clbn_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = CLBNSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    sampled


def identity_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = IdentitySynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    st.dataframe(scores)


def identity_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = IdentitySynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    sampled


def uniform_benchmark(json = 'adult'):
    train, test, meta, categoricals, ordinals = load_dataset(json, benchmark=True)
    synthesizer = UniformSynthesizer()
    synthesizer.fit(train, categoricals, ordinals)
    sampled = synthesizer.sample(300)
    print('Sampled Data for 300 records\n')
    scores = evaluate(train, test, sampled, meta)
    print('\nEvaluation Scores from evaluate function:\n')
    st.dataframe(scores)


def uniform_synthesis(json = 'adult'):
    data, categorical_columns, ordinal_columns = load_dataset(json)
    synthesizer = UniformSynthesizer()
    synthesizer.fit(data, categorical_columns, ordinal_columns)
    sampled = synthesizer.sample(10)
    sampled


if link:
        if synthesizer == 'IndependentSynthesizer':
            if task_done == 'Benchmark':
                independent_benchmark()
            if task_done == 'Data Synthesis':
                independent_synthesis()
        if synthesizer == 'CLBNSynthesizer':
            if task_done == 'Benchmark':
                clbn_benchmark()
            if task_done == 'Data Synthesis':
                clbn_synthesis()
        if synthesizer == 'IdentitySynthesizer':
            if task_done == 'Benchmark':
                identity_benchmark()
            if task_done == 'Data Synthesis':
                identity_synthesis()
        if synthesizer == 'UniformSynthesizer':
            if task_done == 'Benchmark':
                uniform_benchmark()
            if task_done == 'Data Synthesis':
                uniform_synthesis()

