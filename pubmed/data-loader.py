from pymed import PubMed
import threading, queue, csv, re, pathlib, time
import time

# OUTPUT_PATH
PATH_PREFIX = str(pathlib.Path().resolve()) + "/data"

# Query to search keywords that includes in title/abstract from 2019-2022
PUB_QUERY = '({}[Title/Abstract]) AND (("2019/01/01"[Date - Publication] : "3000"[Date - Publication]))'

# Set Keyword: Covid-19 / Vaccine / Booster / mRNA 
KEYWORD = "Covid-19"


# Output filename
filename = "{}/{}.csv".format(PATH_PREFIX, KEYWORD)

# Create query
query = PUB_QUERY.format(KEYWORD)

# Initailize downloader
pubmed = PubMed(tool="AnalyzeTool", email="student@bu.edu")

# Ask as much as 10,000,000 entries for each season
# MAX_RESULTS = 10000000
MAX_RESULTS = 1000

print("Start crawling: ", query)

start = time.time()

results = pubmed.query(query, max_results=MAX_RESULTS)

with open(filename, 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile, delimiter=',')

    for article in results:
        if hasattr(article, 'title') and hasattr(article, 'publication_date') and hasattr(article, 'abstract'):
            title = article.title.strip('"')
            date = article.publication_date
            # abstract = article.abstract.replace("\n", "")

            data_writer.writerow([date, title])


end = time.time()
print(end - start)
print("Complete: ", filename)


