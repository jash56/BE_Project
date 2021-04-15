import pickle
import numpy as np

def predict(messages):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
            "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
            'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 
            'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
            "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 
            'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 
            'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
            'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 
            'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 
            'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
            "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
            "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 
            'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
            'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    message_list = ' '.join([word for word in messages.split() if word not in stopwords])
    feature_list = np.array([message_list])
    tfidf = pickle.load(open('text_encoder.sav','rb'))
    encoded_feature_list = tfidf.transform(feature_list)
    model = pickle.load(open('outcome.sav','rb'))
    output = model.predict(encoded_feature_list)
    if output[0] == '0':
        return 'This negotiation will most likely fail :('
    else:
        return 'This negotiation is on track to being a success :)'

def get_reccomendation(messages, buyer_target, seller_target):

    return predict(messages)

""" import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import numpy as np


def predict(category, buyer_target, seller_target, messages):

    stop = stopwords.words('english')
    print(messages)
    message_list = ' '.join([word for word in messages.split() if word not in stop])
    feature_list = np.array([category, buyer_target, seller_target, messages])
    feature_list = feature_list.reshape((1, 4))
    print(feature_list.shape)
    tfidf = pickle.load(open('text_encoder.sav','rb'))
    encoded_feature_list = tfidf.transform(feature_list.astype('U'))
    print(encoded_feature_list.shape)
    #print(encoded_feature_list)
    model = pickle.load(open('outcome.sav','rb'))
    #print(model)
    output = model.predict(encoded_feature_list)
    print(output)
    if output[0] == '0':
        return 'This negotiation will most likely fail'
    else:
        return 'This negotiation is on track to being a success' """