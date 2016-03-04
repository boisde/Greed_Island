import json
import requests

body = {
    "filter_col": ["id", "tel"],
    "query":
        {
            "op": "AND",
            "exprs": [
                {"id": {"in": [1,2,3]}},
            ]
        }
}
for _ in xrange(1000):
    resp = requests.post('http://127.0.0.1:3002/staff/complex_query/0', json=body)
    print resp

    print resp.json()