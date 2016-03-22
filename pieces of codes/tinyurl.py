import requests


def tiny_url(long_url):
    shorten_service_url = "http://dwz.cn/create.php"
    my_link = {"url": str(long_url)}
    resp = requests.post(url=shorten_service_url, data=my_link)
    resp = resp.json()
    if resp['status'] == 0:
        return resp["tinyurl"]
    else:
        raise ValueError('Shorten url=[%s] error, msg=[%s]' % (long_url, resp["err_msg"]))


if __name__ == "__main__":
    long = "http://data.123feng.com:8885"
    print tiny_url(long)
