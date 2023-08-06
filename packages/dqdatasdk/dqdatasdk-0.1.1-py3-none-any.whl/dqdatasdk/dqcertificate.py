# -*- coding: utf-8 -*-
"""
点宽鉴权系统
"""
import requests

url = "https://online2.digquant.com"  # 生产环境


# url = "http://alpha.digquant.com:18889" # alpha环境

def dqlogin(username, password):
    # get data
    url_p = url + '/user-server/user/login'
    data = {
        'sessionId': '',
        'loginName': username,
        'productName': 'dqdatasdk',
        'loginType': 'password',
        'password': password,
        'verifyCode': ''
    }
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.post(url_p, json=data, headers=headers)
    # print(response.text)
    data = response.json()

    if data['errCode'] != 0:
        raise Exception(data['errMsg'])

    return data['data']


def get_dqdata_license(username, password):
    logininfo = dqlogin(username, password)
    token = logininfo['token']

    url_p = url + '/support-server/dqDataLicense/getDqDataLicense'
    headers = {
        'Content-Type': "application/json",
        'Product': 'dqdatasdk',
        'token': token
    }
    response = requests.post(url_p, headers=headers)
    '''
    {
  "data": {
    "applyId": 0,
    "auditComment": "string",
    "endDate": 0,
    "id": 0,
    "license": "string",
    "startDate": 0,
    "status": 0,
    "updateDate": 0,
    "updateId": 0,
    "userId": 0
  },
  "errCode": 0,
  "errMsg": "string"
}
    '''
    data = response.json()
    if data['errCode'] != 0:
        raise Exception(data['errMsg'])

    if data['data'] == None:
        raise Exception('data字段为None,可能没有开通dqdata权限或用户信息错误')

    licenseinfo = data['data']
    if 'license' not in licenseinfo:
        raise Exception('没有请求到lincense字段,可能没有开通dqdata权限或用户信息错误')

    return licenseinfo['license']


if __name__ == "__main__":
    license = get_dqdata_license('jin', '123456')
    print(license)
