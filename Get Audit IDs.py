import http.client, json, csv

def main():
    conn = http.client.HTTPSConnection("api.observepoint.com")

    payload = "{}"

    headers = {'authorization':"api_key MTFhNGc0cHQzcnUzcGY3cHQ0czZiaGVmZnU4OXFyanBhZnJqY2VsdWtyOGNnNjNldW52NGVwdnFqZjAmMjMyMCYxNTAwNTYxMTg1NjA0"}

    #conn.request("GET", "/v2/web-audits/24138/runs/128023/results/pages", payload, headers)
    conn.request("GET", "/v2/web-audits", payload, headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    #print(data)

    jsonResponse = json.loads(data)
    ofile = open('AuditIDs.csv', 'w', newline='')
    csvwriter = csv.writer(ofile, delimiter=',')
    csvwriter.writerow(['Audit', 'ID'])

    for doc in jsonResponse:
        print(doc['name'], ':', doc['id'])
        csvwriter.writerow([doc['name'], doc['id']])
        

if __name__ == '__main__':
    main()


