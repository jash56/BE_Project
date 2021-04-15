import pickle
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def predict(messages):

    stop = stopwords.words('english')
    message_list = ' '.join([word for word in messages.split() if word not in stop])
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