from flask import Flask
from flask import render_template
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
wsgi_app = app.wsgi_app

class WordOfTheDay:
    word = ''
    wordclass = ''
    pronounciation = ''
    definition = ''

word = WordOfTheDay()
today = date.today()

def scrape_merriam_webster(date):
    source = requests.get('https://www.merriam-webster.com/word-of-the-day/' + date.strftime("%Y-%m-%d")).text
    scrape = BeautifulSoup(source, features='html.parser')

    word.word = scrape.find('h1').text
    word.wordclass = scrape.find('span', class_='main-attr').text
    word.pronounciation = scrape.find('span', class_='word-syllables').text
    word.definition = scrape.find('div', class_='wod-definition-container').select_one('p').text

    return word

def handle_date(inputdate):
    if inputdate is None:
        inputdate = today
    else:
        try: 
            inputdate = datetime.strptime(inputdate, "%Y-%m-%d").date()
        except:
            inputdate = today

    if inputdate > today:
        inputdate = today
    return inputdate

@app.route('/')
@app.route('/<inputdate>')
def word_of_the_day(inputdate=None):
    inputdate = handle_date(inputdate)

    word = scrape_merriam_webster(inputdate)

    return render_template(
        'index.html',
        date=inputdate,
        word=word,
        delta=timedelta(1)
    )


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
