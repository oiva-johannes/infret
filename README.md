# infret
### - Search engine, recommendation system and an aggregator for Finnish news articles from Yle, Ilta-Sanomat and Helsingin Sanomat.

## Instructions for users of Ubuntu.

Clone the repository to your own computer.

Cd into the reposiroty and create a virtual enviroment to contain the repository.

Add a virtual enviroment `demoenv`:

`python3 -m venv demoenv`

Activate the enviroment:

`. demoenv/bin/activate`

Install the required packages:
`pip3 install -r requirements.txt`

### Install voikko:
More information here: https://voikko.puimula.org/

(Note: Instructions to install and use voikko with python applications, also info about common errors: https://voikko.puimula.org/python.html)

Install the native library:

`sudo apt-get install libvoikko1`

Install dictionary files:

Choose the first standard dictionary of Finnish `dict.zip`
https://www.puimula.org/htp/testing/voikko-snapshot-v5/
Unzip the `dict.zip` in `/etc/voikko`

### Install the spacy model for finnish:

`python3 -m spacy download fi_core_news_sm`

### Run the Flask app:

```
export FLASK_APP=app.py
export FLASK_DEBUG=True
export FLASK_RUN_PORT=8000
```

`flask run`



