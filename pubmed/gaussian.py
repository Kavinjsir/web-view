from peewee import *
from playhouse.db_url import connect

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import os

KEYWORD = os.environ['KEYWORD']

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

query = Dataset.raw("""SELECT
    date_trunc('month', date) m,
    COUNT (id)
FROM
    dataset
WHERE
    keyword = %s
GROUP BY
    m
ORDER BY
    m;""", KEYWORD)

COUNT_DICT = {}

for item in query:
    COUNT_DICT[item.m] = item.count

# Create figure and plot space
fig, ax = plt.subplots(figsize=(12, 12))

# Add x-axis and y-axis
ax.bar(COUNT_DICT.keys(),
       COUNT_DICT.values(),
       width=10)

# Set title and labels for axes
ax.set(xlabel="Year 2019-2022",
       ylabel="Count",
       title="Keyword: {}".format(KEYWORD))

# Define the date format
date_form = DateFormatter('%Y-%m')
ax.xaxis.set_major_formatter(date_form)
plt.show()

