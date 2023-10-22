from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import io
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from functools import reduce
from collections import Counter
import nltk
from translate import Translator
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

def get_URLs(): 
    urls = []
    # directory = os.path.join(os.getcwd(), "urls")
    directory = '/Users/sabinemay/Downloads/Users/sabinemay/umd-fall-2023/technica2023/urls'

    for filename in os.listdir(directory):
        fPath = os.path.join(directory, filename)

        if not os.path.isfile(fPath):
            print("something went wrong, fPath is not a valid file path")
        else: 
           urls.append(open(fPath).read())
    
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
    # print(text.lower())
    return text.lower()
    #https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python

def get_tuples(url):

    text = get_text(url)
    sections = nltk.word_tokenize(text)
    tuples = nltk.pos_tag(sections)

    return tuples

    #print(tag)

def expand_POS(pos):
    if pos[0] == "N": 
        return "Noun"
    if pos[0] == "R":
        return "Adverb"
    if pos[0] == "V": 
        return "Verb"
    if pos[0] == "J":
        return "Adjective"



'''
def translate_tuple(tuple, lang):
    lang_code = {'Spanish':'es', 'Chinese':'zh', 'Tagalog':'tl', 'Vietnamese':'vi', 
             'French':'fr', 'Hindi':'hi', 'Urdu':'ur', 'Arabic':'ar', 'Telugu':'te',
             'Tamil':'ta', 'Korean':'ko', 'Russian':'ru', 'Italian':'it'}
    
    ISO = lang_code[lang]

    translator = Translator(to_lang=ISO)
    translation = translator.translate(tuple[0])
    print(translation)
    return translation
'''



def get_small_CSV(url, dict, freq, pos, lang): 
    output = ""
    tuples = get_tuples(url)

    # Filter out tuples with the wrong POS (N, R, V, J)
    newTuples = []

    # Filter out tuples with no letter characters or that are "xxx"
    alphabet = re.compile("[A-Za-zÀ-ÖØ-öø-ÿ]+")

    for tuple in tuples: 
        match = re.search(alphabet, tuple[0])
        if match != None:
            if tuple[1][0] in pos and tuples[1] != "RP": 
                newTuples.append(tuple)

    

    # Sort tuples by count
    count_dict = {} 

    for newTuple in newTuples: 
        if newTuple in count_dict: 
            count_dict[newTuple] += 1
        else: 
            count_dict[newTuple] = 1

    newTuples.sort(reverse=True, key=lambda x: count_dict[x])

    # remove duplicates in newTuples
    res = set()
    temp = []

    for tuple in newTuples: 
        if tuple not in res: 
            temp.append(tuple)
            res.add(tuple)

    newTuples = temp

    # Cut list off based on freq
    numElems = int((freq/100)*len(newTuples))
    if numElems == 0: 
        numElems = 1

    newTuples = newTuples[:numElems:]
    
    # put into one big string seperated by x's
    big_string = ""
    for tuple in newTuples:
        big_string += tuple[0]
        big_string += " xxx "    

    # translate the big string
    lang_code = {'Spanish':'es', 'Chinese':'zh', 'Tagalog':'tl', 'Vietnamese':'vi', 
             'French':'fr', 'Hindi':'hi', 'Urdu':'ur', 'Arabic':'ar', 'Telugu':'te',
             'Tamil':'ta', 'Korean':'ko', 'Russian':'ru', 'Italian':'it'}
    
    ISO = lang_code[lang]

    translated_big_string = GoogleTranslator(source='english', target =ISO).translate(big_string)

    # translator = Translator(to_lang=ISO)
    # translated_big_string = translator.translate(big_string)
    # print(translated_big_string)

    # split bigstring on commas (regex or indexing, not ndkl)
    translations = translated_big_string.split(" xxx ")

    # Put in CSV format
    # print(len(newTuples))
    # print(len(translations))
    for i in range(len(translations) - 3):
        output += f"({newTuples[i][0]} ({expand_POS(newTuples[i][1])}), {translations[i]})"
    
    return output

def get_big_CSV(freq, pos, lang): 
    output = ""
    dict = {}

    for url in get_URLs(): 
        output += get_small_CSV(url, dict, freq, pos, lang)

    return output

@app.route('/')
def main(): 
    return open('index.html').read()

@app.route('/generate', methods=['POST'])
def generate_csv():
    data = request.json
    lang = data['languages'][0]
    freqs = data['freqs']
    pos = data['pos']

    response = get_big_CSV(int(freqs[0]), pos, lang)
    return response
    

if __name__ == '__main__':
    app.run(debug=True)







