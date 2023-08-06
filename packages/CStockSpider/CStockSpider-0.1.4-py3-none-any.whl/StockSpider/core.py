# Insert your code here. 
import requests
import pandas as pd


class StockSpider:
    """
    爬取股票交易信息。
    """
    def __init__(self):
        """
        对象参数成员：
            url1：接口url
            default_params1：数据属性
        """
        self.encoding = "GBK"
        self.url1 = "http://quotes.money.163.com/service/chddata.html"
        self.default_params1 = ["TCLOSE", "HIGH", "LOW", "TOPEN", "LCLOSE", "CHG", "PCHG", "TURNOVER", "VOTURNOVER", "VATURNOVER", "TCAP", "MCAP"]

    def get(self, exchange, code, start, end, params=None):
        """
        获取历史（按日）交易信息
        :param exchange: 交易所信息  数据类型：int   交易所信息 0：上证交易所；1：深圳交易所
        :param code: 股票代码   数据类型：str
        :param start: 开始日期  数据类型：str    格式：yyyyMMdd
        :param end: 结束日期    数据类型：str    格式：yyyyMMdd
        :param params: 访问数据类型   数据类型：List[str]
            TCLOSE: 收盘价
            HIGH: 当日最高
            LOW: 当日最低
            TOPEN: 开盘价
            LCLOSE: 前收盘
            CHG: 涨跌额
            PCHG: 涨跌幅
            TURNOVER: 换手率
            VATURNOVER: 成交量
            VOTURNOVER: 成交金额
            TCAP: 总市值
            MCAP: 流通市值

        :return: DataFrame对象
        """
        if not params:
            params = self.default_params1
        query = {
            "code": str(exchange) + code,
            "start": start,
            "end": end,
            "fields": ";".join(params)
        }
        response = requests.get(self.url1, params=query)
        response.encoding = self.encoding

        # 处理数据格式
        text_ls = response.text.split(sep='\n')
        new_ls = []
        for i in text_ls:
            new_ls.append(i.split(','))

        columns = new_ls[0]
        columns[-1] = columns[-1][:-1]
        new_ls.pop(-1)
        data = new_ls[:0:-1]
        for i in range(len(data)):
            data[i][-1] = data[i][-1][:-1]
        df = pd.DataFrame(data=data, columns=columns)
        return df

class smSpider:
    """
    获取报表（Statement）信息
    """

    def __init__(self):
        """
        初始化
        数据成员：
            url1: 接口url
            headers: 主要是用于存放UA伪装
            encoding: 编码
            type_ls: 报表类型 包括：资产负债表、利润表、现金流量表、财务报表摘要、主要财务指标（又包括：偿债能力、营运能力、盈利能力）
            parts: 财务指标类型， 包括：偿债能力、盈利能力、营运能力
        """
        self.url1 = "http://quotes.money.163.com/service/"
        self.headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
        }
        self.encoding = "GBK"
        self.type_ls = {
            "资产负债表": 'zcfzb',
            "利润表": 'lrb',
            "现金流量表": 'xjllb',
            "财务报告摘要": 'cwbgzy',
            "主要财务指标": 'zycwzb'
        }

        self.parts = {
            "盈利能力": 'ylnl',
            "偿债能力": 'cznl',
            "营运能力": 'yynl'
        }

    def get(self, code,  sm_type, frequency="report", part=""):
        """
        获取财报信息
        :param code: 股票代码   数据类型：str
        :param sm_type: 报表类型
            可选参数: 资产负债表、利润表、资金流量表、财务报告摘要、主要财务指标
        :param frequency: 频率    数据类型
            可选参数: report、year
        :param part: 主要财务指标追加参数
            可选参数: 盈利能力、偿债能力、营运能力
        :return: DateFrame对象
        """
        url1 = self.url1 + self.type_ls[sm_type] + "_" + code + ".html"

        if sm_type == "主要财务指标" and part != "":
            part = self.parts[part]
        else:
            part = ""

        query = {
            "part": part,
            "type": frequency
        }
        response = requests.get(url1, params=query, headers=self.headers)
        response.encoding = self.encoding
        print(response.url)
        text = response.text
        lines = text.split("\n")
        columns = (lines[0].split(','))[1:-1]
        indexes = [line.split(',')[0] for line in lines[1:]]
        data = [line.split(',')[1:-1] for line in lines[1:]]
        indexes.pop(-1)
        data.pop(-1)
        res = pd.DataFrame(data=data, columns=columns, index=indexes)
        return res

class holderSpider:
    """
    爬取持股信息
    """
    def __init__(self):
        """
        初始函数
        数据成员：
            encoding: GBK编码
            url1: 股东分析接口
            url2: 基金持股接口
            period: 报告期
        """
        self.encoding = "GBK"
        self.url1 = 'http://quotes.money.163.com/service/gdfx.html'
        self.url2 = 'http://quotes.money.163.com/service/jjcg.html'
        self.url3 = 'http://quotes.money.163.com/f10/fhpg_'
        self.period = {
            1: "-03-31%2C,-12-31",
            2: "-06-30%2C,-03-31",
            3: "-09-30%2C,-06-30",
            4: "-12-31%2C,-09-30"
        }

    def getTop10(self, code, year, period=1, lt=False):
        """
        获取10大股东信息
        :param code: 股票编码   数据类型：str
        :param year: 年份 数据类型：int
        :param period: 报告期  数据类型：int    可选参数：1、2、3、4
        :param lt: 是否是流通股
        :return: DataFrame数据对象
        """
        if lt:
            lt = "lt"
        else:
            lt = ""

        query_date = lt + "date"

        date_ls = self.period[1].split(',')
        if period == 1:

            date = str(year)+date_ls[0]+str(year-1)+date_ls[1]
        else:
            date = str(year)+date_ls[0]+str(year)+date_ls[1]

        query = {
            query_date: date,
            "symbol": code
        }

        response = requests.get(self.url1, params=query)
        response.encoding = "UTF-8"
        text = response.text

        #使用lxml解析
        from lxml import etree
        tree = etree.HTML(text)
        columns = [i.text for i in tree.xpath("*//tr/th")]
        text_ls = [i.text for i in tree.xpath("*//tr/td")]
        data = [text_ls[4*i: 4*(i+1)] for i in range(10)]
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def getFundHolders(self, code, year, period=1):
        """
        获取基金持股信息（按报告期）
        :param code: 股票代码   数据类型：str
        :param year: 年份 数据类型：int
        :param period: 报告期 数据类型：int 可选参数：1、2、3、4
        :return: DataFrame对象
        """
        query_date = "date"

        date_ls = self.period[period].split(',')
        if period == 1:
            date = str(year)+date_ls[0]+str(year-1)+date_ls[1]
        else:
            date = str(year)+date_ls[0]+str(year)+date_ls[1]

        query = {
            query_date: date,
            "symbol": code
        }

        response = requests.get(self.url2, params=query)
        response.encoding = "UTF-8"
        print(response.url)
        text = response.text

        # 用lxml解析
        from lxml import etree
        etree = etree.HTML(text=text)

        # 定义函数，处理转义字符
        import json
        import re
        def transform(string):
            if not string:
                return ""
            elif len(string) < 5:
                return string
            string = string.replace(" ", "")
            string = string.replace("\\r", "")
            string = string.replace("\\n", "")
            string = string.replace("\\t", "")
            string = string.replace("\\", "")

            regex = re.compile("u[0-9a-f]{4}")
            body = "\\".join(regex.findall(string))
            try:
                name = json.loads('\"\\'+body+'\"')
            except:
                return string
            iter_ = list(regex.finditer(string))
            iter_name = iter(name)
            string_list = list(string)
            for i in range(len(iter_)):
                span = iter_[i].span()
                string_list[span[0]:span[1]] = list(next(iter_name) + " "*4)
            string = "".join(string_list).replace(" ", "")
            return string

        # 处理数据
        columns = ["基金名称"] + [transform(i.text) for i in etree.xpath("*//thead//*//th")][1:]
        fundNames = [transform(i.text) for i in etree.xpath("*//thead//*//td//*")[:-10]]
        sub_data = [transform(i.text) for i in etree.xpath("*//thead//*//td")[:]]
        info_index = sub_data[-1].find("info")
        sub_data[-1] = sub_data[-1][:info_index-3]

        data = []
        for i in range(len(fundNames)):
            curr = []
            curr.append(fundNames[i])
            for j in range(1,6):
                curr.append(sub_data[i*6+j])
            data.append(curr)

        df = pd.DataFrame(data, columns=columns)
        return df

    def getFundHolders2(self, code, start, end):
        """
        获取基金持股信息（不推荐，参数格式要求高）
        代码：复用getFundHolders，代码简化将在以后进行
        :param code: 股票代码   数据类型：int
        :param start: 开始日期  数据类型：str    必须符合报告期要求，包括：yyyy-03-31、yyyy-06-30、yyyy-09-30、yyyy-12-31
        :param end: 结束日期    数据类型：str    必须符合报告期要求，与start参数要求一直
        :return: DataFrame对象
        """
        query_date = "date"
        date = end + "%2C" + start

        query = {
            query_date: date,
            "symbol": code
        }

        response = requests.get(self.url2, params=query)
        response.encoding = "UTF-8"
        print(response.url)
        text = response.text

        # 用lxml解析
        from lxml import etree
        etree = etree.HTML(text=text)

        # 定义函数，处理转义字符
        import json
        import re
        def transform(string):
            if not string:
                return ""
            elif len(string) < 5:
                return string
            string = string.replace(" ", "")
            string = string.replace("\\r", "")
            string = string.replace("\\n", "")
            string = string.replace("\\t", "")
            string = string.replace("\\", "")

            regex = re.compile("u[0-9a-f]{4}")
            body = "\\".join(regex.findall(string))
            try:
                name = json.loads('\"\\' + body + '\"')
            except:
                return string
            iter_ = list(regex.finditer(string))
            iter_name = iter(name)
            string_list = list(string)
            for i in range(len(iter_)):
                span = iter_[i].span()
                string_list[span[0]:span[1]] = list(next(iter_name) + " " * 4)
            string = "".join(string_list).replace(" ", "")
            return string

        # 处理数据
        columns = ["基金名称"] + [transform(i.text) for i in etree.xpath("*//thead//*//th")][1:]
        fundNames = [transform(i.text) for i in etree.xpath("*//thead//*//td//*")[:-10]]
        sub_data = [transform(i.text) for i in etree.xpath("*//thead//*//td")[:]]
        info_index = sub_data[-1].find("info")
        sub_data[-1] = sub_data[-1][:info_index - 3]

        data = []
        for i in range(len(fundNames)):
            curr = []
            curr.append(fundNames[i])
            for j in range(1, 6):
                curr.append(sub_data[i * 6 + j])
            data.append(curr)

        df = pd.DataFrame(data, columns=columns)
        return df

    def getDividen(self, code):
        """
        分红信息查询
        :param code: 股票代码   数据类型：int
        :return: DataFrame数据结构
        """
        # 表头columns
        columns = ["公告日期", "分红年度", "送股", "转增", "派息", "股权登记日", "除权登记日", "红股上市日"]

        url = self.url3 + code + ".html"
        response = requests.get(url)
        text = response.text

        # 解析网页
        from lxml import etree
        tree = etree.HTML(text)
        text_ls = [i.text for i in tree.xpath("*//div[@class='inner_box']//tr//td")]
        print(text_ls)
        data = []
        for i in range(len(text_ls)//8):
            data.append(text_ls[i*8: (i+1)*8])
        print(data)
        df = pd.DataFrame(data, columns=columns)
        return df