from peewee import *
from playhouse.db_url import connect

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import seaborn as sns
from scipy.stats import normaltest

import os

KEYWORD = os.environ['KEYWORD']

QUERY_STR = """SELECT
    date_trunc('month', date) m,
    COUNT (id)
FROM
    dataset
WHERE
    keyword = %s
GROUP BY
    m
ORDER BY
    m;"""

DB_URL = os.environ.get('DATABASE')

db = connect(DB_URL)

class BaseModel(Model):
    class Meta:
        database = db

class Dataset(BaseModel):
    date = DateField()
    title = TextField()
    abstract = TextField()
    keyword = TextField()

query = Dataset.raw(QUERY_STR, KEYWORD)

COUNT_DICT = {}

for item in query:
    COUNT_DICT[item.m] = item.count

# convert the dictionary to a list
l_list = [k for k, v in COUNT_DICT.items() for _ in range(v)]

plt.subplots(figsize=(16, 9))
sns.histplot(data=l_list, kde=True)
plt.show()

stat, p = normaltest(list(COUNT_DICT.values()))
print("stat={}, p={}".format(stat,p))
if p > 0.05:
    print('Probably Gaussian')
else:
    print('Probably not Gaussian')

