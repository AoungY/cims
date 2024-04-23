import requests


def set_id_data(userPk, govPk, id, name, gender, eth_group, addr, number, date_of_birth, authority, start, expiration,
                photo, preid, futureid, pp):
    url = 'http://localhost:5002/WeBASE-Front/trans/handle'
    data = {

        "groupId": "1",
        "user": "0x825f8401f4c7cb0bde149abad7f530889e705032",
        "contractName": "IdDataStorage",
        "contractPath": "/",
        "version": "",
        "funcName": "addIdData",
        "funcParam": [
            "[\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"]".format(
                userPk, govPk, id, name, gender, eth_group, addr, number, date_of_birth, authority, start, expiration,
                photo, preid, futureid, pp)
        ],
        "contractAddress": "0xe44dfc8a4e3ffebef24093606f9ee954a1af380a",
        "contractAbi": [
            {
                "constant": False,
                "inputs": [
                    {
                        "name": "idData",
                        "type": "string[]",
                        "value": "[\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\",\"2\"]"
                    }
                ],
                "name": "addIdData",
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
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        # 处理返回的结果
        return result
    else:
        return "Error: " + str(response.status_code)


def get_id_data(userPk):
    url = 'http://localhost:5002/WeBASE-Front/trans/handle'
    data = {

        "groupId": "1",
        "user": "",
        "contractName": "IdDataStorage",
        "contractPath": "/",
        "version": "",
        "funcName": "getIdDataByUserPk",
        "funcParam": [
            userPk
        ],
        "contractAddress": "0xe44dfc8a4e3ffebef24093606f9ee954a1af380a",
        "contractAbi": [
            {
                "constant": True,
                "inputs": [
                    {
                        "name": "userPk",
                        "type": "string",
                        "value": "2"
                    }
                ],
                "name": "getIdDataByUserPk",
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
                "funcId": 1
            }
        ],
        "useAes": False,
        "useCns": False,
        "cnsName": ""

    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        # 处理返回的结果
        return result
    else:
        return "Error: " + str(response.status_code)


# print(set_id_data("3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3"))
# print(get_id_data("3"))
def set_passport_data(userPk, govPk, id, name, gender, date_of_birth, country, number, issuing_authority,
                      issuing_country, start, expiration,
                      photo, prepp, futurepp, idcard):
    url = 'http://localhost:5002/WeBASE-Front/trans/handle'
    data = {
        "groupId": "1",
        "user": "0x825f8401f4c7cb0bde149abad7f530889e705032",
        "contractName": "PassportDataStorage",
        "contractPath": "/",
        "version": "",
        "funcName": "addPassportData",
        "funcParam": [
            "[\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"]".format(
                userPk, govPk, id, name, gender, date_of_birth, country, number, issuing_authority, issuing_country,
                start, expiration,
                photo, prepp, futurepp, idcard)
        ],
        "contractAddress": "0xc3598914b91ca7bd1c8190c739dcdaf6d9288a64",
        "contractAbi": [
            {
                "constant": False,
                "inputs": [
                    {
                        "name": "passportData",
                        "type": "string[]",
                        "value": "[\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\",\"1\"]"
                    }
                ],
                "name": "addPassportData",
                "outputs": [],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function",
                "funcId": 1
            }
        ],
        "useAes": False,
        "useCns": False,
        "cnsName": ""
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        # 处理返回的结果
        return result
    else:
        return "Error: " + str(response.status_code)


def get_passport_data(userPk):
    url = 'http://localhost:5002/WeBASE-Front/trans/handle'
    data = {
        "groupId": "1",
        "user": "",
        "contractName": "PassportDataStorage",
        "contractPath": "/",
        "version": "",
        "funcName": "getPassportDataByUserPk",
        "funcParam": [
            userPk
        ],
        "contractAddress": "0xc3598914b91ca7bd1c8190c739dcdaf6d9288a64",
        "contractAbi": [
            {
                "constant": True,
                "inputs": [
                    {
                        "name": "userPk",
                        "type": "string",
                        "value": "1"
                    }
                ],
                "name": "getPassportDataByUserPk",
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
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        # 处理返回的结果
        return result
    else:
        return "Error: " + str(response.status_code)


# print(set_passport_data("3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3"))
print(get_passport_data("3"))
