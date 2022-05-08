import time
import requests
import os
import  json
while True:
    evpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/img/'
    response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxc89ec0b61a9d8dae&secret=5c1e711a135a57233b60c4c27a22eda1', verify=False)  # 需填入appid和AppSecret
    print(response.json())
    with open(evpath+'access_token.json','w') as f:
        json.dump(response.json(),f)
    time.sleep(7200)