from web3 import Web3
import requests
import json
import web3.eth

URL = 'https://walletapi.onethingpcs.com'


def getBalance(address):
    '''
    查询账户余额
    :param address:  账号
    :return:
    {'error': {'message': 'Order is abnormal, please check', 'code': -3034}, 'jsonrpc': '2.0', 'id': 1}
    {"id":1,"jsonrpc":"2.0","result":"0x89aaeb710be00000"}
    '''
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    data = json.dumps(data)
    res = requests.post(URL + '/getBalance', data=data)
    res = json.loads(res.text)
    print(res)
    if 'err' in res:
        return resJson(res['err'])
    else:
        res['result'] = str(Web3.fromWei(eval(res['result']), 'ether'))

    return resJson('查询成功', 1, res)


def getTransactionCount(address):
    '''
    获取账户交易次数
    :param address:账户地址
    :return: {'jsonrpc': '2.0', 'id': 1, 'result': '0x8'}
    '''
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [address, "pending"],
        "id": 1
    }
    data = json.dumps(data)
    res = requests.post(URL + '/getTransactionCount', data=data)
    res = json.loads(res.text)
    print(res)


    print(res)
    return res





def SignTransaction(address, to_address,money, nonce):
    # web3.utils.toHex(web3.utils.toWei(params.value)),
    txParams = {
        "from": address,
        "to": to_address,
        "value": Web3.toHex(Web3.toWei(money)) ,
        "gasLimit": '0x186a0',
        "gasPrice": '0x174876e800',
        "nonce": nonce,
    }






def resJson(msg='', code=0, data=[]):
    return json.dumps({'code': code, 'msg': msg, 'data': data})
