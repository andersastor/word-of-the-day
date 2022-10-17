from flask import Flask
from flask import render_template
from datetime import date
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
wsgi_app = app.wsgi_app

class WordOfTheDay:
    word = ''
    wordclass = ''
    pronounciation = ''
    definition = ''

def scrape_merriam_webster():
    source = requests.get('https://www.merriam-webster.com/word-of-the-day').text
    scrape = BeautifulSoup(source, features='html.parser')

    word = WordOfTheDay()
    word.word = scrape.find('h1').text
    word.wordclass = scrape.find('span', class_='main-attr').text
    word.pronounciation = scrape.find('span', class_='word-syllables').text
    word.definition = scrape.find('div', class_='wod-definition-container').select_one('p').text

    return word

@app.route('/')
def word_of_the_day():
    word = scrape_merriam_webster()
    return render_template(
        'index.html',
        date=date.today().strftime("%B %d, %Y"),
        word=word
    )

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
