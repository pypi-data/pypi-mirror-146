import json
import sys

import numpy as np
import pandas as pd
import tornado.ioloop
import tornado.web

sys.path.append('../../../')
from autox import AutoXServerOpenmldb
import requests
import argparse

bst = None

# 原始表信息
table_schema = [
	("requestId", "string"),
	("cId", "string"),
	("cType", "string"),
	("cLabel", "string"),
	("cPubTime", "date"),
	("pRank", "double"),
	("pCount", "double"),
	("pServTime", "date"),
	("UUID", "string"),
	("pPlayPos", "double"),
	("unique_id", "bigint"),
]

url = ""

def get_schema():
    dict_schema = {}
    for i in table_schema:
        dict_schema[i[0]] = i[1]
    return dict_schema

dict_schema = get_schema()
json_schema = json.dumps(dict_schema)

def build_feature(r):
    pred_feas = pd.DataFrame([r], columns=autoxserver.G_hist['sql_final_used_cols'])
    pred_feas = pred_feas[autoxserver.G_hist['fe_lgb']['used_features']]
    pred_feas = pred_feas.astype(float)
    return np.array(pred_feas)

class SchemaHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json_schema)

class PredictHandler(tornado.web.RequestHandler):
    def post(self):
        row = json.loads(self.request.body)
        data = {}
        data["input"] = []
        row_data = []
        for i in table_schema:
            row_data.append(row[i[0]])
        data["input"].append(row_data)
        rs = requests.post(url, json=data)
        result = json.loads(rs.text)
        for r in result["data"]["data"]:
            ins = build_feature(r)
            self.write("----------------ins---------------\n")
            self.write(str(ins) + "\n")
            pred = bst.predict(ins)
            self.write("---------------predict -------------\n")
            self.write("%s"%str(pred[0]))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("real time execute sparksql demo")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/schema", SchemaHandler),
        (r"/predict", PredictHandler),
    ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint",  help="specify the endpoint of apiserver")
    parser.add_argument("save_path",  help="specify the save path")
    parser.add_argument("server_name",  help="specify the server_name")
    args = parser.parse_args()
    url = "http://%s/dbs/demo_db/deployments/demo_data_service" % args.endpoint

    autoxserver = AutoXServerOpenmldb(is_train=False, server_name=args.server_name)  # 注意server_name需要和训练时一致
    autoxserver.load_server(args.save_path)

    bst = autoxserver.G_hist['fe_lgb']['model']
    app = make_app()
    app.listen(8029)
    tornado.ioloop.IOLoop.current().start()

# endpoint = 172.24.4.62:8027
# save_path = /home/caihengxing/AutoX/autox/autox_server/demo/luoji/save_openmldb
# server_name = luoji

# ./start_predict_server.sh 172.24.4.62:8027 /home/caihengxing/AutoX/autox/autox_server/demo/luoji/save_openmldb luoji


