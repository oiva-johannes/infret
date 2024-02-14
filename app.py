from flask import Flask, render_template, request
import cosine_search


#Initialize Flask instance
app = Flask(__name__)

df = cosine_search.read_data()
articles = df.to_dict('records')

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form["query"]
        data = cosine_search.read_data()["text"].tolist()
        result = cosine_search.search_documents(query, data)
        result = [r[1] for r in result]
        result = [articles[r] for r in result]
        return render_template('index.html', articles=result)



