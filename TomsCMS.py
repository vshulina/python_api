from urllib.request import Request, urlopen, URLError
import json, csv

def main():
    startDate = input('Start Date? (YYYY-MM-DD) ') + 'T00%3A00%3A00Z'
    endDate = input('End Date? (YYYY-MM-DD) ') + 'T00%3A00%3A00Z'
    limit = '2000'

    url = 'http://internal-us-east1-tomsguide-app-elb-39731471.us-east-1.elb.amazonaws.com:8080/getcontent/en/listing?limit=' \
          + limit + '&lang=en&dateFrom=' + startDate + '&dateTo=' + endDate
    
    tgus = urlopen(url)
    response = tgus.read().decode("utf-8")
    jsonResponse = json.loads(response)
    
    ofile = open('TomsCMS.csv', 'w', newline='')
    ofile.truncate()
    tomswriter = csv.writer(ofile, delimiter=',')
    tomswriter.writerow(['content-type','content-url','author-id','publish date','category','site','title'])
    
    for doc in jsonResponse['cms_content']:
        try:
            publishDate = doc['publish_date'][5:7] + '/' + doc['publish_date'][8:10] + '/' + doc['publish_date'][:4]
        except KeyError:
            publishDate = ''
        try:
            category = ', '.join(doc['tags'])
        except KeyError:
            category = ''
        try:
            site = doc['canonical'][:doc['canonical'].find('/', 10)]
        except KeyError:
            site = ''
        try:
            pageurl = doc['canonical'][doc['canonical'].find('/', 10):]
        except KeyError:
            pageurl = ''
        try:
            tomswriter.writerow([doc['doc_type'], pageurl, 'author_placement', publishDate, category, site, doc['headline']])
        except KeyError:
            print('Unavailable')

if __name__ == '__main__':
    main()
