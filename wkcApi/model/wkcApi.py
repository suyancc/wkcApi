from web3 import Web3
import requests
import json

URL = 'https://walletapi.onethingpcs.com'

def getBalance(address):
    '''
    查询账户余额
    :param address:  账号
    :return:
    {'error': {'message': 'Order is abnormal, please check', 'code': -3034}, 'jsonrpc': '2.0', 'id': 1}
    {"id":1,"jsonrpc":"2.0","result":"0x89aaeb710be00000"}
    '''
    body = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    body = json.dumps(body)
    res = requests.post(URL + '/getBalance', data=body)
    res = json.loads(res.text)
    print(res)
    if 'err' in res:
        return resJson(res['err'])
    else:
        res['result'] = str(Web3.fromWei(eval(res['result']), 'ether'))

    return resJson('查询成功', 1, res)






def resJson(msg='', code=0, data=[]):
    return json.dumps({'code': code, 'msg': msg, 'data': data})
