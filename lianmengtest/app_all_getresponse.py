import requests
import json
import pandas as pd
class app_all_getresponse:
    # 根据id获取广告数据
    def fetch_response(dataid,iszujianhua=False,issave=False,save_univ_csv=''):
        if not issave:
            if iszujianhua:
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
                """发送请求并返回解析后的响应"""
                url = f"https://adqa.test.gifshow.com/api/union/record/queryStyleCaseAuto?dataids={dataid}&pageNo=1&pageSize=1"
            else:
                headers = {
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
                """发送请求并返回解析后的响应"""
                url = f"https://adqa.test.gifshow.com/api/union/record/queryCaseAuto?dataids={dataid}&pageNo=1&pageSize=1"
            try:
                response = requests.post(url, headers=headers)
                response.raise_for_status()  # 检查响应状态
                response_data = response.json()
                if 'data' in response_data and 'list' in response_data['data'] and len(
                        response_data['data']['list']) > 0:
                    raw_response = response_data['data']['list'][0].get('response', None)
                    if raw_response is not None:
                        return json.loads(raw_response)  # 解析 JSON 字符串
                else:
                    print(f"Warning: No data found for dataid {dataid}")
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                print(f"Error: {e} for dataid {dataid}")
            return None
        else:
            """根据 dataid 获取响应数据"""
            if not dataid:
                print("查询 ID 为空")
                return None

            # 读取 saveuniv.csv 文件
            df_saveuniv = pd.read_csv(save_univ_csv)
            # 查找对应的 dataid
            row = df_saveuniv[df_saveuniv['chaxunid'] == int(dataid)]

            if not row.empty:
                # 获取 response 列的数据
                response_data = row['response'].values[0]
                if response_data is None or '':
                    print("响应数据为空")
                    return None
                if isinstance(response_data, (float, int)):
                    response_data = str(response_data)  # 确保 response_data 是字符串
                try:
                    # 尝试将 response 数据解析为 JSON
                    response_json = json.loads(response_data)
                    return response_json
                except json.JSONDecodeError:
                    print(f"解析 JSON 错误: {response_data}")
                    return None
            else:
                print(f"未找到 dataid: {dataid}")
                return None

    # 接口传mock数据至指定测试环境https://adqa.test.gifshow.com
    def send_compatibility_request(device_id, payload):
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
        'access-control-allow-headers': 'X-Requested-With,Content-Type',
        'access-control-allow-methods': 'PUT,POST,GET,DELETE,OPTIONS',
        'access-control-allow-origin': '*',
        'content-type': 'application/json',
        'cookie': 'your_cookie_here',  # 请根据需要替换为实际 cookie
        'origin': 'https://adqa.test.gifshow.com',
        'priority': 'u=1, i',
        'referer': 'https://adqa.test.gifshow.com/union/compatibility/compatibilitytest',
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
        """发送兼容性请求并返回结果"""
        url = f"https://adqa.test.gifshow.com/api/union/data/compatibility/setCompatibilityCase?deviceID={device_id}&isReplaceTK=True"
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result.get("success")
        else:
            print(f"Request error for device {device_id}, status code: {response.status_code}")
            return False