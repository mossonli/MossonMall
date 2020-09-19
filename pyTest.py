from lxml import etree
import requests
from lxml.html import fromstring, tostring
url = "https://libweb.zju.edu.cn/39511/list.htm"
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/72.0.3626.121 Safari/537.36'

}
ret = requests.get(url, headers=headers)
code = ret.apparent_encoding  # 获取url对应的编码格式
ret.encoding = code
html = ret.text               # html文件内容即示例中的标签

tree = etree.HTML(html)
result = tree.xpath('//*[@id="wp_content_w14_0"]')[0]
div = etree.tostring(result).decode()
print(div)