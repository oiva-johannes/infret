from flask import Flask, render_template, request
from search_methods.cosine_search import search_documents
from utils.utils import read_data


#Initialize Flask instance
app = Flask(__name__)

df = read_data()
articles = df.to_dict('records')
data = df["text"].tolist()

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form["query"]
        if query.strip() == "":
            return index()
        result = search_documents(query, data)
        result = [r[1] for r in result]
        result = [articles[r] for r in result]
        return render_template('index.html', articles=result)
