import requests
import re
import http.cookiejar as cookielib
import time
from bs4 import BeautifulSoup as bs

class Signin(object):
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    headers = {
        'User-Agent': agent
    }
    # 使用登录cookie信息
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cookies')
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")

    def get_xsrf(self):
        soup = bs(self.session.get('http://www.zhihu.com/#signin', headers=self.headers).text, 'html.parser')
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
        return xsrf

    # 获取验证码
    def get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
        r = self.session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        captcha = input("请输入验证码：\n")
        return captcha

    def isSignin(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = "https://www.zhihu.com/settings/profile"
        signin_code = self.session.get(url, allow_redirects=False).status_code
        if int(x=signin_code) == 200:
            return True
        else:
            return False

    def signin(self, account, password):
        # 通过输入的用户名判断是否是手机号
        if re.match(r"^1\d{10}$", account):
            print("手机号登录 \n")
            post_url = 'https://www.zhihu.com/login/phone_num'
            postdata = {
                '_xsrf': self.get_xsrf(),
                'password': password,
                'remember_me': 'true',
                'phone_num': account,
            }
        # 可加上邮箱的判断，这里不加了
        else:
            print("邮箱登录 \n")
            post_url = 'https://www.zhihu.com/login/email'
            postdata = {
                '_xsrf': self.get_xsrf(),
                'password': password,
                'remember_me': 'true',
                'email': account,
            }
        conf_url = 'https://www.zhihu.com/settings/profile'
        try:
            # 不需要验证码直接登录成功
            signin_page = self.session.post(post_url, data=postdata, headers=self.headers)
            signin_code = signin_page.text
            print(signin_code['msg'])
        except:
            # 需要输入验证码后才能登录成功
            postdata["captcha"] = self.get_captcha()
            signin_page = self.session.post(post_url, data=postdata, headers=self.headers)
            signin_code = eval(signin_page.text)
            print(signin_code['msg'])
        self.session.cookies.save()
        return self.session