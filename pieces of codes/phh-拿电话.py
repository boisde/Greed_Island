# encoding=utf-8
import re
import requests

url = "http://express.yqphh.com/login"
payload = {'username': 'fxs1', 'password': 'i6l01v', 'return_url':'', 'act':'signin'}
with requests.session() as s:
    # fetch the login page
    s.get(url)
    print(s.cookies)

    # post to the login form
    s.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    print(s.cookies)

    url2 = 'http://express.yqphh.com/shipmentDetail?tracking_number=000000064513'
    r = s.get(url2)
    # print(r.text)
    raw = r.text

# raw = """
# 	            <tbody>
# 	                <tr>
# 	                	<td>000000064513</td>
# 	                	<td>风先生</td>
# 	                    <td>朱琴琴</td>
# 	                    <td>13738229699</td>
# 	                    <td>浙江</td>
# 	                    <td>杭州</td>
# 	                    <td>拱墅区</td>
# 	                    <td>定海西园21幢1单元303</td>
# 	                </tr>
# 	            </tbody>
# """
raw = ''.join(raw.split())
m = re.search(r"(?<=<tbody><tr>)(.*)(?=</tr></tbody>)", raw)
tbody = m.group(0)
print tbody
m = re.findall(r"(?<=<td>)(.*?)(?=</td>)", tbody)
for item in m:
	print item



