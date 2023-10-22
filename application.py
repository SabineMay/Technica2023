from flask import Flask, render_template, request, jsonify
import os
import io
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from functools import reduce
from collections import Counter
import nltk
from translate import Translator

app = Flask(__name__)

def get_URLs(): 
    urls = []
    directory = os.getcwd()

    for filename in os.listdir(directory):
        fPath = os.path.join(directory, filename)

        if not os.path.isfile():
            print("something went wrong, fPath is not a valid file path")
        else: 
            urls.append(fPath.read())
    
    return urls

def get_text(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text.lower()
    #https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python

def get_tuples(url):

    text = get_text(url)
    sections = nltk.word_tokenize(text)
    tuples = nltk.pos_tag(sections)
    return tuples

    #print(tag)

def get_count_dict(tuples): 
    counts = Counter(word for word, tag in tuples)
    return counts

def expand_POS(pos):
    if pos[0] == "N": 
        return "Noun"
    if pos[0] == "R":
        return "Adverb"
    if pos[0] == "V": 
        return "Verb"
    if pos[0] == "J":
        return "Adjective"

def translate_tuple(tuple): 
    pass

def get_small_CSV(url, dict, freq, pos, lang): 
    output = ""
    tuples = get_tuples(url)

    # Filter out tuples with the wrong POS (N, R, V, J)
    newTuples = []

    for tuple in tuples: 
        if tuples[1][0] in pos and tuples[1] != "RP": 
            newTuples.append(tuple)

    # Sort tuples by count
    newTuples.sort(key=lambda x: get_count_dict[x])

    # Cut list off based on freq
    numElems = int((freq/100)*len(newTuples))
    if numElems == 0: 
        numElems = 1

    newTuples = newTuples[:numElems:]
    translatedNewTuples = []

    # Translate
    for newTuple in newTuples: 
        translatedNewTuples.append(translate_tuple(newTuple))

    # Put in CSV format
    for i in len(newTuples):
        output += f"{newTuples[i][0]} ({expand_POS(newTuples[i][1])}),{translatedNewTuples[i][0]}\n"
    
    return output

def get_big_CSV(freq, pos, lang): 
    output = ""
    dict = {}

    for url in get_URLs: 
        output.append(get_small_CSV(url, dict, freq, pos, lang))
    
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate(): 
    if request.method == 'POST': 
        print(get_big_CSV(100, ["N", "R", "V", "J"], "French"))

    return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug=True)

'''
@app.route('/get_freq', methods=['POST'])
def calculate_square():
    number = float(request.form['number'])
    result = number ** 2
    return jsonify({'result': result})

@app.route('/get_lang', methods=['POST'])
def calculate_cube():
    number = float(request.form['number'])
    result = number ** 3
    return jsonify({'result': result})

@app.route('/get_POS', methods=['POST'])
def calculate_cube():
    number = float(request.form['number'])
    result = number ** 3
    return jsonify({'result': result}) 
'''



