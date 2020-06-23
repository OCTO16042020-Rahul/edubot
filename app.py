from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import pymysql

#=========
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import json
import pickle

from sklearn import preprocessing
import pandas as pd
import numpy as np
import scipy.stats
import scipy.spatial
from sklearn.model_selection import KFold
import random
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import warnings
import sys
#from sklearn.utils.extmath import np.dot

#=========Database Connection===
connection = pymysql.connect(host="localhost", user="root", password="root", database="063autoqa")
cursor = connection.cursor()
#============start=======chatbot============
#chatbot
with open("QASystemCrypto.json", encoding="utf8") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            # print(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model11 = tflearn.DNN(net)

try:
    model11.load("model.tflearn")
except:

    model11.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model11.save("model.tflearn")


#==============end====chatbot=================


app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        username = request.form.get("username")
        password = request.form.get("password")
        cursor.execute("insert into userdetails(fullname,gender,mobile,email,dob,username,password) values('"+name+"','"+gender+"','"+mobile+"','"+email+"','"+dob+"','"+username+"','"+password+"')")
        connection.commit()
        #return render_template('/index')
        return redirect(url_for('/index'))
    else:
        #return render_template('index.html')
        return redirect(url_for('/index'))


@app.route('/login', methods=["GET","POST"])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user',None)
        username = request.form.get("username")
        password = request.form.get("password")
        cursor.execute('SELECT * FROM userdetails WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        #print(account)
        if account:
            session['user'] = account[1]
            #return render_template('home.html')
            return redirect(url_for('chatbot'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    #return render_template('index.html', msg=msg)
    return redirect(url_for('index'))


#logout code
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('index'))


@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('index'))

#bot start======
@app.route('/chatbot')
def chatbot():
    if 'user' in session:
        return render_template('chatbot.html', user=session['user'])
    return redirect(url_for('index'))


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    results = model11.predict([bag_of_words(userText, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    outdatagot = ""
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
            outdatagot = random.choice(responses)
            print(outdatagot)
    return str(outdatagot)


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)
model11.load("model.tflearn")
#bot end======-------------


if __name__ == '__main__':
    #app.run(debug="True")
    app.run()
