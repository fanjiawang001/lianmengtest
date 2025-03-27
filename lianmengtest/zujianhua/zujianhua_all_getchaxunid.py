import requests
import pandas as pd
import json
from sqlalchemy import create_engine
from lianmengtest.database_test.database_test import database_test

class zujianhua_all_getchaxunid:
    # 创建 SQLAlchemy 引擎
    engine = create_engine(
        f'mysql+pymysql://{database_test().user}:{database_test().password}@{database_test().host}:{database_test().port}/{database_test().database}')

    def getpageid(self):
        # 假设你已经将 JSON 数据保存在一个文件中，文件名为 kconf.json
        json_file_path = 'lianmengtest/zujianhua/zujianhua_mobankconf.json'

        # 读取 JSON 数据
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print('长度',len(data))

        # 提取所需的键和值
        records = []
        for key, value in data.items():
            if value["status"]==1:
                records.append({
                    'pageid': key,
                    'name': value['name']
            })
        print('status:1,长度',len(records))
        # 创建 DataFrame
        df = pd.DataFrame(records)

        # 将 DataFrame 保存为 CSV 文件
        csv_file_path = 'zujianhua_getpageid.csv'
        df.to_csv(csv_file_path, index=False)

        print(f"数据已成功保存至 {csv_file_path}")
        # 将数据写入数据库
        df.to_sql(name='zujianhua_getpageid', con=self.engine, if_exists='replace', index=False)
        print(f"Data written to table: zujianhua_getpageid")
        # self.engine.dispose()

    def getchaxunid(self):
        # 读取 CSV 文件并获取 pageid 和 name 列
        # data = pd.read_csv('zujianhua_getpageid.csv')
        # 读取数据库的表zujianhua_getpageid
        data = pd.read_sql_table('zujianhua_getpageid', self.engine)

        pageid_list = data['pageid'].tolist()  # 将 pageid 列转换为列表
        name_list = data['name'].tolist()  # 将 name 列转换为列表

        # 用于存储返回结果的查询 ID
        chaxunid_list = []

        # 请求头（确保在代码中定义 headers）
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
            'access-control-allow-headers': 'X-Requested-With,Content-Type',
            'access-control-allow-methods': 'PUT,POST,GET,DELETE,OPTIONS',
            'access-control-allow-origin': '*',
            'content-length': '0',
            'cookie': 'your_cookie_here',  # 请根据需要替换为实际 cookie
            'origin': 'https://adqa.test.gifshow.com',
            'priority': 'u=1, i',
            'referer': 'https://adqa.test.gifshow.com/union/autocase/stylerules',
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

        # 循环遍历 pageid_list 数组
        for pageid in pageid_list:
            # 替换 URL 中的 labellist 值
            url = f"https://adqa.test.gifshow.com/api/union/data/queryStyleDataRuleInfo?labellist={pageid}&pageNo=1&pageSize=1"

            try:
                # 发送请求
                response = requests.post(url, headers=headers)

                # 检查响应状态
                response.raise_for_status()  # 如果响应状态码为 4xx 或 5xx，会抛出异常

                # 解析 JSON 响应
                response_data = response.json()

                # 确保 data.list 存在并且有元素
                if 'data' in response_data and 'list' in response_data['data'] and len(
                        response_data['data']['list']) > 0:
                    # 获取 data.list[0].id
                    item_id = response_data['data']['list'][0]['id']
                    chaxunid_list.append(int(item_id))  # 确保将 ID 转换为整数
                else:
                    print(f"Warning: No data found for pageid {pageid}")
                    chaxunid_list.append(None)  # 如果没有数据，添加 None 以保持索引一致

            except requests.exceptions.RequestException as e:
                print(f"Error: {e} for pageid {pageid}")
                chaxunid_list.append(None)  # 如果请求失败，添加 None 以保持索引一致

        # 将结果保存到 DataFrame
        result_df = pd.DataFrame({
            'pageid': pageid_list,  # 直接使用 pageid_list
            'chaxunid': chaxunid_list,  # 直接使用 chaxunid_list
            'name': name_list,
        })

        # 确保 chaxunid 列为整数，使用 astype(int) 方法
        result_df['chaxunid'] = result_df['chaxunid'].astype('Int64')  # 使用 'Int64' 以允许 None 值

        # 将结果保存到新的 CSV 文件
        result_df.to_csv("zujianhua_getchaxunid.csv", index=False)
        print(f"数据已成功保存至 zujianhua_getchaxunid.csv")
        # 将数据写入数据库
        result_df.to_sql(name='zujianhua_getchaxunid', con=self.engine, if_exists='replace', index=False)
        print(f"Data written to table: zujianhua_getchaxunid")
        # self.engine.dispose()

        # 输出结果
        print("Collected IDs:", chaxunid_list)


    def getshaixuanid(self):
        # 筛选条件及其对应的输出文件路径
        shaixuan_config = {
            "chaping": {
                "num": "313",
                "csv": 'zujianhua_chaping_shaixuanid.csv',
                "table":'zujianhua_chaping_shaixuanid'
            },
            "kaiping": {
                "num": "304",
                "csv": 'zujianhua_kaiping_shaixuanid.csv',
                "table": 'zujianhua_kaiping_shaixuanid'
            },
            "quanping": {
                "num": "303",
                "csv": 'zujianhua_quanping_shaixuanid.csv',
                "table": 'zujianhua_quanping_shaixuanid'
            },
            "jili": {
                "num": "300",
                "csv": 'zujianhua_jili_shaixuanid.csv',
                "table": 'zujianhua_jili_shaixuanid'
            }
        }

        # input_file_path = 'zujianhua_getchaxunid.csv'  # 输入文件路径
        """根据给定的筛选条件筛选数据并保存结果"""
        # 读取 CSV 文件
        # df = pd.read_csv(input_file_path)
        # 读取数据库的表zujianhua_getchaxunid
        df = pd.read_sql_table('zujianhua_getchaxunid', self.engine)
        if df is None:
            return  # 如果读取失败，直接返回
        for key in shaixuan_config.keys():
            # 筛选 pageid 前三位为指定值的数据
            filtered_df = df[df['pageid'].astype(str).str.startswith(shaixuan_config[key]['num'])]

            # 选择要保存的列
            result_df = filtered_df[['pageid', 'chaxunid', 'name']].copy()

            # 将 chaxunid 列转换为整数类型，处理无法转换的值为 NaN
            result_df['chaxunid'] = pd.to_numeric(result_df['chaxunid'], errors='coerce').astype('Int64')

            # 保存到新的 CSV 文件
            result_df.to_csv(shaixuan_config[key]['csv'], index=False)
            print('共',len(result_df['chaxunid']),'条数据','已写入', shaixuan_config[key]['csv'], '文件')
            # 将数据写入数据库
            result_df.to_sql(name=shaixuan_config[key]['table'], con=self.engine, if_exists='replace', index=False)
            print(f"Data written to table: {shaixuan_config[key]['table']}")
            # self.engine.dispose()


    def main(self):
        """主函数，遍历所有筛选条件并执行筛选操作"""
        self.getpageid()
        self.getchaxunid()
        self.getshaixuanid()
        self.engine.dispose()

if __name__ == '__main__':
    zujianhua_all_getchaxunid().main()