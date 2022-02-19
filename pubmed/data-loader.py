from peewee import *
from playhouse.db_url import connect
from pymed import PubMed
from datetime import datetime
import time, os

# Validate if a given publication_date is a date format (yyyy-mm-dd)
def validate(date_num):
    date_text = str(date_num)
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

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

db.create_tables([Dataset])

# Query to search keywords that includes in title/abstract from 2019-2022
PUB_QUERY = '({}[Title/Abstract]) AND (("2019/01/01"[Date - Publication] : "3000"[Date - Publication]))'

# Set Keyword: Covid-19 / Vaccine / Booster / mRNA 
KEYWORD = os.environ['KEYWORD']

# Create query
query = PUB_QUERY.format(KEYWORD)

# Initailize downloader
pubmed = PubMed(tool="AnalyzeTool", email="student@bu.edu")

# Ask as much as 10,000,000 entries for each keyword
MAX_RESULTS = 10000000

print("Start crawling: ", query)

start = time.time()

results = pubmed.query(query, max_results=MAX_RESULTS)

error_count = 0

for article in results:
    title = article.title.strip('"')
    isDate = validate(article.publication_date)
    if title is not None and isDate and article.abstract is not None:
        abstract = article.abstract.replace("\n", " ").replace("\r", " ")
        if abstract is not None:
            try:
                data = Dataset(date=article.publication_date, title=title, abstract=abstract, keyword=KEYWORD)
                data.save()
            except Exception as e:
                error_count += 1
                print("[Insert Error]" + str(date) + ", " + title + ", " + abstract)
                print(e)
            if error_count > 3:
                raise Exception

end = time.time()
print(end - start)

print("Complete: {} items".format(Dataset.select().count()))

