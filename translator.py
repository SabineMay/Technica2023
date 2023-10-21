from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from functools import reduce
import nltk
from translate import Translator

def get_text(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text

    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text.lower()

def translator(url, dict, freq, pos, language):

    text = get_text(url)
    sections = nltk.word_tokenize(text)
    tag = nltk.pos_tag(sections)

    print(tag)

result = translator("https://justinjackson.ca/words.html", [], "french")
translator = Translator(to_lang="es")
translation = translator.translate("This is a pen.")
print(translation)