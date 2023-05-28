import requests
import re
from lxml import etree

from tookit.fofaUseragent import getFofaLoginHeaders


class FofaLogin:
    def __init__(self):
        self.session = requests.session()

    def fofaCaptcha(self, src):
        import ddddocr
        ocr = ddddocr.DdddOcr(show_ad=False)
        fofa_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
            'Host': 'i.nosec.org',
            'Referer': 'https://i.nosec.org/login',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
        }
        captcha_api = f'https://i.nosec.org{src}'
        print(captcha_api)
        resp = self.session.get(url=captcha_api, headers=fofa_headers)
        print(resp.text)
        return ocr.classification(resp.content)

    def fofaLogin(self,fofa_username, fofa_password):
        print('尝试登录')

        authen = self.session.get(url='https://i.nosec.org/login?service=https://octra.fofa.vip/fofaLogin', headers=getFofaLoginHeaders())
        src = re.findall('class="rucaptcha-image" src="(.*?)"', authen.text)[0]

        captcha = self.fofaCaptcha(src)
        authenticity_token = re.findall('"csrf-token" content="(.*?)" /', authen.text)[0]
        lt = re.findall('id="lt" value="(.*?)" /', authen.text)[0]
        data = {
            'utf8': '%E2%9C%93',
            'authenticity_token': authenticity_token,
            'lt': lt,
            'service': 'https://octra.fofa.vip/fofaLogin',
            'username': fofa_username,
            'password': fofa_password,
            '_rucaptcha': captcha,
            'rememberMe': '1',
            'button': '',
            'fofa_service': '1',
        }
        user_login_api = 'https://i.nosec.org/login'
        res_login = self.session.post(url=user_login_api, data=data)
        if '登录验证码错误' in res_login.text:
            print("验证码错误，重新运行脚本")
            return 0
        elif '用户名或密码错误' in res_login.text:
            print('用户名或密码错误,请检查账户名和密码后重试')
            return 0
        else:
            print("登录成功")
            tempstr = ''
            for key, value in self.session.cookies.get_dict().items():
                tempstr += key + "=" + value + "; "
            with open('fofa_cookie.txt', 'w') as f:
                f.write(tempstr)
            return self.session.cookies, 1

    def check_login(self, cookies):
        self.check_headers = {
            'Host': 'fofa.info',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'DNT': '1',
            'Referer': 'https://fofa.info/',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': cookies,
        }
        resp = requests.get(url='https://fofa.info/result?qbase64=MQ==&page=2&page_size=10', headers=self.check_headers)
        tree = etree.HTML(resp.text)
        urllist = tree.xpath('//span[@class="hsxa-host"]/a/@href')
        return len(urllist), cookies


def main():
    fofaLogin=FofaLogin()
    print(fofaLogin.fofaLogin("Dragonglifes","Lxygwqf@2020**"))

if __name__ == '__main__':
    main()