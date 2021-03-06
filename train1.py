# -*- coding: utf-8 -*-
"""word2vec training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gfcKcrWlaD5XiQit8A5IYWR7vSNdlQKZ
"""

# Loading libraries
import re
import time
import pandas as pd
from tqdm.auto import tqdm
from collections import Counter

from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from gensim.models import Word2Vec
from gensim.test.utils import lee_corpus_list
from gensim.models import KeyedVectors

# Loading NLTK dataset
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Time calculation
def cal_elapsed_time(s):
    return print("Elapsed time:\t", round((time.time() - s),2))
s_time = time.time()
cal_elapsed_time(s=s_time)

# Stop words like a,the, this, so etc
stop_words = set(stopwords.words('english'))

# Convert plural verb into sungular verb
lemmatizer = WordNetLemmatizer()
print("Length of stopwords: ", len(stop_words))
print("\nLemmatization")
print("rocks :", lemmatizer.lemmatize("rocks"))

# Loading the dataset
fn_data = r"pdf_parses_0.jsonl" #Rename file from "jsonl.gz" to "jsonl"
data_pdf = pd.read_json(fn_data, lines=True)
data_pdf.head()

fn_metadata = r"metadata_0.jsonl"
metadata_df = pd.read_json(fn_metadata, lines=True)

print(list(metadata_df))
print(list(data_pdf))

set(metadata_df['year'].tolist())
data_df = pd.merge(metadata_df, data_pdf, how="inner", on="paper_id")

#data_df = data_df.dropna(subset=['year'])

#years = [1990.0,1991.0,1992.0,1993.0,1994.0,1995.0,1996.0,1997.0,1998.0,1999.0,2000.0,2001.0,2002.0,2003.0,2004.0,2005.0,2006.0,2007.0,2008.0,2009.0,2010.0,2011.0,2012.0,2013.0,2014.0,2015.0,2016.0,2017.0,2018.0,2019.0,2020.0]
#data_df= data_df[data_df.year.isin(years)]

#data_df = data_df.sort_values(by="year")

data_df = data_pdf.dropna().reset_index(drop=True)
data_df.isnull().sum()

data_content = data_df['body_text']

"""##### Data cleaning"""

def remove_link_punc(string):
    # removing links
    temp_string = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', string)

    # removing all everything except a-z english letters
    regex = re.compile('[^a-zA-Z]')
    temp_string = regex.sub(' ', temp_string)

    # removing extra spaces
    clean_string = re.sub(' +', ' ', temp_string).lower()    

    return clean_string

def data_cleaning(content):
    sentences = []
    for idx in tqdm(range(len(content))):
        
        if content[idx] !="":
            # Sentence tokenization using NLTK library
            for each_sent in  sent_tokenize(str(content[idx])):
                
                if each_sent != "":
                    temp_sent = []
                    # Removing link and punctuation
                    each_sent = remove_link_punc(each_sent.lower())

                    # Removing stopwords and applying lemmatization
                    for each_word in each_sent.split():
                        if each_word not in stop_words and len(each_word)>= 3:
                            temp_sent.append(lemmatizer.lemmatize(each_word))

                    # Only taking word list length is greater than equals to 5
                    if len(temp_sent) >= 0:
                        sentences.append(temp_sent)
    
    return sentences

sent_corpus = data_cleaning(data_content)

# Sentence words stats
len_count = []
for l in sent_corpus:
    len_count.append(len(l))

print("Total number of Sentences : ", len(len_count))
word_sent_df = pd.DataFrame(sorted(Counter(len_count).items()), columns=["No of Words in each Sentence","No of sentence"])
word_sent_df.head(10)

# data after cleaning and preprocessing
print(sent_corpus[0])



"""## Model training

##### Using Gensim model to triain word2vec model
"""

from gensim.models import Word2Vec

s_time = time.time()
print("Model Training Started...")
model = Word2Vec(sentences=sent_corpus, vector_size=100, window=5, min_count=1, workers=4)
#model = Word2Vec(lee_corpus_list, vector_size=24, epochs=100)
cal_elapsed_time(s_time)
print("Total number of unique words loaded in Model : ", len(model.wv))

# Saving the model
#model.save(r"word2vec_trained_model.model")
#model_file = 'imdb_word2vec_embedding.txt'
model.wv.save_word2vec_format('w2v_model.txt')
# Loading the model
#model = Word2Vec.load(r"word2vec_trained_model.model")

