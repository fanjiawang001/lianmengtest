import requests
import pandas as pd
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from lianmengtest.database_test.database_test import database_test

class nozujianhua_all_saveuniv:
    def __init__(self):
        # 配置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # 创建 SQLAlchemy 引擎
        self.engine = create_engine(
            f'mysql+pymysql://{database_test().user}:{database_test().password}@{database_test().host}:{database_test().port}/{database_test().database}',pool_pre_ping=True)

        # 读取 CSV 文件
        # self.input_file = {
        #     '激励': {
        #         'nozujianhua': '../nozujianhua_jili_chaxunid.csv'
        #     },
        #     '插屏': {
        #         'nozujianhua': '../nozujianhua_chaping_chaxunid.csv'
        #     },
        #     '全屏': {
        #         'nozujianhua': '../nozujianhua_quanping_chaxunid.csv'
        #     },
        #     '开屏': {
        #         'nozujianhua': '../nozujianhua_kaiping_chaxunid.csv'
        #     },
        # }
        self.input_table = {
            '激励': {
                'nozujianhua': 'nozujianhua_jili_chaxunid'
            },
            '插屏': {
                'nozujianhua': 'nozujianhua_chaping_chaxunid'
            },
            '全屏': {
                'nozujianhua': 'nozujianhua_quanping_chaxunid'
            },
            '开屏': {
                'nozujianhua': 'nozujianhua_kaiping_chaxunid'
            },
        }
        # self.output_file = {
        #     '激励': {
        #         'nozujianhua': '../nozujianhua_jili_chaxunid_save.csv'
        #     },
        #     '插屏': {
        #         'nozujianhua': '../nozujianhua_chaping_chaxunid_save.csv'
        #     },
        #     '全屏': {
        #         'nozujianhua': '../nozujianhua_quanping_chaxunid_save.csv'
        #     },
        #     '开屏': {
        #         'nozujianhua': '../nozujianhua_kaiping_chaxunid_save.csv'
        #     },
        # }
        self.output_table = {
            '激励': {
                'nozujianhua': 'nozujianhua_jili_chaxunid_save'
            },
            '插屏': {
                'nozujianhua': 'nozujianhua_chaping_chaxunid_save'
            },
            '全屏': {
                'nozujianhua': 'nozujianhua_quanping_chaxunid_save'
            },
            '开屏': {
                'nozujianhua': 'nozujianhua_kaiping_chaxunid_save'
            },
        }

        # self.data = pd.read_csv(self.input_file['激励']['nozujianhua'])

        # 将 chaxunid 列转换为整数类型，处理无法转换的值为 NaN
        # self.data['chaxunid'] = pd.to_numeric(self.data['chaxunid'], errors='coerce').astype('Int64')

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
            'access-control-allow-headers': 'X-Requested-With,Content-Type',
            'access-control-allow-methods': 'PUT,POST,GET,DELETE,OPTIONS',
            'access-control-allow-origin': '*',
            'content-length': '0',
            'cookie': 'sidebarStatus=1; apdid=7dff22e0-9e72-4cf4-84a7-a707a82579f14a06b2face1fb7e22c76fd196e6d8b94:1732521392:1; hdige2wqwoino=cC6BSFkjjW65a3s6SxfHsJCGsdmbJBySee99eaf1; ehid=8fTTQ-souUdJYbpDSUafpjrd9_nQ3TITpUjJp; accessproxy_session=bc20f8d8-422f-47c2-b814-a2a7a2b3f646; apdid=337dc453-ea59-41fe-83cd-b16080e6d2b691abe41231c74e8a76868ea12fae3064:1739329758:1; accessproxy_session=a3131141-3e80-45da-8c46-2f0ba1d46ad8',
            'origin': 'https://adqa.test.gifshow.com',
            'priority': 'u=1, i',
            'referer': 'https://adqa.test.gifshow.com/union/autocase/case2',
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

    def fetch_response(self, dataid):
        """发送请求并返回解析后的响应"""
        url = f"https://adqa.test.gifshow.com/api/union/record/queryCaseAuto?dataids={dataid}&pageNo=1&pageSize=1"

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

    def process_dataid(self, index, row):
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
        for key, velue in self.input_table.items():
            print(f"开始缓存 {key} 的非组件化数据")
            # self.data = pd.read_csv(velue['nozujianhua'])
            self.data = pd.read_sql_table(velue['nozujianhua'], con=self.engine)
            # 将 chaxunid 列转换为整数类型，处理无法转换的值为 NaN
            self.data['chaxunid'] = pd.to_numeric(self.data['chaxunid'], errors='coerce').astype('Int64')
            # 使用线程池并发处理请求
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(self.process_dataid, index, row) for index, row in self.data.iterrows()]
                for future in futures:
                    future.result()  # 等待所有任务完成
            # 保存到新的 CSV 文件
            # self.data.to_csv(self.output_file[key]['nozujianhua'], index=False)
            # logging.info(f"数据已经保存到 {self.output_file[key]['nozujianhua']}")
            # 创建连接
            # 假设 self.engine 是你的 SQLAlchemy 引擎，self.output_table 是你的表名映射
            table_name = self.output_table[key]['nozujianhua']

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
            self.data.to_sql(self.output_table[key]['nozujianhua'], con=self.engine,if_exists='append', index=False)
            logging.info(f"数据已经保存到 {self.output_table[key]['nozujianhua']}")
            # 关闭数据库连接
            self.engine.dispose()
            print(f"缓存 {key} 的非组件化数据完成")

if __name__ == '__main__':
    nozujianhua_all_saveuniv().main()