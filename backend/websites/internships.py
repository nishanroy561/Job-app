import http.client, json

def fetch_internships(api_key: str):
    conn = http.client.HTTPSConnection("internships-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "internships-api.p.rapidapi.com"
    }
    conn.request("GET", "/active-jb-7d", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
