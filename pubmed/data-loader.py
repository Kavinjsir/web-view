from pymed import PubMed
import threading, queue, csv, re, pathlib

# OUTPUT_PATH
PATH_PREFIX = str(pathlib.Path().resolve()) + "/data"

# Query to search keywords Covid-19/Vaccine/Booster/mRNA that includes in title/abstract from 2019-2022
PUB_QUERY= '((((Covid-19[Title/Abstract]) OR (Vaccine[Title/Abstract])) OR (Booster[Title/Abstract])) OR (mRNA[Title/Abstract])) AND (("{}"[Date - Publication] : "{}"[Date - Publication]))'

# Year to query
TARGET_YEARS = [ 2019, 2020, 2021, 2022 ]

# SEASONS = [ ('01/01', '03/31'), ('04/01', '06/30'), ('07/01', '09/30'), ('10/01', '12/31') ]
SEASONS = [ ('12/21', '12/23'), ('12/24', '12/26'), ('12/27', '12/29'), ('12/30', '12/31') ]

# Ask as much as 1000,000 entries for each season
MAX_RESULTS = 100000

q = queue.Queue()

def downloader():
    while True:
        query = q.get()

        start, end = re.findall(r"\d{4}\/\d{2}\/\d{2}", query)
        print(f'{start}-{end} start')

        pubmed = PubMed(tool="AnalyzeTool", email="student@bu.edu")
        results = pubmed.query(query, max_results=MAX_RESULTS)

        filename = "{}/{}-{}.csv".format(PATH_PREFIX, start.replace("/", "-"), end.replace("/", "-"))
        with open(filename, 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=',')

            for article in results:
                if hasattr(article, 'title') and hasattr(article, 'publication_date') and hasattr(article, 'abstract'):
                    title = article.title.strip('"')
                    date = article.publication_date
                    # abstract = article.abstract.replace("\n", "")

                    data_writer.writerow([date, title])

        print(f'{filename} done')
        q.task_done()


# turn-on the worker thread
threading.Thread(target=downloader, daemon=True).start()

print("Build queue...")
for year in TARGET_YEARS:
    for s in SEASONS:
        startDate = "{}/{}".format(year, s[0])
        endDate = "{}/{}".format(year, s[1])
        query = PUB_QUERY.format(startDate, endDate)
        q.put(query)
print("Queue built.")

q.join()

print("All tasks complete.")

