from urllib import parse,request
import json

# post_data={"name": "haha", "age": "12"}
#     url='http://localhost:8080/asuka/actress/new'
def http_post(url, post_data):
    #json串数据使用
    # post_data = json.dumps(post_data).encode(encoding='utf-8')

    #普通数据使用
    post_data = parse.urlencode(post_data).encode(encoding='utf-8')
    print(post_data)

    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        "Content-Type": "application/x-www-form-urlencoded"
    }

    req = request.Request(url=url, data=post_data, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()

    print(res.decode(encoding='utf-8'))
