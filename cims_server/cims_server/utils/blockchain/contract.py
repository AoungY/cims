import json

import requests
from django.conf import settings

from cims_server.utils.utils import decrypt_message, verify_signature

# 政府角色公私钥 长度1024
government_private_key = settings.BLOCKCHAIN['government_private_key']
government_public_key = settings.BLOCKCHAIN['government_public_key']

# blockchain_url = 'http://localhost:5002/WeBASE-Front/trans/handle'  # 本地区块链服务地址
# blockchain_url = 'http://175.178.154.217:5002/WeBASE-Front/trans/handle'  # 云端区块链服务地址
blockchain_url = settings.BLOCKCHAIN['url']  # 云端区块链服务地址


class Contract:
    def __init__(self):
        self.contract_user_public_key = settings.BLOCKCHAIN['contract_user_public_key']  # 区块链合约用户公钥
        self.IdentityCard = {"contractAddress": settings.BLOCKCHAIN['IdentityCard_contractAddress'],
                             "contractName": "IdDataStorage",
                             "funcName": {"get": "getIdDataByUserPk", "add": "addIdData"},
                             "get_contractAbi_name": "getIdDataByUserPk",
                             "inputs_name": "idData",
                             }

        self.Passport = {"contractAddress": settings.BLOCKCHAIN['Passport_contractAddress'],
                         "contractName": "PassportDataStorage",
                         "funcName": {"get": "getPassportDataByUserPk", "add": "addPassportData"},
                         "get_contractAbi_name": "getPassportDataByUserPk",
                         "inputs_name": "passportData",
                         }

        self.now_certificate = None  # 当前操作的证件类型
        self.user_public_key = None  # 当前用户公钥
        self.user_private_key = None  # 当前用户私钥

    def _get_func_param(self, certificate_str):
        """
            用来获取最终func_param的期望的格式
            certificate_str是传入的证件模型实例的str，具体方法见证件模型的__str__方法
        """

        res = f'["{self.user_public_key}","{government_public_key}",{certificate_str}]'
        # res = f'["{self.user_public_key}","{government_public_key}",{certificate_str}]'
        return res

    def set_now_certificate(self, certificate):
        """
            设置当前操作的证件类型
        """
        self.now_certificate = certificate

    def set_user_public_key(self, user_public_key):
        """
            设置当前用户公钥
        """
        self.user_public_key = user_public_key

    def get_data(self):
        """
            根据当前用户密钥和证件雷系在区块链中获取数据
        """
        # 判断是否有用户公钥和当前证件类型
        if not self.user_private_key: raise Exception("user_private_key为None")
        if not self.user_public_key: raise Exception("user_public_key为None")
        if not self.now_certificate: raise Exception("now_certificate为None")
        data = {
            "groupId": "1",
            "user": "",
            "contractName": self.now_certificate["contractName"],
            "contractPath": "/",
            "version": "",
            "funcName": self.now_certificate["funcName"]["get"],
            "funcParam": [self.user_public_key],
            "contractAddress": self.now_certificate["contractAddress"],
            "contractAbi": [
                {
                    "constant": True,
                    "inputs": [
                        {
                            "name": "userPk",
                            "type": "string",
                            "value": self.user_public_key
                        }
                    ],
                    "name": self.now_certificate["get_contractAbi_name"],
                    "outputs": [
                        {
                            "components": [
                                {
                                    "name": "userPk",
                                    "type": "string"
                                },
                                {
                                    "name": "govPk",
                                    "type": "string"
                                },
                                {
                                    "name": "signature",
                                    "type": "string"
                                },
                                {
                                    "name": "id",
                                    "type": "string"
                                },
                                {
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "name": "gender",
                                    "type": "string"
                                },
                                {
                                    "name": "date_of_birth",
                                    "type": "string"
                                },
                                {
                                    "name": "country",
                                    "type": "string"
                                },
                                {
                                    "name": "number",
                                    "type": "string"
                                },
                                {
                                    "name": "issuing_authority",
                                    "type": "string"
                                },
                                {
                                    "name": "issuing_country",
                                    "type": "string"
                                },
                                {
                                    "name": "start",
                                    "type": "string"
                                },
                                {
                                    "name": "expiration",
                                    "type": "string"
                                },
                                {
                                    "name": "photo",
                                    "type": "string"
                                },
                                {
                                    "name": "prepp",
                                    "type": "string"
                                },
                                {
                                    "name": "futurepp",
                                    "type": "string"
                                },
                                {
                                    "name": "idcard",
                                    "type": "string"
                                }
                            ],
                            "name": "",
                            "type": "tuple[]"
                        }
                    ],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function",
                    "funcId": 0
                }
            ],
            "useAes": False,
            "useCns": False,
            "cnsName": ""
        }
        try:
            res = requests.post(blockchain_url, json=data)
            # 发送请求
            data = json.loads(res.json()[0])
            for i in range(len(data)):
                # 验证签名
                if not verify_signature(decrypt_message(data[i][3], self.user_private_key), data[i][2], government_public_key):
                    data[i] = None
                    print("签名验证失败", data[i])
                    continue

                # 对item[3:]进行解密,因为前两个是公钥,第三个是签名，不需要解密
                # 注:这里用用户的私钥解密，因为这个加密是使用用户的公钥进行加密的
                data[i] = [decrypt_message(_, self.user_private_key) for _ in data[i][3:]]
            data = [i for i in data if i]  # 去掉签名验证失败的数据
            # print("get_data", res.status_code, len(data), data, self.now_certificate)
            return data
        except:
            return False

    def add_data(self, certificate_str):
        if not self.user_public_key: raise Exception("user_public_key为None")
        if not self.now_certificate: raise Exception("now_certificate为None")

        funcParam = self._get_func_param(certificate_str)
        data = {
            "groupId": "1",
            "user": self.contract_user_public_key,
            "contractName": self.now_certificate["contractName"],
            "contractPath": "/",
            "version": "",
            "funcName": self.now_certificate["funcName"]["add"],
            "funcParam": [funcParam],
            "contractAddress": self.now_certificate["contractAddress"],
            "contractAbi": [
                {
                    "constant": False,
                    "inputs": [
                        {
                            "name": self.now_certificate["inputs_name"],
                            "type": "string[]",
                            "value": funcParam
                        }
                    ],
                    "name": self.now_certificate["funcName"]["add"],
                    "outputs": [],
                    "payable": False,
                    "stateMutability": "nonpayable",
                    "type": "function",
                    "funcId": 0
                }
            ],
            "useAes": False,
            "useCns": False,
            "cnsName": ""
        }
        res = requests.post(blockchain_url, json=data)
        try:
            # 测试是否成功，返回值是否是json格式
            # print("add_data", res.status_code, res.json())
            return res.status_code == 200
        except:
            return False
