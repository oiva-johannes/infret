from datetime import datetime, timedelta
from utils.utils import read_data, write_data


df = read_data()
articles = df.to_dict('records')
rm = []
delta = timedelta(weeks=2)
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
