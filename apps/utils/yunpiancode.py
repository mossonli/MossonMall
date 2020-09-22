import json
import requests


class Yunpian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_single_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": f"【李露】您的验证码是{code}"
        }
        response = requests.post(self.single_send_url, data=params)
        ret = json.loads(response.text)
        return ret

if __name__ == '__main__':
    yun_pian = Yunpian("33d6bd07ac642204e14b6eeef1409683")
    yun_pian.send_single_sms("2020", 18910523426)
