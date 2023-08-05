import requests

url = "http://172.24.4.62:8029/predict"

req = {"requestId": "5847dd6453740990783204",
 "cId": "3792",
 "cType": "1.0",
 "cLabel": "9,14",
 "cPubTime": "2016-10-10",
 "pRank": 0.0,
 "pCount": 9.0,
 "pServTime": "2016-12-07",
 "UUID": "9cb98c94-cb66-11e6-8520-3c15c2c199c2",
 "pPlayPos": 1.0,
 "unique_id": 1
	   }

r = requests.post(url, json=req)
print(r.text)
