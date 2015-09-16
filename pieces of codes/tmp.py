import requests
import json

# requests.post(url="http://10.171.99.129:5555/staff_info/complex_query/1",data=json.dumps({'query': {'exprs': [{'user': {'in': [7794662]}}], 'op': 'AND'}, 'filter_col': ['user', 'real_name']}))
requests.post(url="http://10.171.133.108:5555/staff_info/complex_query/1",data=json.dumps({'query': {'exprs': [{'user': {'in': [7794662]}}], 'op': 'AND'}, 'filter_col': ['user', 'real_name']}))