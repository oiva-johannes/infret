from datetime import datetime, timedelta
from utils.utils import read_data, write_data
import os


def filter_dates():
    df = read_data()
    articles = df.to_dict('records')
    rm = []
    delta = timedelta(weeks=1)
    dt_current = datetime.now()

    for i in range(len(articles)):
        date = articles[i]['date']
        dt_object = datetime.strptime(date, '%d.%m.%Y')
        difference = dt_current - dt_object
        if difference > delta:
            rm.append(i)

    print(rm)
    df.drop(rm,axis=0,inplace=True) # remove news articles that are older than 2 weeks
    write_data(df)

    directory = os.fsencode("static/images/")
    updated_df = read_data()
    links = set(updated_df.to_dict('list')['href'])

    for file in os.listdir(directory):
        filename1 = os.fsdecode(file)
        filename2 = filename1.replace("_", "/")[:-4]
        if filename2 in links:
            continue
        os.remove(f"static/images/{filename1}")
