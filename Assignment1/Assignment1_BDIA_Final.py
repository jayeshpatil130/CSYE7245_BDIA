
import apache_beam as beam

# import print library
import logging

from past.builtins import unicode

# import pipeline options.
from apache_beam.options.pipeline_options import PipelineOptions

# Set log level to info
root = logging.getLogger()
root.setLevel(logging.INFO)

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import io
import csv
from google.cloud import storage
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
# client = storage.Client()
storage_client = storage.Client()
bucket = storage_client.get_bucket('assignment1bdia')

from tokenizers import SentencePieceBPETokenizer

#Initialize a tokenizer
tokenizer = SentencePieceBPETokenizer()

#Then train it!
tokenizer.train('Trained_words.txt')

#And finally save it somewhere
tokenizer.save("tokenizer", "my-bpe")

#Initialize a tokenizer
vocab = "tokenizer/my-bpe-vocab.json"
merges = "tokenizer/my-bpe-merges.txt"
tokenizer = SentencePieceBPETokenizer(vocab, merges)
global_list = []


# scrape from input to output
class Scrape(beam.DoFn):
    def process(self,element):
        inputs_pattern = 'gs://assignment1bdia/data/export_dataframe.csv'
        df = pd.read_csv(inputs_pattern)
        output_csv = pd.DataFrame(columns=['cik', 'year', 'Filings', 'link'])
        counter = 0
        quarter = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
        for i in quarter:
            for index, row in df.iterrows():
                #####Get the Master Index File for the given Year
                url = 'https://www.sec.gov/Archives/edgar/full-index/%s/%s/master.idx' % (str(row['year']), i)
                response = urllib2.urlopen(url)
                string_match1 = 'edgar/data/'
                element2 = None
                element3 = None
                element4 = None
                text_list = []
                ###Go through each line of the master index file and find given CIK #and
                # FILE (10-K) and extract the text file path
                for line in response:
                    line = line.decode('utf-8')
                    if str(row['cik']) in line and str(row['Filings']) in line:
                        for element1 in line.split(' '):
                            if string_match1 in element1:
                                element2 = element1.split('|')
                                for element3 in element2:
                                    if string_match1 in element3:
                                        element4 = element3
                                        url3 = 'https://www.sec.gov/Archives/' + element4
                                        response3 = urllib2.urlopen(url3)
                                        # print (url3)
                                        a = row['cik']
                                        b = row['year']
                                        c = row['Filings']
                                        output_csv.loc[counter] = [a, b, c, url3]
                                        with open('Original_txt_file.txt', 'w') as f:
                                            f.write(response3.read().decode('utf-8'))
                                            f.close()
                                        counter = counter + 1
                                        output_csv.to_csv('local_file.csv')
                                        filename('local_file.csv', content_type='text/csv')
                                        blob = bucket.blob(str(row['cik']) + '/' + str(row['year']) + '/' + str(
                                            row['Filings']) + '/' + 'Metadata.csv')
                                        blob.upload_from_filename('local_file.csv', content_type='text/csv')
                                        blob = bucket.blob(str(row['cik']) + '/' + str(row['year']) + '/' + str(
                                            row['Filings']) + '/' + 'Original_txt_file.txt')
                                        blob.upload_from_filename('Original_txt_file.txt', content_type='text/csv')
                                        text_list.append(str(row['cik']) + '/' + str(row['year']) + '/' + str(
                                            row['Filings']) + '/' + 'Original_txt_file.txt')
        global_list.append(text_list)
        return global_list

class CleanText(beam.DoFn):
    def process(self, element):
        print("Inside create_text_files")
        for i in global_list:
            print(i)
            inputs_pattern = i[0]
            input_pattern_without_filename = inputs_pattern[:-21]
            cleaned_list = []
            blob = bucket.get_blob(inputs_pattern)
            downloaded_blob = blob.download_as_string()
            # response = urllib2.urlopen(inputs_pattern)

            try:
                new_str = re.sub('[^a-zA-Z]', ' ', downloaded_blob)
                new_str2 = ' '.join(word for word in new_str.split(' ') if len(word) > 1)
                stop_words = set(stopwords.words('english'))
                element = new_str2.split()
                for r in element:
                    if not r in stop_words:
                        # blob.upload_from_string(r)
                        cleaned_list.append(r)
                with open('Scraped_text_file.txt', 'w') as f:
                    for z in cleaned_list:
                        f.write(z + '')
                        f.close()
            except:
                pass
            finally:
                f.close()
            blob = bucket.blob(input_pattern_without_filename + 'Scraped_text_file.txt')
            blob.upload_from_filename('Scraped_text_file.txt', content_type='text/csv')
        return

class Tokenize(beam.DoFn):
    def process(self, element):
        line = element.split()
        encoded = tokenizer.encode_batch(line)
        return

class Word_count(beam.DoFn):
    def process(self,element):
        wordcomparepath = 'categories'
        blob = bucket.get_blob(wordcomparepath + '/Negative.txt')
        negative = blob.download_as_string().split()
        blob = bucket.get_blob(wordcomparepath + '/Positive.txt')
        positive = blob.download_as_string().split()
        blob = bucket.get_blob(wordcomparepath + '/Uncertainty.txt')
        uncertainty = blob.download_as_string().split()
        blob = bucket.get_blob(wordcomparepath + '/Litigious.txt')
        litigious = blob.download_as_string().split()
        blob = bucket.get_blob(wordcomparepath + '/StrongModal.txt')
        strongmodal = blob.download_as_string().split()
        blob = bucket.get_blob(wordcomparepath + '/WeakModal.txt')
        weakmodal = blob.download_as_string().split()
        blob = bucket.get_blob(wordcomparepath + '/Constraining.txt')
        constraining = blob.download_as_string().split()

        for i in global_list:
            inputs_pattern = i[0]
            input_pattern_without_filename = inputs_pattern[:-21]
            input_pattern_just_path = inputs_pattern[:-22]
            pathlist1 = input_pattern_just_path.split('/')
            print(type(pathlist1))
            pathlist2 = []
            pathlist2_string = ''
            for x in pathlist1:
                pathlist2.append(x)
            downloaded_blob = ''
            try:
                blob = bucket.get_blob(input_pattern_without_filename + 'Scraped_text_file.txt')
                downloaded_blob = blob.download_as_string()
            except:
                pass

        # Open the file in read mode
        text1 = downloaded_blob.split()

        count_list = []
        # count_csv = pd.DataFrame(columns=['Word', 'Wordlist', 'Count'])
        for w in set(text1):
            if w in negative:
                count_list.append(pathlist2 + [w, "negative", text1.count(w)])
            elif w in positive:
                count_list.append(pathlist2 + [w, "positive", text1.count(w)])
            elif w in uncertainty:
                count_list.append(pathlist2 + [w, "uncertainty", text1.count(w)])
            elif w in litigious:
                count_list.append(pathlist2 + [w, "litigious", text1.count(w)])
            elif w in strongmodal:
                count_list.append(pathlist2 + [w, "strongmodal", text1.count(w)])
            elif w in weakmodal:
                count_list.append(pathlist2 + [w, "weakmodal", text1.count(w)])
            elif w in constraining:
                count_list.append(pathlist2 + [w, "constraining", text1.count(w)])


        for o in range(len(count_list)):
            print(count_list[o])

        dfWordCount = pd.DataFrame(count_list, columns=['cik', 'year', 'filing', 'wordlist', 'word', 'wordcount'])
        csv_wordcount = dfWordCount.to_csv('Word_count.csv', index=False)

        blob = bucket.blob(input_pattern_without_filename + 'Word_count.csv')
        blob.upload_from_filename('Word_count.csv', content_type='text/csv')

        return count_list



# Create a pipeline
plOps = beam.Pipeline(options=PipelineOptions())

txt_files = (
        plOps | 'Read lines' >> beam.io.ReadFromText('gs://assignment1bdia/data/export_dataframe.csv')
)

scrape_txt_file = (
        txt_files | 'Scrape Text File' >> beam.ParDo(Scrape())
)

clean_text = (
        scrape_txt_file | 'Remove stopwords and symbols' >> beam.ParDo(CleanText())
)

tokenize = (
        clean_text | 'Remove blanks' >> beam.ParDo(Tokenize())
)

word_counts = (
           tokenize | 'Word count' >> beam.ParDo(Word_count())
                    | 'Write word count' >> beam.io.WriteToText('Word_count', file_name_suffix='.txt')
       )

# Run the pipeline
result = plOps.run()
#  wait until pipeline processing is complete
result.wait_until_finish()