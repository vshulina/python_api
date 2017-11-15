from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.api import FacebookAdsApi
import datetime, csv, json

def main():
    #create file and csv writer objects, create header in csv file
    file = open('FB Ad Spend.csv', 'w', newline='', encoding='utf-8')
    csvwriter = csv.writer(file, delimiter=',')
    #header not needed after initial file creation
    csvwriter.writerow(['date','account id','account name','campaign id','campaign name','impressions','spend'])

    #set access details
    access_token = 'EAACtFzVjEfMBADkT0K7hqlAQrQ1cVOrEhXJfIyDR8egxCHNJBj9pAHvoiZCtvPwDr08jWLBzZCouolYgr04KIS3nmo3HL2sQGRavopO1iVsjmfUxQwoIcfFqnalYoOR7iG6lywIR2ZAKDO6Kw2cPzBVhtpC8074hgJ0Us0KkTR85F0ZBIkZAR'
    ad_account_id = 'act_299274085'
    app_secret = 'a1551a9ab4a24e97dd75da091e1c39a9'
    app_id = '190315191538163'

    #initialize
    FacebookAdsApi.init(access_token=access_token)

    #set date ranges
    start_date = datetime.date(2017, 9, 22)
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    day_count = (end_date - start_date).days + 1

    #set fields
    fields = [
    'campaign_id',
    'campaign_name',
    'account_id',
    'account_name',
    'ad_id',
    'impressions',
    'spend',]

    if start_date <= end_date:
        for d in (start_date + datetime.timedelta(n) for n in range(day_count)):
            print('date ' + str(d))
            #set fields to pull
            start = str(d)
            end = str(d)

            #set parameters
            params = {
                'level': 'campaign',
                'filtering': [],
                'breakdowns': [],
                'time_range': {'since':start,'until':end},
            }

            jsonData = AdAccount(ad_account_id).get_insights(fields=fields,params=params)

            try:
                for d in jsonData:
                    csvwriter.writerow([d['date_start'],d['account_id'],d['account_name'],d['campaign_id'], \
                                        d['campaign_name'],d['impressions'],d['spend']])
            except KeyError:
                print(jsonData)

if __name__ == '__main__':
    script_start = datetime.datetime.now()
    print("started at " + str(script_start))
    main()
    #how long did script take
    script_end = datetime.datetime.now()
    script_diff = script_end - script_start
    print("started at " + str(script_end))
    print("script took " + str(round(script_diff.total_seconds() / 60)) + "minutes"))
    
    
