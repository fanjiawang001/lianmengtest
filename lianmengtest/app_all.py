import wx
import wx.grid
import pandas as pd
import json
from app_all_getresponse import app_all_getresponse
from nozujianhua.nozujianhua_all_getchaxunid import nozujianhua_all_getchaxunid
from zujianhua.zujianhua_all_getchaxunid import zujianhua_all_getchaxunid
from sqlalchemy import create_engine
from lianmengtest.database_test.database_test import database_test

engine = create_engine(
        f'mysql+pymysql://{database_test().user}:{database_test().password}@{database_test().host}:{database_test().port}/{database_test().database}')

android_device_ids = [
    "ANDROID_4d8eb9184c10f1c3",
    'ANDROID_06281416577b28d8'
]
ios_device_ids = [
    "IDFA_9733E8B8-2590-4152-B982-C68AA07FBCAA",
    "IDFA_D27ECE36-B1E2-4229-BDB0-C308663D964A"
]
read_csvs={
    '激励':{
        'zujianhua':'zujianhua_jili_shaixuanid',
        'nozujianhua':'nozujianhua_jili_chaxunid'
    },
    '插屏':{
        'zujianhua':'zujianhua_chaping_shaixuanid',
        'nozujianhua':'nozujianhua_chaping_chaxunid'
    },
    '全屏':{
        'zujianhua': 'zujianhua_quanping_shaixuanid',
        'nozujianhua': 'nozujianhua_quanping_chaxunid'
    },
    '开屏':{
        'zujianhua': 'zujianhua_kaiping_shaixuanid',
        'nozujianhua': 'nozujianhua_kaiping_chaxunid'
    },
}
save_univ_csvs = {
    '激励':{
        'zujianhua':'zujianhua_jili_shaixuanid_save.csv',
        'nozujianhua':'nozujianhua_jili_chaxunid_save.csv'
    },
    '插屏':{
        'zujianhua':'zujianhua_chaping_shaixuanid_save.csv',
        'nozujianhua':'nozujianhua_chaping_chaxunid_save.csv'
    },
    '全屏':{
        'zujianhua': 'zujianhua_quanping_shaixuanid_save.csv',
        'nozujianhua': 'nozujianhua_quanping_chaxunid_save.csv'
    },
    '开屏':{
        'zujianhua': 'zujianhua_kaiping_shaixuanid_save.csv',
        'nozujianhua': 'nozujianhua_kaiping_chaxunid_save.csv'
    },
}

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='联盟SDK测试')
        # 初始化实例变量

        self.read_csv_zujianhua = 'zujianhua_jili_shaixuanid'
        self.read_csv_nozujianhua = 'nozujianhua_jili_chaxunid'
        self.save_univ_csv_zujianhua = 'zujianhua_jili_shaixuanid_save'
        self.save_univ_csv_nozujianhua = 'nozujianhua_jili_chaxunid_save'

        self.iszujianhua = False
        self.issave = False
        self.save_univ_csv = ''
        self.adstyle='激励'
        self.biaoge_data = None

        # 创建面板和布局
        self.panel = wx.Panel(self)
        # 创建垂直布局
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        # 创建水平布局
        self.hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # 创建下拉菜单
        self.choice = wx.Choice(self.panel, choices=[f"{key}" for key in read_csvs.keys()])
        self.choice.Bind(wx.EVT_CHOICE, self.on_choice_select)
        # 创建搜索框提示词
        self.search_label = wx.StaticText(self.panel, label="搜索框", style=wx.ALIGN_RIGHT)
        # 创建搜索框
        self.search_box = wx.TextCtrl(self.panel,size=(200, 20))
        self.search_box.Bind(wx.EVT_TEXT, self.on_search)
        # 创建按钮
        self.load_button_renewzujianhuaid = wx.Button(self.panel, label='更新组件化id列表')
        self.load_button_renewnozujianhuaid = wx.Button(self.panel, label='更新非组件化id列表')
        self.load_button_zujianhua = wx.Button(self.panel, label='加载组件化id列表')
        self.load_button_nozujianhua = wx.Button(self.panel, label='加载非组件化id列表')
        self.load_button_savezujianhua = wx.Button(self.panel, label='加载已保存组件化数据列表')
        self.load_button_savenozujianhua = wx.Button(self.panel, label='加载已保存非组件化数据列表')
        self.load_button_renewnozujianhuaid.Bind(wx.EVT_BUTTON, lambda event: self.renew_nozujianhuaid(event))
        self.load_button_renewzujianhuaid.Bind(wx.EVT_BUTTON, lambda event: self.renew_zujianhuaid(event))
        self.load_button_zujianhua.Bind(wx.EVT_BUTTON, lambda event: self.on_load_csv(event, iszujianhua=1))
        self.load_button_nozujianhua.Bind(wx.EVT_BUTTON, lambda event: self.on_load_csv(event, iszujianhua=2))
        self.load_button_savezujianhua.Bind(wx.EVT_BUTTON, lambda event: self.on_load_csv(event, iszujianhua=3))
        self.load_button_savenozujianhua.Bind(wx.EVT_BUTTON, lambda event: self.on_load_csv(event, iszujianhua=4))
        # 创建表格
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(0, 5)  # 初始时创建 0 行 5 列
        # 设置列标题
        self.grid.SetColLabelValue(0, 'pageid')
        self.grid.SetColLabelValue(1, 'chaxunid')
        self.grid.SetColLabelValue(2, 'name')
        self.grid.SetColLabelValue(3, 'Action')
        self.grid.SetColLabelValue(4, 'Response')
        # 设置滚动条
        self.grid.EnableScrolling(True, True)
        # 绑定鼠标点击事件
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_cell_click)
        # 将按钮添加水平布局第一行
        self.hbox0.Add(self.choice, 0, wx.ALL | wx.LEFT, 5)
        self.hbox0.Add(self.load_button_renewzujianhuaid, 0, wx.ALL | wx.LEFT, 5)
        self.hbox0.Add(self.load_button_renewnozujianhuaid, 0, wx.ALL | wx.LEFT, 5)
        # 将按钮添加到水平布局第二行
        self.hbox1.Add(self.load_button_zujianhua, 0, wx.ALL | wx.LEFT, 5)
        self.hbox1.Add(self.load_button_nozujianhua, 0, wx.ALL | wx.LEFT, 5)
        self.hbox1.Add(self.load_button_savezujianhua, 0, wx.ALL | wx.LEFT, 5)
        self.hbox1.Add(self.load_button_savenozujianhua, 0, wx.ALL | wx.LEFT, 5)
        # 将搜索框添加到水平布局第三行
        self.hbox2.Add(self.search_label, 0, wx.ALL | wx.LEFT, 5)
        self.hbox2.Add(self.search_box, 0, wx.ALL | wx.LEFT, 5)
        # 将水平布局添加到垂直布局
        self.vbox.Add(self.hbox0, 0, wx.EXPAND | wx.ALL, 5)
        self.vbox.Add(self.hbox1, 0, wx.EXPAND | wx.ALL, 5)
        self.vbox.Add(self.hbox2, 0, wx.EXPAND | wx.ALL, 5)
        self.vbox.Add(self.grid, 0, wx.EXPAND | wx.ALL, 5)
        # 将垂直布局添加到 Panel
        self.panel.SetSizer(self.vbox)
        # 调用 tiaozhengbuju() 方法调整布局
        self.tiaozhengbuju()
        # 显示 Frame
        self.Show()

    def tiaozhengbuju(self):
        # 表格自动调整
        self.grid.AutoSize()
        self.panel.SetMinSize((750, 100))  # 设置最小高度为 200 像素
        self.panel.SetMaxSize((750, 600))  # 设置最大高度为 600 像素
        # 调用 Fit() 方法使 Panel 自适应
        self.panel.Fit()
        # 调用 Layout() 方法确保布局正确
        self.panel.Layout()
        # 调整 Frame 的大小以适应 Panel 的内容
        self.Fit()
        # 调用 Layout() 方法确保布局正确
        self.Layout()

    def renew_nozujianhuaid(self, event):
        nozujianhua_all_getchaxunid().main()
        wx.MessageBox("非组件id更新完成", "Success", wx.OK | wx.ICON_INFORMATION)
    def renew_zujianhuaid(self, event):
        zujianhua_all_getchaxunid().main()
        wx.MessageBox("组件id更新完成", "Success", wx.OK | wx.ICON_INFORMATION)
    def on_choice_select(self, event):
        # 获取选择的值
        selected_key = self.choice.GetString(self.choice.GetSelection())
        self.adstyle = selected_key
        print(f'当前指定广告为：{self.adstyle}')
        # 根据选择的值设置 CSV 文件路径
        self.read_csv_zujianhua = read_csvs[selected_key]['zujianhua']
        self.read_csv_nozujianhua = read_csvs[selected_key]['nozujianhua']
        self.save_univ_csv_zujianhua = save_univ_csvs[selected_key]['zujianhua']
        self.save_univ_csv_nozujianhua = save_univ_csvs[selected_key]['nozujianhua']
        print(f"指定的组件化文件：{self.read_csv_zujianhua}\n指定的非组件文件：{self.read_csv_nozujianhua}\n指定保存的组件化文件：{self.save_univ_csv_zujianhua}\n指定保存的非组件化文件：{self.save_univ_csv_nozujianhua}")

    def on_search(self, event):
        # 获取搜索框中的值
        search_text = self.search_box.GetValue().strip()  # 使用 strip() 移除首尾可能存在的空格
        # 根据搜索框中的值过滤表格数据
        if search_text:
            self.biaoge_data_search = self.biaoge_data[
                self.biaoge_data['name'].str.contains(search_text, case=False, na=False)]
        else:
            self.biaoge_data_search = self.biaoge_data.copy()  # 如果没有搜索文本，则显示所有数据

        # 重置索引
        self.biaoge_data_search.reset_index(drop=True, inplace=True)

        # 打印搜索结果，以便检查数据是否正确
        print("筛选结果:")
        print(self.biaoge_data_search)

        # 清空表格并重新创建
        self.grid.ClearGrid()

        # 检查当前行数，删除现有行
        num_rows = self.grid.GetNumberRows()
        if num_rows > 0:
            self.grid.DeleteRows(0, num_rows)  # 删除现有行

        # 创建新的表格行
        num_new_rows = len(self.biaoge_data_search)
        if num_new_rows > 0:
            self.grid.AppendRows(num_new_rows)  # 添加新行

        # 打印添加新行后的行数，以便确认行数是否正确
        print(f"筛选后的数据行数: {self.grid.GetNumberRows()}")

        # 设置新的数据
        for index, row in self.biaoge_data_search.iterrows():
            if index < self.grid.GetNumberRows():  # 确保索引在有效范围内
                self.grid.SetCellValue(index, 0, str(row['pageid']))  # pageid 作为字符串
                # 检查 chaxunid 是否为 NaN
                if pd.isna(row['chaxunid']):
                    self.grid.SetCellValue(index, 1, '')  # 或者设置为 'N/A' 或其他默认值
                else:
                    self.grid.SetCellValue(index, 1, str(int(row['chaxunid'])))  # 将 chaxunid 转换为整数并转为字符串

                self.grid.SetCellValue(index, 2, str(row['name']))
                self.grid.SetCellValue(index, 3, 'Send Request')  # 显示按钮文本
        self.tiaozhengbuju()

    def on_load_csv(self, event, iszujianhua):
        try:
            # 读取 CSV 文件
            if iszujianhua == 1:
                # df = pd.read_csv(self.read_csv_zujianhua)
                df = pd.read_sql_table(self.read_csv_zujianhua, con=engine)
                engine.dispose()
                self.iszujianhua = True
                self.issave = False
                self.save_univ_csv = ''
            elif iszujianhua == 2:
                # df = pd.read_csv(self.read_csv_nozujianhua)
                df = pd.read_sql_table(self.read_csv_nozujianhua, con=engine)
                engine.dispose()
                self.iszujianhua = False
                self.issave = False
                self.save_univ_csv = ''
            elif iszujianhua == 3:
                df = pd.read_csv(self.save_univ_csv_zujianhua)
                # df = pd.read_sql_table(self.save_univ_csv_zujianhua, con=engine)
                # engine.dispose()
                self.iszujianhua = True
                self.issave = True
                self.save_univ_csv = self.save_univ_csv_zujianhua
            elif iszujianhua == 4:
                df = pd.read_csv(self.save_univ_csv_nozujianhua)
                # df = pd.read_sql_table(self.save_univ_csv_nozujianhua, con=engine)
                # engine.dispose()
                self.iszujianhua = False
                self.issave = True
                self.save_univ_csv = self.save_univ_csv_nozujianhua
        except FileNotFoundError:
            wx.MessageBox("CSV 文件未找到", "Error", wx.OK | wx.ICON_ERROR)
            self.grid.ClearGrid()
            return
        except pd.errors.EmptyDataError:
            wx.MessageBox("CSV 文件是空的", "Error", wx.OK | wx.ICON_ERROR)
            self.grid.ClearGrid()
            return
        except pd.errors.ParserError:
            wx.MessageBox("CSV 文件格式错误", "Error", wx.OK | wx.ICON_ERROR)
            self.grid.ClearGrid()
            return
        except Exception as e:
            wx.MessageBox(f"发生了未知错误: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            self.grid.ClearGrid()
            return
        # df数据保存至全局变量self.biaoge_data中
        self.biaoge_data = df
        # 清空表格并重新创建
        self.grid.ClearGrid()

        # 检查当前行数，删除现有行
        num_rows = self.grid.GetNumberRows()
        if num_rows > 0:
            self.grid.DeleteRows(0, num_rows)  # 删除现有行

        # 创建新的表格行
        self.grid.AppendRows(len(df))  # 添加新行

        for index, row in df.iterrows():
            self.grid.SetCellValue(index, 0, str(row['pageid']))  # pageid 作为字符串

            # 检查 chaxunid 是否为 NaN
            if pd.isna(row['chaxunid']):
                self.grid.SetCellValue(index, 1, '')  # 或者设置为 'N/A' 或其他默认值
            else:
                self.grid.SetCellValue(index, 1, str(int(row['chaxunid'])))  # 将 chaxunid 转换为整数并转为字符串

            self.grid.SetCellValue(index, 2, str(row['name']))
            self.grid.SetCellValue(index, 3, 'Send Request')  # 显示按钮文本

        self.tiaozhengbuju()

    def on_cell_click(self, event):
        row = event.GetRow()
        col = event.GetCol()

        # 检查是否点击了 Action 列
        if col == 3:  # Action 列
            chaxunid = self.grid.GetCellValue(row, 1)  # 获取 chaxunid
            if not chaxunid:
                wx.MessageBox("查询 ID 为空", "Error", wx.OK | wx.ICON_ERROR)
                self.grid.SetCellValue(row, 4, "查询 ID 为空")
                return
            print(f"chaxunid: {chaxunid},iszujianhua: {self.iszujianhua},issave: {self.issave},save_univ_csv: {self.save_univ_csv}")
            response_value = app_all_getresponse.fetch_response(chaxunid, iszujianhua=self.iszujianhua, issave=self.issave, save_univ_csv=self.save_univ_csv)
            if response_value is not None:
                # 确保 response_value 为字符串
                response_value_str = json.dumps(response_value, ensure_ascii=False)  # 转义并转换为字符串
                print(response_value_str)

                # 定义 payload
                payload = {
                    "id": 1,
                    "caseId": 90355,
                    "caseNo": 1,
                    "caseName": "插屏",
                    "adstyle": 13,
                    "dataids": chaxunid,
                    "labelid": None,
                    "platform": 0,
                    "createTime": 1735005144264,
                    "request": None,
                    "response": response_value_str  # 使用转换后的字符串
                }

                # 发送请求并检查结果
                android_results = []
                for android_device_id in android_device_ids:
                    android_result = app_all_getresponse.send_compatibility_request(android_device_id, payload)
                    android_results.append(android_result)

                ios_results = []
                for ios_device_id in ios_device_ids:
                    ios_result = app_all_getresponse.send_compatibility_request(ios_device_id, payload)
                    ios_results.append(ios_result)

                if all(android_results) and all(ios_results):
                    self.grid.SetCellValue(row, 4, "请求成功")
                elif any(android_results):
                    self.grid.SetCellValue(row, 4, "Android 请求成功，iOS 请求失败")
                elif any(ios_results):
                    self.grid.SetCellValue(row, 4, "Android 请求失败，iOS 请求成功")
                else:
                    self.grid.SetCellValue(row, 4, "请求失败")
            else:
                wx.MessageBox("未能获取有效的响应数据", "Error", wx.OK | wx.ICON_ERROR)
                self.grid.SetCellValue(row, 4, "没有数据")

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()