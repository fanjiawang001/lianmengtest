import json
import pandas as pd
import requests
class nozujianhua_all_getchaxunid:
    # 广告样式与对应的 CSV 文件路径
    adstyle_mapping = {
        "chaping": {"adstyle": "13", "csv": 'nozujianhua_chaping_chaxunid.csv'},
        "kaiping": {"adstyle": "4", "csv": 'nozujianhua_kaiping_chaxunid.csv'},
        "quanping": {"adstyle": "3", "csv": 'nozujianhua_quanping_chaxunid.csv'},
        "jili": {"adstyle": "2", "csv": 'nozujianhua_jili_chaxunid.csv'},
    }

    # 请求头
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
        'access-control-allow-headers': 'X-Requested-With,Content-Type',
        'access-control-allow-methods': 'PUT,POST,GET,DELETE,OPTIONS',
        'access-control-allow-origin': '*',
        'content-length': '0',
        'cookie': 'sidebarStatus=1; apdid=7dff22e0-9e72-4cf4-84a7-a707a82579f14a06b2face1fb7e22c76fd196e6d8b94:1732521392:1; hdige2wqwoino=cC6BSFkjjW65a3s6SxfHsJCGsdmbJBySee99eaf1; ehid=4Hp3buL_3GHFQPz6St-sFUAD8AcsNNPPYmiu3; accessproxy_session=56631f53-b924-4fa0-b0de-1ccb94b7938f; apdid=337dc453-ea59-41fe-83cd-b16080e6d2b691abe41231c74e8a76868ea12fae3064:1739329758:1; accessproxy_session=a3131141-3e80-45da-8c46-2f0ba1d46ad8',
        'origin': 'https://adqa.test.gifshow.com',
        'priority': 'u=1, i',
        'referer': 'https://adqa.test.gifshow.com/union/autocase/rules',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'trace-context': '{"laneId":"PRT.beta2"}',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'username': 'wb_fanjiawang'
    }

    def fetch_data(self,adstyle):
        """发送请求并获取数据"""
        url = f"https://adqa.test.gifshow.com/api/union/data/queryDataRuleInfo?interfaceType=1&adStyle={adstyle}&pageNo=1&pageSize=2000"
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data for adStyle {adstyle}: {e}")
            return None

    def process_response(self,response_result, csv_path):
        """处理响应数据并写入 CSV 文件"""
        if 'data' in response_result and 'list' in response_result['data']:
            chaxunid = [int(item['id']) for item in response_result['data']['list']]
            names = [item['description'] for item in response_result['data']['list']]

            # 打印总数
            print("Total items:", response_result['data']['total'])

            # 将数据写入 CSV 文件
            pageid = [None] * len(chaxunid)
            df = pd.DataFrame({'pageid': pageid, 'chaxunid': chaxunid, 'name': names})
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"Data written to {csv_path}")
        else:
            print("No data found in the response.")

    def main(self):
        for key, value in self.adstyle_mapping.items():
            print(f"Fetching data for {key}...")
            response_result = self.fetch_data(value['adstyle'])
            if response_result:
                self.process_response(response_result, value['csv'])

if __name__ == '__main__':
    nozujianhua_all_getchaxunid().main()