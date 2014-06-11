import httplib, urllib

def doPost(url, json):
    params = urllib.urlencode(json)
    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
    connection = httplib.HTTPConnection(url)
    connection.request("POST", "/cgi-bin/query", params, headers)
    response = connection.getresponse()
    print response.status, response.reason

    data = response.read()
    connection.close()

if __name__ == '__main__':
    json_data = {'alice': 1, 'smartalice':2, 'stupidalice':0}
    url_port = "musi-cal.mojam.com:80"
    doPost(url_port, json_data)
