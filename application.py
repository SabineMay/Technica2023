from flask import Flask
import os
import io
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from functools import reduce
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
    tag = nltk.pos_tag(sections)

    print(tag)

def get_small_CSV(url, dict, freq, pos, lang): 
    tuples = get_tuples(url)

    # Filter out tuples with the wrong POS
    newTuples = []

    for tuple in tuples: 
        if tuples[1] in pos: 
            newTuples.append(tuple)

    # Sort tuples by count
    newTuples.sort(key=)

    # Cut list off based on freq

def get_big_CSV(freq, pos, lang): 
    output = ""
    dict = {}

    for url in get_URLs: 
        output.append(get_small_CSV(url, dict, freq, pos, lang))


@app.route("/")
def main():
    return "<p>Hello, World!</p>"

# this is my comment
#TEST
