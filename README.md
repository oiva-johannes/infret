# InfRet
### Search engine, recommendation system and an aggregator for Finnish news articles from Yle, Ilta-Sanomat and Helsingin Sanomat.

![Screenshot from 2024-03-10 22-22-26](https://github.com/oiva-johannes/infret/assets/72695556/56556af4-fc37-4384-9eab-38d56155bbbc)


## Instructions for running the `app.py` on Ubuntu based systems

Clone the repository to your computer.

Cd into the repository and create a virtual enviroment to contain the dependencies.

Add a virtual enviroment `demoenv`:

`python3 -m venv demoenv`

Activate the enviroment:

`source demoenv/bin/activate`

Install the dependencies/requirements:

`pip3 install -r requirements.txt`

Next we need to install the Finnish language library called Voikko (https://voikko.puimula.org/).

Instructions to install and use Voikko with Ubuntu+Python are

Install the native library with apt:

`sudo apt install libvoikko1`

Install dictionary files:

Choose the first standard dictionary for Finnish named `dict.zip` from the link:

https://www.puimula.org/htp/testing/voikko-snapshot-v5/

create `/etc/voikko` with:

`sudo mkdir /etc/voikko`

Then unzip the `dict.zip` to the `/etc/voikko`:

`sudo unzip /etc/voikko/dict.zip`

More info on Python with Voikko can be found here https://voikko.puimula.org/python.html

Now also install the spacy model for Finnish:

`python3 -m spacy download fi_core_news_sm`

Now you can run the Flask app:

`flask run`


## If you want to run or schedule the web scraper you will need the Selenium webdriver (because of the nature of dynamic Javascript sites).
The Selenium webdriver requires `chrome-linux64` and `chromedriver` binaries and you can install them with Wget. 

First check that you Wget installed:

`sudo apt install wget`

And then install `chrome-linux64` and `chromedriver` with:

`wget https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chrome-linux64.zip`

`wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip`

Unzip both of these to the main directory (same where app.py resides).

Now you should be able to run the web scraper from the main directory with:

`python -m utils.web_scraping`

If error arises you might need to hunt for some missing requirements for the chromedriver/chrome.



