import requests
import pandas as pd
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from lianmengtest.database_test.database_test import database_test

class zujianhua_all_saveuniv:
    def __init__(self):
        # 配置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # 创建 SQLAlchemy 引擎
        self.engine = create_engine(
            f'mysql+pymysql://{database_test().user}:{database_test().password}@{database_test().host}:{database_test().port}/{database_test().database}',
            pool_pre_ping=True)

        # 读取 CSV 文件
        # self.input_file = {
        #     '激励':{
        #         'zujianhua':'../zujianhua_jili_shaixuanid.csv'
        #     },
        #     '插屏':{
        #         'zujianhua':'../zujianhua_chaping_shaixuanid.csv'
        #     },
        #     '全屏':{
        #         'zujianhua': '../zujianhua_quanping_shaixuanid.csv'
        #     },
        #     '开屏':{
        #         'zujianhua': '../zujianhua_kaiping_shaixuanid.csv'
        #     },
        # }
        self.input_table = {
            # '激励': {
            #     'zujianhua': 'zujianhua_jili_shaixuanid'
            # },
            '插屏': {
                'zujianhua': 'zujianhua_chaping_shaixuanid'
            },
            '全屏': {
                'zujianhua': 'zujianhua_quanping_shaixuanid'
            },
            '开屏': {
                'zujianhua': 'zujianhua_kaiping_shaixuanid'
            },
        }
        # self.output_file = {
        #     '激励':{
        #         'zujianhua':'../zujianhua_jili_shaixuanid_save.csv'
        #     },
        #     '插屏':{
        #         'zujianhua':'../zujianhua_chaping_shaixuanid_save.csv'
        #     },
        #     '全屏':{
        #         'zujianhua': '../zujianhua_quanping_shaixuanid_save.csv'
        #     },
        #     '开屏':{
        #         'zujianhua': '../zujianhua_kaiping_shaixuanid_save.csv'
        #     },
        # }
        self.output_table = {
            '激励': {
                'zujianhua': 'zujianhua_jili_shaixuanid_save'
            },
            '插屏': {
                'zujianhua': 'zujianhua_chaping_shaixuanid_save'
            },
            '全屏': {
                'zujianhua': 'zujianhua_quanping_shaixuanid_save'
            },
            '开屏': {
                'zujianhua': 'zujianhua_kaiping_shaixuanid_save'
            },
        }

        self.headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
                'access-control-allow-headers': 'X-Requested-With,Content-Type',
                'access-control-allow-methods': 'PUT,POST,GET,DELETE,OPTIONS',
                'access-control-allow-origin': '*',
                'content-length': '0',
                'cookie': 'your_cookie_here',  # 请根据需要替换为实际 cookie
                'origin': 'https://adqa.test.gifshow.com',
                'priority': 'u=1, i',
                'referer': 'https://adqa.test.gifshow.com/union/autocase/case3',
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

    def fetch_response(self,dataid):
        """发送请求并返回解析后的响应"""
        url = f"https://adqa.test.gifshow.com/api/union/record/queryStyleCaseAuto?dataids={dataid}&pageNo=1&pageSize=1"

        try:
            response = requests.post(url, headers=self.headers)
            print(response.status_code)
            response.raise_for_status()  # 检查响应状态
            response_data = response.json()

            # 确保 data.list 存在且有元素
            if 'data' in response_data and 'list' in response_data['data'] and len(response_data['data']['list']) > 0:
                raw_response = response_data['data']['list'][0].get('response', None)
                if raw_response is not None:
                    return json.loads(raw_response)  # 解析 JSON 字符串
            else:
                logging.warning(f"No data found for dataid {dataid}")
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            logging.error(f"Error: {e} for dataid {dataid}")
        return None

    def process_dataid(self,index, row):
        """处理单个 dataid 并更新 DataFrame"""
        dataid = row['chaxunid']
        response_value = self.fetch_response(dataid)
        if response_value is not None:
            self.data.at[index, 'response'] = json.dumps(response_value)  # 将 JSON 数据转换为字符串
            logging.info(f"已保存 {dataid} 的数据")
            print(f"已保存 {dataid} 的数据")
        else:
            logging.warning(f"未找到 {dataid} 的数据")

    def main(self):
        for key,velue in self.input_table.items():
            print(f"开始缓存 {key} 的组件化数据")
            # self.data = pd.read_csv(velue['zujianhua'])
            self.data = pd.read_sql_table(velue['zujianhua'], con=self.engine)
            # 将 chaxunid 列转换为整数类型，处理无法转换的值为 NaN
            self.data['chaxunid'] = pd.to_numeric(self.data['chaxunid'], errors='coerce').astype('Int64')
            # 使用线程池并发处理请求
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(self.process_dataid, index, row) for index, row in self.data.iterrows()]
                for future in futures:
                    future.result()  # 等待所有任务完成
            # 保存到新的 CSV 文件
            # self.data.to_csv(self.output_file[key]['zujianhua'], index=False)
            # logging.info(f"数据已经保存到 {self.output_file[key]['zujianhua']}")
            # 创建连接
            # 假设 self.engine 是你的 SQLAlchemy 引擎，self.output_table 是你的表名映射
            table_name = self.output_table[key]['zujianhua']

            # 确保表名是安全的
            safe_table_name = f"`{table_name}`"  # 使用反引号以防止特殊字符问题

            with self.engine.connect() as connection:
                try:
                    # 创建表，如果表已存在则会被替换
                    connection.execute(text(f"""
                             CREATE TABLE IF NOT EXISTS {safe_table_name} (
                                 pageid TEXT,
                                 chaxunid BIGINT,
                                 name TEXT,
                                 response LONGTEXT
                             );
                         """))

                    # 清空表中的数据
                    connection.execute(text(f"DELETE FROM {safe_table_name};"))

                except Exception as e:
                    print(f"Error occurred while creating or clearing table: {e}")

            # 保存到新的 SQL 表
            self.data.to_sql(self.output_table[key]['zujianhua'], con=self.engine, if_exists='append',
                             index=False)
            logging.info(f"数据已经保存到 {self.output_table[key]['zujianhua']}")
            # 关闭数据库连接
            self.engine.dispose()
            print(f"缓存 {key} 的组件化数据完成")
if __name__ == '__main__':
    zujianhua_all_saveuniv().main()