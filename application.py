from flask import Flask
import os
import io

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

def get_small_CSV(url, dict, freq, pos, lang): 
    pass 

def get_big_CSV(freq, pos, lang): 
    output = ""
    dict = {}

    for url in get_URLs: 
        output.append(create_big_CSV(url, dict, freq, pos, lang))


@app.route("/")
def main():
    return "<p>Hello, World!</p>"

# this is my comment
#TEST
