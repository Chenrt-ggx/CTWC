import os
import re
import xlrd
import json
import base64
import requests
from bs4 import BeautifulSoup


def get_user_info():
    def __decode(text):
        return base64.b64decode(text.encode()).decode()

    try:
        """
        authorization.json：
            username: 用户名的 base64 加密结果
            password: 用户密码的 base64 加密结果
        """
        with open('../authorization.json', 'r') as file:
            authorization = json.load(file)
        return __decode(authorization['username']), __decode(authorization['password'])
    except IOError:
        print('error: authorization file failed to load')
        exit(0)


def sso_login():
    session = requests.session()
    request = session.get('https://sso.buaa.edu.cn/login')
    soup = BeautifulSoup(request.text, 'html.parser')
    execution = soup.find(name='input', attrs={'name': 'execution'}, recursive=True)['value']
    username, password = get_user_info()
    session.post(url='https://sso.buaa.edu.cn/login', data={
        'username': username,
        'password': password,
        'execution': execution,
        '_eventId': 'submit',
    }, allow_redirects=False)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    if len(cookies) == 0:
        print('^^^ sso login failed ^^^')
        exit(0)
    return cookies


def jw_login(sso_cookies):
    session = requests.session()
    session.get(url='http://jwxt.buaa.edu.cn:8080/ieas2.1/welcome', cookies=sso_cookies)
    sso_cookies = requests.utils.dict_from_cookiejar(session.cookies)
    sso_cookies = {'JSESSIONID': sso_cookies['JSESSIONID']}
    return sso_cookies


def get_xls():
    cookies = jw_login(sso_login())
    request = requests.get('http://jwxt.buaa.edu.cn:8080/ieas2.1/kbcx/queryGrkb', cookies=cookies)
    match = re.search('<option value="(\d+-\d+)" selected>', request.text)
    request = requests.post('http://jwxt.buaa.edu.cn:8080/ieas2.1/kbcx/ExportGrKbxx', data={
        'fhlj': 'kbcx/queryGrkb',
        'xnxq': match.group(1)
    }, cookies=cookies)
    with open('./temp.xls', 'wb') as file:
        file.write(request.content)
    return xlrd.open_workbook('./temp.xls').sheets()[0]


def clear_xls():
    os.remove('./temp.xls')
