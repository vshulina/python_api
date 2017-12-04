import http.client, json, csv, math, datetime
from collections import deque

def main():    
    #create file and csv writer objects
    hfile = open('Headers.csv','w', newline='', encoding='utf-8')
    cfile = open('BraxCampaigns.csv', 'a', newline='', encoding='utf-8')
    pfile = open('BraxPublishers.csv', 'a', newline='', encoding='utf-8')
    afile = open('BraxAds.csv', 'a', newline='', encoding='utf-8')
    hcsvwriter = csv.writer(hfile, delimiter=',')
    ccsvwriter = csv.writer(cfile, delimiter=',')
    pcsvwriter = csv.writer(pfile, delimiter=',')
    acsvwriter = csv.writer(afile, delimiter=',')
    
    #create headers in csv files
    hcsvwriter.writerow(['x-request-id', 'request string'])
    #not needed after initial load
    #ccsvwriter.writerow(['date','source','source account id', 'source campaign id', 'campaign name', 'ctr', 'ecpc', 'cost', 'cpa', 'icr'])
    #pcsvwriter.writerow(['date','source','source account id', 'source campaign id', 'source publisher id', 'publisher name', 'ctr', 'ecpc', 'cost', 'cpa', 'icr'])
    #acsvwriter.writerow(['date','source','source account id', 'source campaign id', 'source publisher id', 'source section id', 'publisher name', 'section name', 'ctr', 'ecpc', 'cost', 'cpa', 'icr'])

    #get account ids
    jsonResponse = getdata("/v1/accounts", hcsvwriter)
    campaigns = []
    source_account_ids = []
    sources = []

    #set date ranges
    last_date = get_last_date('BraxAds.csv').split('-')
    start_date = datetime.date(int(last_date[0]), int(last_date[1]), int(last_date[2])+1)
    print("starting from " + str(start_date))
    #start_date = datetime.date(2017,7,27) #manual date input
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    day_count = (end_date - start_date).days + 1

    #store account ids and sources
    try:
        for camp in jsonResponse['results']:
            campaigns.append(camp['id'])
            source_account_ids.append(camp['source_account_id'])
            sources.append(camp['source'])
    except KeyError:
        print(jsonResponse)

    if start_date <= end_date:
        for d in (start_date + datetime.timedelta(n) for n in range(day_count)):
            for source, cid in zip(sources, source_account_ids):
                dates = "&start_date=" + str(d) + "&end_date=" + str(d)
                
                #campaign data
                cjsonResponse = getdata("/v1/reports/campaigns?source="+source+"&source_account_id="+cid+dates, hcsvwriter)
                try:
                    for sai in cjsonResponse['results']:
                        ccsvwriter.writerow([str(d),source,cid,sai['source_campaign_id'],sai['name'],sai['ctr'],sai['ecpc'],sai['cost'],sai['cpa'],sai['icr']])
                except KeyError:
                    print("campaigns unavailable for source " + source + " account id " + cid)
                print(str(d) + " campaign data for source " + source + " account id " + cid + " done")
                
                #publisher data
                count = 0
                offset = 0
                pagination = getdata("/v1/reports/publishers?source="+source+"&source_account_id="+cid+dates, hcsvwriter)
                pages = math.ceil(pagination['pagination']['total']/100)
                
                #pull all pages of the report
                while (count < pages):
                    pageParameter = "&offset=" + str(offset) + "&limit=100"
                    pjsonResponse = getdata("/v1/reports/publishers?source="+source+"&source_account_id="+cid+dates+pageParameter, hcsvwriter)
                    try:
                        for psai in pjsonResponse['results']:
                            pcsvwriter.writerow([str(d),source,cid,psai['source_campaign_id'],psai['source_publisher_id'],psai['name'],psai['ctr'],psai['ecpc'],psai['cost'],psai['cpa'],psai['icr']])
                    except KeyError:
                        print("publishers unavailable for source " + source + " account id " + cid)
                    offset = offset + 100
                    count = count + 1
                print(str(d) + " publisher data for source " + source + " account id " + cid + " done")
                
                #ads data
                ajsonResponse = getdata("/v1/reports/sections?source="+source+"&source_account_id="+cid+dates, hcsvwriter)
                try:
                    for asai in ajsonResponse['results']:
                        acsvwriter.writerow([str(d),source,cid,asai['source_campaign_id'],asai['source_publisher_id'],asai['source_section_id'],asai['publisher_name'],asai['name'],asai['ctr'],asai['ecpc'],asai['cost'],asai['cpa'],asai['icr']])    
                except KeyError:
                    print("sections unavailable for source " + source + " account id " + cid)
                print(str(d) + " ads data for source " + source + " account id " + cid + " done")

#requests data, returns in json format, records request id
def getdata(getstring, writer):
    conn = http.client.HTTPSConnection("api.brax.io")
    payload = "{}"
    headers = {'authorization':'Basic dnNodWxpbmE6UHVwc2lrSG9yc2UzNDU2Nw==', 'accept':'application/json', 'content-type':'application/json'}
    conn.request("GET", getstring, payload, headers)
    getres = conn.getresponse()

    #record request id
    writer.writerow([getres.getheader('x-request-id'), getstring])
    
    data = getres.read().decode("utf-8")
    jsonResponse = json.loads(data)
    return jsonResponse

#gets latest date from file
def get_last_date(csv_filename):
    with open(csv_filename, 'r', encoding='utf-8') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow[0]

if __name__ == '__main__':
    script_start = datetime.datetime.now()
    print("started at " + str(script_start))
    main()
    #how long did script take
    script_end = datetime.datetime.now()
    script_diff = script_end - script_start
    print("started at " + str(script_end))
    print("script took " + str(round(script_diff.total_seconds())) + " seconds")
