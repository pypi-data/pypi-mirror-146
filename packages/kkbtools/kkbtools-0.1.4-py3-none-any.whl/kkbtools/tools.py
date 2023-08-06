import calendar
import datetime
import json
import os
import re
import time

import oss2
import pandas as pd
import pymongo
import pymysql
import requests
from feapder.utils.tools import get_current_date
from tqdm import tqdm
from urllib3 import encode_multipart_formdata


class OssUpload:
    access_key_id = os.getenv('ACCESS_KEY_ID')
    access_key_secret = os.getenv('ACCESS_KEY_SECRET')
    endpoint = 'oss-cn-beijing.aliyuncs.com'
    bucket_name = 'kkb-storage'
    key = 'excel'
    download_link_pre = 'https://kkb-storage.oss-cn-beijing.aliyuncs.com/etg/'
    corpid = os.getenv('CORPID')
    secrect = os.getenv('SECRECT')

    def __init__(self, access_key_id=None, access_key_secret=None, endpoint=None, bucket_name=None,
                 key=None, download_link_pre=None, corpid=None, secrect=None):
        OssUpload.access_key_id = access_key_id or OssUpload.access_key_id
        OssUpload.access_key_secret = access_key_secret or OssUpload.access_key_secret
        OssUpload.endpoint = endpoint or OssUpload.endpoint
        OssUpload.bucket_name = bucket_name or OssUpload.bucket_name
        OssUpload.key = key or OssUpload.key
        OssUpload.download_link_pre = download_link_pre or OssUpload.download_link_pre
        OssUpload.corpid = corpid or OssUpload.corpid
        OssUpload.secrect = secrect or OssUpload.secrect

    def __upload_file(self, file_path: str) -> str:
        """
        上传文件到OSS
        """
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        # 填写Object完整路径和本地文件的完整路径。Object完整路径中不能包含Bucket名称。
        # 如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
        # file_abspath = os.path.abspath(filename)
        object_name = 'etg/' + file_path
        with open(file_path, 'rb') as fileobj:
            # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
            # fileobj.seek(1000, os.SEEK_SET)
            # Tell方法用于返回当前位置。
            # current = fileobj.tell()
            # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
            bucket.put_object(object_name, fileobj)

        download_link = self.download_link_pre + file_path
        print('upload success!', file_path, download_link)

        return download_link

    @staticmethod
    def __send_oss_file_to_dingding(download_url: str, url_robot: str, msg: str, key: str) -> str:
        """通过群机器人发送链接，达到点击链接下载文件的目的"""
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data = {
            "actionCard": {
                "title": "%s" % key,
                "text": " %s \n\n更新时间：%s " % (msg, send_time),
                "hideAvatar": "0",
                "btnOrientation": "0",
                "btns": [
                    {
                        "title": "点击下载数据",
                        "actionURL": download_url
                    },

                ]
            },
            "msgtype": "actionCard"
        }
        r = requests.post(url_robot, data=json.dumps(data), headers=header)
        print(r.text)
        return r.json()

    @classmethod
    def send_file_and_remove_oss(cls, file_path: str, url_robot: str):
        """
        把文件上传到oss中，生成直链后，发送到钉钉群,并删除本地文件
        """
        download_url = cls.__upload_file(cls, file_path)
        url_robot = url_robot
        msg = '文件名：' + file_path
        key = cls.key  # 钉钉安全设置的自定义关键字
        cls.__send_oss_file_to_dingding(download_url, url_robot, msg, key)
        time.sleep(1)
        if os.path.exists(file_path):
            os.remove(file_path)

    # 下面的是不通过oss转存，用盯盘转存发送到钉钉群的相关的程序
    def __get_token(self):
        """
        获取最新的access_toke
        """
        corpid = self.corpid
        secrect = self.secrect
        url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (
            corpid, secrect)
        req = requests.get(url)
        access_token = json.loads(req.text)
        return access_token['access_token']

    @staticmethod
    def __get_media_id(file_path, file_name, access_token):
        """上传文件并且返回对应的media_id"""
        url_post = r"https://oapi.dingtalk.com/media/upload?access_token=%s&type=file" % access_token
        headers = {}
        # file_name,不支持中文，必须为应为字符
        data = {'media': (file_name, open(file_path, 'rb').read())}
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]
        r = requests.post(url_post, headers=headers, data=data)
        media_id = json.loads(r.text)["media_id"]
        return media_id

    # 临时链接方法，上传到盯盘，在传到钉钉群，链接有效期为2小时
    @classmethod
    def send_file_and_remove_ding(cls, file_path, url_robot):
        """
        依次为文件路径，Webhook地址,需要发送的消息,钉钉安全设置的自定义关键字
        这种方式直接发送文件到群里，文件有效期2小时，不经过oss存储，发送完毕后，删除本地文件
        """
        msg = '文件名：' + file_path
        key = cls.key
        access_token = cls.__get_token()
        file_name = file_path.split('\\')[-1]
        media_id = cls.__get_media_id(file_path, file_name, access_token)
        download_url = "https://oapi.dingtalk.com/media/downloadFile?access_token=%s&media_id=%s" % (
            access_token, media_id)
        result = cls.__send_oss_file_to_dingding(download_url, url_robot, msg, key)
        print(result)


class PandasPro:
    MYSQL_IP = os.getenv("MYSQL_IP")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_USER_NAME = os.getenv("MYSQL_USER_NAME")
    MYSQL_USER_PASS = os.getenv("MYSQL_USER_PASS")

    MONGO_IP = os.getenv("MONGO_IP")
    MONGO_PORT = os.getenv("MONGO_PORT")
    MONGO_DB = os.getenv("MONGO_DB")

    @classmethod
    def insert_lists_dict_to_excel(cls, lists, columns=None, table_name='test'):
        """
        将形如[{},{}]这样的列表插入存入excel中，并可指定{}中的列名
        """
        df = pd.DataFrame(lists, columns=columns)
        current_time = get_current_date(date_format="%Y-%m-%d-%H:%M:%S")
        file_name = f'{table_name}_{current_time}_.xlsx'
        df.to_excel(file_name, columns=columns, index=False)
        if os.path.exists(file_name):
            cls.__set_format(file_name)
        print('finshed:', f'{table_name}_{current_time}.xlsx')
        return f'{table_name}_{current_time}.xlsx'

    @staticmethod
    def __set_format(filename):
        writer = pd.ExcelWriter(filename.replace('_.', '.'))
        workbook = writer.book
        sheet = 'Sheet1'
        # # 3.循环遍历sheet取数据
        df1 = pd.read_excel(filename, sheet_name=sheet)

        # 4.设置格式
        fmt = workbook.add_format(
            {"font_name": u"微软雅黑", 'align': 'left', 'valign': 'vcenter', 'font_size': 11})
        border_format = workbook.add_format({'border': 1})
        bg_format = workbook.add_format({'bold': True,
                                         'font_name': u'微软雅黑',
                                         'bg_color': '#4570FF',
                                         'align': 'center',
                                         'valign': 'vcenter',
                                         'font_color': 'black',
                                         'font_size': 13})
        # 5.写入excel
        l_end = len(df1.index) + 1  # 行数
        colums = df1.shape[1]  # 列数
        df1.to_excel(
            writer,
            sheet_name=sheet,
            encoding='utf8',
            header=df1.columns.values.tolist(),
            index=False,
            startcol=0,
            startrow=0)
        worksheet1 = writer.sheets[sheet]

        # 6.生效单元格格式
        # 设置行高a
        worksheet1.set_row(0, 20, fmt)  # 从第0行开始，行高为20，格式为fmt

        # 设置列宽， 设置为每列中最长的字符数+1
        df1_list = df1.values.tolist()
        df2 = list(map(list, zip(*df1_list)))

        for index, i in enumerate(df2):
            # 注意:  1. execl读取会将类似'3.22'这种格式转成float,用str() 2. 有些特殊符号，没有gbk, 用ignore
            max_len = len(str(max(i, key=lambda x: len(str(x).encode(
                'gbk', errors='ignore')), default='')).encode('gbk', errors='ignore')) + 5
            # max_len = len(max(i, key=len, default='').encode('gbk')) + 5
            if max_len > 80:
                max_len = 80
            if max_len < 10:
                max_len = 10
            worksheet1.set_column(index, index, max_len, fmt)

        # 设置列宽
        # worksheet1.set_column('A:A', 20, fmt)  # 从A列到F列，行高为10，格式为fmt
        # 加边框
        worksheet1.conditional_format(
            f'A1:{chr(65 + colums)}{l_end}', {'type': 'no_blanks', 'format': border_format})
        # worksheet1.conditional_format(0, l_end, {'type': 'no_blanks', 'format': border_format})
        # A1单元格到F(索引值）, 'type': 'no_blanks'指非空的单元格加格式
        # 设置背景色
        worksheet1.conditional_format(
            f'A1:{chr(65 + colums)}1', {'type': 'no_blanks', 'format': bg_format})

        writer.save()
        if os.path.exists(filename):
            os.remove(filename)

    @classmethod
    def mongo_to_execl(cls, db_name: str, table_name: str, sql: dict = {}) -> pd.DataFrame:
        """mongo中查询到的数据直接存到excel文件名前缀曲子表名"""
        file_name_pre = table_name
        client = pymongo.MongoClient(cls.MONGO_IP, cls.MONGO_PORT)
        db = client[db_name]
        table = db[table_name]
        # 从excel中读数据到Pandas
        # excel名称
        # excelFile = r''
        # df = pd.DataFrame(pd.read_excel(excelFile))
        # 加载数据到Pandas中
        data = pd.DataFrame(list(table.find(sql)))
        # 删除mongdb中_id字段
        del data['_id']
        # 选择需要显示的字段
        # data = data[['date', 'num1', 'num10']]
        # 写入excel
        current_time = get_current_date(date_format="%Y-%m-%d-%H:%M:%S")
        file_name = f'{file_name_pre}_{current_time}_.xlsx'
        data.to_excel(file_name, index=False, encoding='utf-8')
        if os.path.exists(file_name):
            cls.__set_format(file_name)
        output_file_name = file_name.replace('_.', '.')
        print('finshed:', output_file_name)
        return output_file_name

    @classmethod
    def mysql_to_execl(cls, table_name: str = None, days: str = None, remove_field: list = None):
        """
        使用days这个参数，mysql数据库汇总必须有publish_time这个参数
        """
        file_name_pre = table_name
        if not days:
            query = "select * from {}".format(table_name)
        else:
            query = f"""
                SELECT * 
                FROM `{table_name}`
                WHERE `publish_time` >= '{days}';
            """
        db = pymysql.connect(
            host=cls.MYSQL_IP,
            port=cls.MYSQL_PORT,
            user=cls.MYSQL_USER_NAME,
            password=cls.MYSQL_USER_PASS,
            charset='utf8',
            database=cls.MYSQL_DB)
        df = pd.read_sql_query(query, db)
        # df = ' / '.join(df['E'].groupby('colleges', 'title'))
        del df['id']
        if remove_field:
            for j in remove_field:
                del df[j]

        current_time = get_current_date(date_format="%Y-%m-%d-%H:%M:%S")
        file_name = f'{file_name_pre}_{current_time}_.xlsx'
        df.to_excel(file_name, index=False, encoding='utf-8')
        if os.path.exists(file_name):
            cls.__set_format(file_name)
        output_file_name = file_name.replace('_.', '.')
        print('finshed:', output_file_name)
        return output_file_name

    @staticmethod
    def dict_to_csv(item: dict, pre: str = 'test') -> str:
        """
        dict转存到csv
        """
        df = pd.DataFrame(item, index=[0])
        df.to_csv(f'{pre}.csv', mode='a', index=False, encoding='utf-8',
                  header=False)
        return pre

    @staticmethod
    def excel_to_list(filename: str, sheet_name: int = 0) -> list:
        """
        csv或者excel文件读取到list
        """
        list_from_csv = pd.read_excel(filename, sheet_name=sheet_name).values.tolist()
        return list_from_csv

    @staticmethod
    def excel_to_dict_list(path):
        """
        将excel表格转为字典，形如：
        {'data': [{'列1':  '值1', '列2': '值2', '列3': '值3', '列4': '值4'}, {'列1':  '值5', '列2': '值6', '列3': '值7', '列4': '值8'}]}
        """
        # 创建最终返回的空字典
        df_dict = {}
        # 读取Excel文件
        df = pd.read_excel(path)

        # 替换Excel表格内的空单元格，否则在下一步处理中将会报错
        df.fillna("", inplace=True)
        df_list = []
        for i in df.index.values:
            # loc为按列名索引 iloc 为按位置索引，使用的是 [[行号], [列名]]
            df_line = df.loc[i, [column for column in df]].to_dict()
            # 将每一行转换成字典后添加到列表
            df_list.append(df_line)
        df_dict['data'] = df_list

        return df_dict


class Tools:
    """
    工具类
    """

    @staticmethod
    def nth_replace(string, sub, wanted, n):
        """
        替换第n个字符串
        """
        pattern = re.compile(sub)
        where = [m for m in pattern.finditer(string)][n - 1]
        before = string[:where.start()]
        after = string[where.end():]
        new_string = before + wanted + after
        return new_string

    @staticmethod
    def dedup_dict(li: list, li_field: list = None) -> list:
        """
        基于内存的去重，对列表中的字典做去重处理，返回一个去重后的list
        """
        buff_data = []
        dedup_list = []
        for i in li:
            if li_field:
                dedup_str = ''.join([str(i[k]) for k in li_field])
            else:
                dedup_str = i
            if dedup_str not in dedup_list:
                dedup_list.append(dedup_str)
                buff_data.append(i)

        return buff_data

    @staticmethod
    def check_reg(reg, string: str) -> bool:
        """
        检测字符串中是否包含正则表达式能匹配的字符串
        """
        ss = re.search(reg, string)
        if ss:
            return True
        else:
            return False

    @staticmethod
    def get_off_days_timestamp(days: int = None) -> int:
        """
        获取偏移时间的时间戳
        """
        if not days:
            timestamp = int(time.time())
        else:
            off_days_timetuple = datetime.datetime.now() - datetime.timedelta(days=days)
            timestamp = int(time.mktime(off_days_timetuple.timetuple()))
        return timestamp

    @staticmethod
    def sort_list_dict_costomize(d: dict, li_field: list) -> dict:
        """
        将dict，按照自定义字段li_field排序,返回排序后的dict
        eg:
        li_field = ['unit_name', 'job_name', 'province_name', 'create_time']
        """

        item = {}
        for i in li_field:
            if i in d:
                item[i] = d[i]
        return item

    @staticmethod
    def cut(obj: iter, sec: int) -> list:
        """
        将一个可迭代对象拆分
        """
        return [list(obj[i:i + sec]) for i in range(0, len(obj), sec)]

    @staticmethod
    def my_cut(obj: iter, sec: int) -> list:
        """
        将一个可迭代对象拆分,分割处，重复出现，1,31分割形如
        [[1, 2, 3, 4, 5, 6, 7, 8], [8, 9, 10, 11, 12, 13, 14, 15],
        [15, 16, 17, 18, 19, 20, 21, 22], [22, 23, 24, 25, 26, 27, 28, 29], [29, 30, 31]]
        """
        cut_list = [list(obj[i:i + sec]) for i in range(0, len(obj), sec)]
        for index, j in enumerate(cut_list[:-1]):
            cut_list[index].append(cut_list[index + 1][0])

        return [[i[0], i[-1]] for i in cut_list]

    @staticmethod
    def get_month_first_last_day(year: int = None, month: int = None) -> tuple:
        """
        获取指定年月的第一天和最后一天
        """
        if year:
            year = int(year)
        else:
            year = datetime.date.today().year

        if month:
            month = int(month)
        else:
            month = datetime.date.today().month

        # x：表示当月第一天所属的星期
        # y：表示当月的总天数
        x, y = calendar.monthrange(year, month)

        def get_timestamp(time_day):
            return int(time.mktime(time_day.timetuple()))

        first_day = datetime.date(year=year, month=month, day=1)
        # 下个月的第一天
        # next_first_day = first_day + relativedelta(months=1)
        last_day = datetime.date(year=year, month=month, day=y)

        # return first_day, next_first_day
        return get_timestamp(first_day), get_timestamp(last_day)
        # 返回时间戳


def call_time(func):
    """
    打印时间的装饰器
    """

    def wrapper(*args, **kwargs):
        t1 = time.time()
        func1 = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__} running time: {t2 - t1} secs.')
        return func1

    return wrapper


def bar(func):
    """
    给可迭代对象添加进度条的装饰器
    """

    def wrapper(iter_, *args, **kwargs):
        a = tqdm(iter_, bar_format="{l_bar}{bar}", colour='green', ncols=80)
        for i in a:
            # time.sleep(.01)
            a.set_description("Processing %s" % (i + 1))
            func1 = func(iter_, *args, **kwargs)
        return func1

    return wrapper


if __name__ == '__main__':
    # 将 list[dict] 数据插入excel
    PandasPro.insert_lists_dict_to_excel([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], 'test')

    # 将mysql数据插入excel中，数据库连接信息，默认读取环境变量 ~/.bash_profile
    PandasPro.mysql_to_execl('test')

    # 获取一天前时间戳，默认00：0:0：00时刻
    # 1649734882
    print(Tools.get_off_days_timestamp(-1))

    # 拆分可迭代对象
    # [[1, 2], [3, 4], [5]]
    print(Tools.cut([1, 2, 3, 4, 5], 2))

    # 把文件上传到oss中，生成直链后，发送到钉钉群,并删除本地文件
    OssUpload.send_file_and_remove_oss('test.xlsx', 'https://此处写钉钉群连接')

    # 依次为文件路径，Webhook地址,需要发送的消息,钉钉安全设置自定义关键字
    # 这种方式直接发送文件到群里，文件有效期2小时，不经过oss存储，发送完毕后，删除本地文件
    OssUpload.send_file_and_remove_ding('test.xlsx', 'https://此处写钉钉群连接')

