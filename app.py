from flask import Flask, render_template, request
from search_methods.cosine_search import search_documents
from search_methods.semantic_search import semantic_query, load_model
from utils.utils import read_data, read_lemmatized_documents
import pandas as pd


#Initialize Flask instance
app = Flask(__name__)


@app.route('/')
def index():

    global df, lemmatized, state, articles, option
    df = read_data()
    lemmatized = read_lemmatized_documents()
    state = "popular-top"
    option = "tfidf"
    articles = df.to_dict('records')

    return render_template('index.html', articles=articles, state=state, option=option)


@app.route('/search', methods=['POST', 'GET'])
def search():

    global df, lemmatized, state, articles, option 
    df = read_data()
    lemmatized = read_lemmatized_documents()
    articles = df.to_dict('records')

    data = df["text"].tolist()
    state = "search"

    if request.method == 'POST':

        query = request.form["query"]
        if query.strip() == "":
                return index()

        if request.form['search_method'] == 'method1':
            option = "tfidf"

            result = search_documents(query, data, lemmatized)
            result = [r[1] for r in result]
            result = [articles[r] for r in result]
            return render_template('index.html', articles=result, state=state, option=option)
        
        if request.form['search_method'] == 'method2':
            option = "semantic"
            
            result = semantic_query(query, load_model(), data)
            result = [r[0] for r in result]
            result = [articles[r] for r in result]
            return render_template('index.html', articles=result, state=state, option=option)
            
    
    elif request.method == 'GET':

        return index()


@app.route('/sort', methods=['POST', 'GET'])
def sort():

    global df, lemmatized, state, articles, option

    if request.method == 'POST':
        print(state)
        print(request.form)
        if "Suositut" in request.form['sort_button']:
            if state == "popular-top":
                state = "popular-bot"
                new_df_popu = df.copy()
                sorted_popu_list = new_df_popu.sort_values(by='popularity', ascending=False)
                sort_popu_dict = sorted_popu_list.to_dict('records')
                return render_template('index.html', articles=sort_popu_dict, state=state, option=option)
            else:
                state = "popular-top"
                return render_template('index.html', articles=articles, state=state, option=option)

        elif "Uudet" in request.form['sort_button']:
            new_df_date = df.copy()
            new_df_date['date'] = pd.to_datetime(new_df_date['date'], format='%d.%m.%Y')
            if state == "newest-top":
                state = "newest-bot"
                sorted_date_list = new_df_date.sort_values(by='date', ascending=True) 
                sorted_date_list['date'] = sorted_date_list['date'].dt.strftime('%d.%m.%Y')
                sorted_date_dict = sorted_date_list.to_dict('records')
                return render_template('index.html', articles=sorted_date_dict, state=state, option=option)
            else:
                state = "newest-top"
                sorted_date_list = new_df_date.sort_values(by='date', ascending=False) 
                sorted_date_list['date'] = sorted_date_list['date'].dt.strftime('%d.%m.%Y')
                sorted_date_dict = sorted_date_list.to_dict('records')
                return render_template('index.html', articles=sorted_date_dict, state=state, option=option)

        elif "Tietoa" in request.form['sort_button']:
            if state == "info-top":
                state = "info-down"
                return render_template('info.html', state=state, option=option)
            else:
                state = "info-top"
                return render_template('info.html', state=state, option=option)
    
    elif request.method == 'GET':
        return index()
