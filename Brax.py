import http.client, json, csv, math

def main():
    #get account ids
    jsonResponse = getdata("/v1/accounts")
    #create file and csv writer objects
    cfile = open('BraxCampaigns.csv', 'w', newline='')
    pfile = open('BraxPublishers.csv', 'w', newline='')
    afile = open('BraxAds.csv', 'w', newline='')
    ccsvwriter = csv.writer(cfile, delimiter=',')
    pcsvwriter = csv.writer(pfile, delimiter=',')
    acsvwriter = csv.writer(afile, delimiter=',')
    #create headers in csv files
    ccsvwriter.writerow(['source account id', 'source campaign id', 'campaign name', 'ctr', 'ecpc', 'cost', 'cpa', 'icr'])
    pcsvwriter.writerow(['source account id', 'source campaign id', 'source publisher id', 'publisher name', 'ctr', 'ecpc', 'cost', 'cpa', 'icr'])
    acsvwriter.writerow(['source account id', 'source campaign id', 'source ad id', 'tracking ad id', 'ctr', 'ecpc', 'cost', 'cpa', 'icr'])
    campaigns = []
    source_account_ids = []
    sources = []

    #store account ids and sources
    for camp in jsonResponse['results']:
        campaigns.append(camp['id'])
        source_account_ids.append(camp['source_account_id'])
        sources.append(camp['source'])

    #pull fields and write to csv file
    for source, cid in zip(sources, source_account_ids):
        
        dates = "&start_date=2017-08-20&end_date=2017-08-25"
        #campaign data
        cjsonResponse = getdata("/v1/reports/campaigns?source="+source+"&source_account_id="+cid+dates)
        for sai in cjsonResponse['results']:
            ccsvwriter.writerow([cid,sai['source_campaign_id'],sai['name'],sai['ctr'],sai['ecpc'],sai['cost'],sai['cpa'],sai['icr']])
        #publisher data
        count = 0
        offset = 0
        pagination = getdata("/v1/reports/publishers?source="+source+"&source_account_id="+cid+dates)
        pages = math.ceil(pagination['pagination']['total']/100)
        #pull all pages of the report
        while (count < pages):
            #print("count: " + str(count) + " offset: " + str(offset))
            pageParameter = "&offset=" + str(offset) + "&limit=100"
            pjsonResponse = getdata("/v1/reports/publishers?source="+source+"&source_account_id="+cid+dates+pageParameter)
            for psai in pjsonResponse['results']:
                pcsvwriter.writerow([cid,psai['source_campaign_id'],psai['source_publisher_id'],psai['name'],psai['ctr'],psai['ecpc'],psai['cost'],psai['cpa'],psai['icr']])
            offset = offset + 100
            count = count + 1
        #ads data
        ajsonResponse = getdata("/v1/reports/ads?source="+source+"&source_account_id="+cid+dates)
        for asai in ajsonResponse['results']:
            acsvwriter.writerow([cid,asai['source_campaign_id'],asai['source_ad_id'],asai['tracking_ad_id'],asai['ctr'],asai['ecpc'],asai['cost'],asai['cpa'],asai['icr']])    

#requests data, returns in json format
def getdata(getstring):
    conn = http.client.HTTPSConnection("api.brax.io")
    payload = "{}"
    headers = {'authorization':'Basic dnNodWxpbmE6UHVwc2lrSG9yc2UyMzQ1Ng==', 'accept':'application/json', 'content-type':'application/json'}
    conn.request("GET", getstring, payload, headers)
    getres = conn.getresponse()
    data = getres.read().decode("utf-8")
    jsonResponse = json.loads(data)
    return jsonResponse

if __name__ == '__main__':
    main()
