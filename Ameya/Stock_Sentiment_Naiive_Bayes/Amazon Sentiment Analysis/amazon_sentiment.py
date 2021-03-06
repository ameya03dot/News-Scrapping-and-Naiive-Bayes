# -*- coding: utf-8 -*-
"""Amazon_Sentiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HC4UR8kl1AFHWwYIl0fy9TwusLUzTsjs
"""

import pandas as pd

df = pd.read_csv("amazon_filtered_data.csv")

df

text = df['headline']

!pip install vaderSentiment

import nltk

nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

  
    # Create a SentimentIntensityAnalyzer object. 
sid_obj = SentimentIntensityAnalyzer() 
  
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores.
sentiment=[]
for i in text:
  sentiment_dict = sid_obj.polarity_scores(i)
  if sentiment_dict['compound'] >= 0.05 :
    sentiment.append('Positive')
   
  
  elif sentiment_dict['compound'] <= - 0.05 : 
    sentiment.append('Negative')
  
  
  else : 
    sentiment.append('Neutral')

df2 = pd.DataFrame(sentiment,columns=['Sentiment'])

df2

frames = [df,df2]

df3 = pd.concat(frames,axis = 1)

df3

df3.to_csv('Amazon_Sentiments.csv')

df3.dtypes

df4 = pd.read_csv('Amazon_Sentiments.csv')

df4

df4 = df4.drop(labels = 'Unnamed: 0',axis = 1)



df4['Sentiment'] = df4['Sentiment'].replace(['Neutral','Positive','Negative'],['0','1','2'])

df4

with open('contractions.json', 'r') as f:
    contractions_dict = json.load(f)
contractions = contractions_dict['contractions']

import re

def process_tweet(headlines):
    headlines = headlines.lower()                                             # Lowercases the string
    headlines = re.sub('@[^\s]+', '', headlines)                              # Removes usernames
    headlines = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', headlines)   # Remove URLs
    headlines = re.sub(r"\d+", " ", str(headlines))                           # Removes all digits
    headlines = re.sub('&quot;'," ", headlines)                               # Remove (&quot;) 
    headlines = emoji(headlines)                                              # Replaces Emojis
    headlines = re.sub(r"\b[a-zA-Z]\b", "", str(headlines))                   # Removes all single characters
    for word in headlines.split():
        if word.lower() in contractions:
            headlines = headlines.replace(word, contractions[word.lower()])   # Replaces contractions
    headlines = re.sub(r"[^\w\s]", " ", str(headlines))                       # Removes all punctuations
    headlines = re.sub(r'(.)\1+', r'\1\1', headlines)                         # Convert more than 2 letter repetitions to 2 letter
    headlines = re.sub(r"\s+", " ", str(headlines))                           # Replaces double spaces with single space    
    return headlines

def emoji(headlines):
    # Smile -- :), : ), :-), (:, ( :, (-:, :') , :O
    headlines = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\)|:O)', ' positiveemoji ', headlines)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    headlines = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' positiveemoji ', headlines)
    # Love -- <3, :*
    headlines = re.sub(r'(<3|:\*)', ' positiveemoji ', headlines)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-; , @-)
    headlines = re.sub(r'(;-?\)|;-?D|\(-?;|@-\))', ' positiveemoji ', headlines)
    # Sad -- :-(, : (, :(, ):, )-:, :-/ , :-|
    headlines = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:|:-/|:-\|)', ' negetiveemoji ', headlines)
    # Cry -- :,(, :'(, :"(
    headlines = re.sub(r'(:,\(|:\'\(|:"\()', ' negetiveemoji ', headlines)
    return headlines

import json, nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import numpy as np

headlines = df4.columns.values[0]
sentiment = df4.columns.values[1]
headlines, sentiment



df4['processed_headlines'] = np.vectorize(process_tweet)(df4[headlines])

df4.head(10)

df5 = df4

df5.to_csv('Preprocessing_Amazon.csv')

from sklearn.feature_extraction.text import CountVectorizer

count_vectorizer = CountVectorizer(ngram_range=(1,2))    # Unigram and Bigram
final_vectorized_data = count_vectorizer.fit_transform(df4['processed_headlines'])  
final_vectorized_data

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(final_vectorized_data, df4[sentiment],
                                                    test_size=0.2, random_state=69)

from sklearn.naive_bayes import MultinomialNB  # Naive Bayes Classifier

model_naive = MultinomialNB().fit(X_train, y_train) 
predicted_naive = model_naive.predict(X_test)

from sklearn.metrics import confusion_matrix

plt.figure(dpi=100)
mat = confusion_matrix(y_test, predicted_naive)
sns.heatmap(mat.T, annot=True, fmt='d', cbar=False)

plt.title('Confusion Matrix for Naive Bayes')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig("confusion_matrix.png")
plt.show()

from sklearn.metrics import accuracy_score

score_naive = accuracy_score(predicted_naive, y_test)
print("Accuracy with Naive-bayes: ",score_naive)