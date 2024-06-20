import pickle
import sys
import os
from hazm import Normalizer, word_tokenize




with open(os.path.abspath(os.path.expanduser("../classification/LogisticRegression.pkl")), 'rb') as f:
    model = pickle.load(f)
with open(os.path.abspath(os.path.expanduser("../classification/vectorizer.pkl")), 'rb') as f:
    vectorizer = pickle.load(f)

def classifier(text):
    global model
    global vectorizer
    
    normalizer = Normalizer()
    new_text_processed = ' '.join(word_tokenize(normalizer.normalize(text)))
    new_text_tfidf = vectorizer.transform([new_text_processed])
    predicted_category = model.predict(new_text_tfidf)
    return predicted_category[0]