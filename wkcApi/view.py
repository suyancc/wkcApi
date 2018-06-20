from django.http import HttpResponse
from django.shortcuts import render, redirect
import wkcApi.model.wkcApi as wkc
import json

ERROR_MSG = 1
SUCCESS_MSG = 0


def index(param):
    return render(param, 'index/index.html')


def upload(param):
    f = param.FILES.get('file')
    file_value = []

    try:
        for chrunk in f.chunks():
            file_value = json.loads(chrunk.decode('ascii'))
    except:
        return HttpResponse(resJson('文件格式不正确', ERROR_MSG))

    if 'address' not in file_value:
        return HttpResponse(resJson('文件格式不正确', ERROR_MSG))

    address = '0x' + str(file_value['address'])
    balance = wkc.getBalance(address)

    print('文件内容:', file_value)
    print('余额：', balance)
    return HttpResponse(
        resJson('操作成功', SUCCESS_MSG, {'address': address, 'balance': json.loads(balance)['data']['result']})
    )


def sendPay(param):
    print(param.POST)
    my = '0x10536f4c0093b61e739210d7a7a2ad81dd7ff1fe'
    to = '0x883d1368b8eb625ef393b7a573a9f7a9c51a29ab'
    nonce = wkc.getTransactionCount(my)
    wkc.SignTransaction(my,to,1,nonce['result'])




    return HttpResponse('')


def resJson(msg='', code=0, data=[]):
    return json.dumps({'code': code, 'msg': msg, 'data': data})
