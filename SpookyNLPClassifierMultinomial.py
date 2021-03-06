import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from nltk.stem.porter import *
from sklearn.model_selection import GridSearchCV


def loadData(isTrain):
    """
    Load test and train data
    """
    csv = "test.csv"
    if(isTrain):
        csv = "train.csv"
    return pd.read_csv(csv)


def text_process(text):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    #nopunc = [char for char in text if char not in string.punctuation]

    stemmer = PorterStemmer()

    nopunc = []
    stopwordsRemoved = []

    for char in text:
        if(char not in string.punctuation):
            nopunc.append(char)

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)

    # Now just remove any stopwords
    for word in nopunc.split():
        word = word.lower()
        if word not in stopwords.words('english'):
            word = stemmer.stem(word);
            stopwordsRemoved.append(word)

    return stopwordsRemoved


def buildPipeline(model):
    return Pipeline([
    ('vec', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('clf', model), # train on TF-IDF vectors w/ Naive Bayes classifier
    ])


    #pipeline = Pipeline([('vec', CountVectorizer(encoding='cp874', preprocessor=pre_process_1, tokenizer=tokenize_1, stop_words=heavy_st, token_pattern=None)),('tfidf', TfidfTransformer()), ('clf',       MultinomialNB())])


def main():
    trainData = loadData(True)
    testData = loadData(False)

    txt_train = trainData['text']
    label_train = trainData['author']

    txt_test = testData['text']
    
    model = MultinomialNB()

    #parameters = {'tfidf__use_idf': (True, False),
    #              'alpha': np.array([1,0.1,0.01,0.001,0.0001,0]),
    #              }

    parameters = {
       # 'vec__max_df': (0.5, 0.625, 0.75, 0.875, 1.0),
       #'vec__max_features': (None, 5000, 10000, 20000),
       #'vec__min_df': (1, 5),
       # 'tfidf__use_idf': (True, False),
        #'tfidf__sublinear_tf': (True, False),
        #'vec__binary': (True, False),
       # 'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.01, 0.001)
    }



    pp = buildPipeline(model)

    pipeline = GridSearchCV(pp, parameters, n_jobs=-1)

    pipeline.fit(txt_train,label_train)

    predictions = pipeline.predict_proba(txt_test)
    print("***************************************")
    print(pipeline.best_params_)
    print("***************************************")
    sub = pd.DataFrame(predictions, columns=['EAP', 'HPL', 'MWS'])

    iddd = pd.DataFrame(testData['id'], columns=['id'])

    sub = iddd.join(sub)

    sub.to_csv("submission.csv")



if __name__ == "__main__": main()
