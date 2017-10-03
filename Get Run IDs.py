import http.client, json, csv

def main():
    conn = http.client.HTTPSConnection("api.observepoint.com")

    payload = "{}"

    headers = {'authorization':"api_key MTFhNGc0cHQzcnUzcGY3cHQ0czZiaGVmZnU4OXFyanBhZ \
              nJqY2VsdWtyOGNnNjNldW52NGVwdnFqZjAmMjMyMCYxNTAwNTYxMTg1NjA0"}
    
    audits = ['21388','21376','21394','21386','21393','21374','21375','21371', \
              '21392','21387','21369','21385','21373','21377','21397','21389', \
              '21395','21396','21400','21390','24138']

    conn.request("GET", "/v2/web-audits/21388/runs/89926/results/variable/summary", payload, headers)
                 #"/v2/web-audits/21388"
                 #/runs/89926/results/tag-summaries"
                 #"/web-journeys/6234/runs/5116335/results"

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    #print(data)

    jsonResponse = json.loads(data)

    #print(jsonResponse)
    ofile = open('DataDump.csv', 'w', newline='')
    csvwriter = csv.writer(ofile, delimiter=',')
    #csvwriter.writerow(['Audit', 'ID'])

    with open('test.txt', 'w') as f:
        f.write(data)
        #for doc in jsonResponse:

        
        

if __name__ == '__main__':
    main()

