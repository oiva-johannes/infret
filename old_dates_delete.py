from datetime import datetime, timedelta
import pandas as pd


df = pd.read_excel('dynamic-datasets/articles_excel.xlsx')
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
df.drop(rm,axis=0,inplace=True) # remove news articles that are older than 1 week
df.to_excel('dynamic-datasets/articles_excel.xlsx', index=False)
