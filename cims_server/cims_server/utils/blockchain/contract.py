import json

import requests

# 政府角色公私钥 长度1024
government_private_key = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUNkd0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQW1Fd2dnSmRBZ0VBQW9HQkFML0NDUkR0TlJ1bjM0UnoKVXBnSXQ4SEFZRUlnUW5XQTNJSzJhcWJ1VlByVlkzVUsveS9DL0tneEt6TFNZL2RZYXFtQXFOU3NzRHhCeUpTLwpxOFEvcUVxcWh2UG5yTHU0dUZQZlpwRHFNbXNybXhieVpZRmVFaENrNGMrOVlYK1k2dTQ5R1ZDenhTcEV2WDR5CmF4ZTJ4a1QvenJ4elFKc2ZiUlZXS2k2OHMwNUJBZ01CQUFFQ2dZRUFwYzdGd0JrYi90bmRiODIzOFRZNGpoUW0KSjRkMWI5MEl6dzJra3NzcU4rb2pvYVRzbXdQakxCdTMycTRKT21yOWI2dU1VTGt4ZWlqM280ZElvdHpZU3BhQgoyMUJwM1B0bFR3dUgwNVpwWkluTE85QUg5UWZsSVdpREtSTTNWYldCY3FPeC9MMGdMSDJBM0s5dmhvQ2l6UTNXCmxqY2NVTVNkdW0yYUZ0TDNpMEVDUVFEMTU0UTBEZEo2U0htZE1PM0lSWG9hOXJNT0ZZSTEzZmZXS2hwbkFkWEYKNG1WSDk2djl2SHhKTU9vSkVROWJTem1Oam1sQlJ3T2E3eDg3SzZTYjRuOTlBa0VBeDZGdkU3WnFBWldYRWVtLwpIUE9ySXh4akM3NGNpakF3RjY2dkpZdlhPeHBzZmV0eTh5bEF1UXQ1d25vd1UrdmluM2JsaWEwVlZmeDVrYVFCCmtUT05GUUpBRDdFRVdLWUJKbGgxbWpoREZDS0sxaW1qNTJRcitPLy9IcVYxSmRtU0lKeC94Z1hoN2NFWFZUeFAKMHVCSjBKT09TcUFweTBhU3psSXY5Z0NrOG1XVHFRSkFGMEQwd1dVVVFBNyt3L1ZvYjZUcW9ISmtEekFiL3ZUUwpCVkF4MHJ2UlhHOGRpQ1Z2QkdnZncrNVVScFVaSUExd0hvY3BBYnFKcTdSM0xNSGY5TnYrYVFKQkFJUFJZRFBJCklUaUIzV3Jmak9pWTYzQVIyYW9zbVU2cEt1cnFYL1o1Z05SRHRsL2lPdElsUUc4VkZMZTBRb1lEQWhQMmVjVzYKVW5SWDRsK2ROdVVvQS80PQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg=="
government_public_key = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDL3dna1E3VFVicDkrRWMxS1lDTGZCd0dCQwpJRUoxZ055Q3RtcW03bFQ2MVdOMUN2OHZ3dnlvTVNzeTBtUDNXR3FwZ0tqVXJMQThRY2lVdjZ2RVA2aEtxb2J6CjU2eTd1TGhUMzJhUTZqSnJLNXNXOG1XQlhoSVFwT0hQdldGL21PcnVQUmxRczhVcVJMMStNbXNYdHNaRS84NjgKYzBDYkgyMFZWaW91dkxOT1FRSURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQo==="

blockchain_url = 'http://localhost:5002/WeBASE-Front/trans/handle'  # 本地区块链服务地址


class Contract:
    def __init__(self):
        self.contract_user_public_key = "0x24f5b700d2e66ab27468c6eeba53e25c9f4805fd"  # 区块链合约用户公钥
        self.IdentityCard = {"contractAddress": "0xd297c9364818d5968f34fa5d0e99d5a673ce17e5",
                             "contractName": "IdDataStorage",
                             "funcName": {"get": "getIdDataByUserPk", "add": "addIdData"},
                             "get_contractAbi_name": "getIdDataByUserPk",
                             "inputs_name": "idData",
                             }

        self.Passport = {"contractAddress": "0x1baa583e4babf6bbbef8bf0c5066aa2b4407788e",
                         "contractName": "PassportDataStorage",
                         "funcName": {"get": "getPassportDataByUserPk", "add": "addPassportData"},
                         "get_contractAbi_name": "getPassportDataByUserPk",
                         "inputs_name": "passportData",
                         }

        self.now_certificate = None  # 当前操作的证件类型
        self.user_public_key = None  # 当前用户公钥

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
                                    "name": "eth_group",
                                    "type": "string"
                                },
                                {
                                    "name": "addr",
                                    "type": "string"
                                },
                                {
                                    "name": "number",
                                    "type": "string"
                                },
                                {
                                    "name": "date_of_birth",
                                    "type": "string"
                                },
                                {
                                    "name": "authority",
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
                                    "name": "preid",
                                    "type": "string"
                                },
                                {
                                    "name": "futureid",
                                    "type": "string"
                                },
                                {
                                    "name": "pp",
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
        res = requests.post(blockchain_url, json=data)
        data = json.loads(res.json()[0])

        print("get_data", res.status_code, len(data), data, self.now_certificate)

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
        print("add_data", res.status_code, res.json())
