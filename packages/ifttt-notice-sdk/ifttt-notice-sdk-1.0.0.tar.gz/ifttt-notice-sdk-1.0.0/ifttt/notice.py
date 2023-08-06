# -*- coding: UTF-8 -*-

import requests
import json


def send_notice(event_name, key, text):
    '''
    通过IFTTT发送手机通知
    Args:
        event_name (str):事件名称
        key (str):IFTTT上的Key
        text (str):通知文本信息
    '''
    url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(event_name, key)
    payload = json.dumps({'value1': text})
    headers = {'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    text = '服务器:1号发生故障11111111$%^*a1'
    print(send_notice('test1', 'dXGc1k52h7GflYU4Lcjt7G', text))