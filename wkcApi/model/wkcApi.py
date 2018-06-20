from web3 import Web3
from web3.auto import w3
import requests
import json
import socks
import socket
from eth_account.messages import defunct_hash_message

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
    return res


def SignTransaction(address, to_address, money, nonce):
    with open('/Users/suyan/Downloads/KeyStore.') as keyfile:
        encrypted_key = keyfile.read()
        print('encrypted_key ===>', encrypted_key)
        private_key = w3.eth.account.decrypt(encrypted_key, '940154552')
        # tip: do not save the key or password anywhere, especially into a shared source file

    # b'\xc0\xdf\xb6\t\xdap7k\xe2\n\x85U\\x+i$\x8e\xb7\xf8\xc5\xca\x17\xeb\x95\xd6*\xc3\xb0\x10\xb4\x01'
    # print('private_key ===>', private_key)
    # msg = "I♥SF"
    # message_hash = defunct_hash_message(text=msg)
    # signed_message = w3.eth.account.signHash(message_hash, private_key=private_key)
    # signHash ===> AttrDict({'messageHash': HexBytes('0x1476abb745d423bf09273f1afd887d951181d25adc66c4834a70491911b7f750'), 'r': 75806573456849353714659217037622424417782668665953706446578304768433740446091, 's': 24438865798509095106875808125928253790419909228510974576102628882808767699863, 'v': 28, 'signature': HexBytes('0xa7990005496dfb0da6dd90490800dd013f622e1e288c1c39b59b48aa4c61f98b3607e8695b4676edc55b96085076a2729492be971058b4466a02f1227dcadb971c')})

    # print('signHash ===>',signed_message)
    # print(signed_message.signature)
    # key = w3.toHex(signed_message.signature)
    # print('key ===>',key)

    private_key = w3.toHex(private_key)
    print('private_key', private_key)

    transaction = {
        #"from": address,
        "to": to_address,
        "value": Web3.toHex(Web3.toWei(money, 'ether')),
        "gasLimit": '0x186a0',
        "gasPrice": '0x174876e800',
        # 'gas': 2000000,
        # 'chainId': 1,
        "nonce": nonce,
    }
    transaction = {
        # Note that the address must be in checksum format:
        #0x883d1368b8eb625ef393b7a573a9f7a9c51a29ab
        'to': "0xF0109fC8DF283027b6285cc889F5aA624EaC1F55",
        'value': Web3.toHex(Web3.toWei(money, 'ether')),
        'gas': 2000000,
        'gasPrice': '0x174876e800',
        'nonce': nonce,
        'chainId': 1
    }
    print('transaction ===>', transaction)
    signed = w3.eth.account.signTransaction(transaction, private_key)
    # AttrDict({'rawTransaction': HexBytes(
    #     '0xf8592285174876e800831e848080880de0b6b3a7640000801ca0f9095c218d3f3d2a57d69998d6dab67e859559d510c68a8d8ae6d66fdf0c4c6fa066160c684e4c215a6cccc69cc87d9f6de0656543a38a2052d44e74399e3a3069'),
    #           'hash': HexBytes('0x34270a925fe8b3d593348788b8ec46a307aa28a6641c48941548736e1b0e6d20'),
    #           'r': 112642436786033529022820656178847274196669484088910403382831892221998404488303,
    #           's': 46174866823954587873060830878070405188919827019627630425541614381787799761001, 'v': 28})
    print(signed)

    # res = w3.eth.sendRawTransaction(signed.rawTransaction)
    # print('sendRawTransaction ===>',res)

    transaction = {
        "jsonrpc": "2.0",
        "method": "eth_sendRawTransaction",
        "params": [w3.toHex(signed.rawTransaction)],
        "id": 1
    }
    print('transaction == >', transaction)
    headers = {'content-type': 'application/json', "Nc": "IN"}

    socks.set_default_proxy(socks.SOCKS5,"45.63.18.118",1080,username='suyan',password='940154552')
    socket.socket = socks.socksocket
    res = requests.get('http://www.telize.com/geoip').text
    print(res)
    signed = requests.post(URL + '/sendRawTransaction', data=json.dumps(transaction), headers=headers)

    print(signed.text)


def resJson(msg='', code=0, data=[]):
    '''
    返回JSON字符串
    :param msg: 返回信息
    :param code: 状态 0成功 1失败
    :param data: 返回数据
    :return:
    '''
    return json.dumps({'code': code, 'msg': msg, 'data': data})
