# kkbtools
![](https://img.shields.io/badge/python-3.6-brightgreen)

## Introduction
公司爬虫业务中，常用的工具集
## Requirement
```shell
Python >= 3.6
```

## Install
```shell
pip install kkbtools
```
## Usage
安装后将需要用到的类导入即可，更多方法，请查看源码
```python
from kkbtools import PandasPro, Tools, OssUpload

```

## Example
```python
from kkbtools import PandasPro, Tools, OssUpload

# 将 list[dict] 数据插入excel
PandasPro.insert_lists_dict_to_excel(lists=[{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], table_name='test')

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
```

## Help Document
```Shell
kkbtools [-h] [--help]
# 待完善。。。
```

## Thanks
wshuo
