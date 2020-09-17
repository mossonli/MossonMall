# import jieba
# import xlrd
# data = xlrd.open_workbook("/Users/mosson/desktop/py学员.xls")
# print(data)
# table = data.sheets()[0]
# col1 = table.col_values(1)
# for i in col1:
#     seg_generator = jieba.cut(i, cut_all=True)
#     print(list(seg_generator))
import json

import requests

# 翻译函数，word 需要翻译的内容
def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        print('111')
        return response.text
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None

def get_reuslt(repsonse):
    # 通过 json.loads 把返回的结果加载成 json 格式
    result = json.loads(repsonse)

    return result['translateResult'][0][0]['tgt']

def main(err):
    word = "中国"
    list_trans = translate(word)
    return get_reuslt(list_trans)

print(main('SyntaxError: bad input on line 1'))