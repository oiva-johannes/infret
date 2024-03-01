from flask import Flask, render_template, request
from search_methods.cosine_search import search_documents
from utils.utils import read_data, read_lemmatized_documents
import pandas as pd


#Initialize Flask instance
app = Flask(__name__)

df = read_data()
lemmatized = read_lemmatized_documents()

articles = df.to_dict('records')
data = df["text"].tolist()


@app.route('/')
def index():

    return render_template('index.html', articles=articles)


@app.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        query = request.form["query"]

        if query.strip() == "":
            return index()
        result = search_documents(query, data, lemmatized)
        result = [r[1] for r in result]
        result = [articles[r] for r in result]
        return render_template('index.html', articles=result)
    
    elif request.method == 'GET':
        return index()


@app.route('/sort', methods=['POST', 'GET'])
def sort():

    if request.method == 'POST':

        if request.form['sort_button'] == 'Suositut':
            return index()
        
        elif request.form['sort_button'] == 'Uudet':
            new_df = df.copy()
            new_df['date'] = pd.to_datetime(new_df['date'], format='%d.%m.%Y')
            sorted_df = new_df.sort_values(by='date', ascending=False) 
            sorted_df['date'] = sorted_df['date'].dt.strftime('%d.%m.%Y')
            sort_date = sorted_df.to_dict('records')
            return render_template('index.html', articles=sort_date)
        
        elif request.form['sort_button'] == 'Tilastot':
            return render_template('stats.html')
    
    elif request.method == 'GET':
        return index()
