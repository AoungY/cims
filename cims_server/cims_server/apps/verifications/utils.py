import base64
import hashlib

import jwt
from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class SimpleUser:
    """
    一个简单的用户类，只有一个is_authenticated属性,用于JWT认证
    """

    def __init__(self, payload):
        self.payload = payload

    @property
    def is_authenticated(self):
        return True


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token已过期')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('无效的token')

        # 返回一个SimpleUser实例和None
        return (SimpleUser(payload), None)


# 从Django的SECRET_KEY生成Fernet密钥
def generate_fernet_key(secret_key):
    # 使用SHA-256哈希算法，确保密钥长度符合要求
    hash_key = hashlib.sha256(secret_key.encode()).digest()
    # 转换为base64编码以符合Fernet密钥格式
    return base64.urlsafe_b64encode(hash_key)


def encrypt_payload(public_key, private_key):
    """
        用SECRET_KEY加密public_key, private_key
        返回payload
    """
    # 获取Django的SECRET_KEY
    django_secret_key = settings.SECRET_KEY
    fernet_key = generate_fernet_key(django_secret_key)

    cipher_suite = Fernet(fernet_key)

    # 使用SECRET_KEY加密public_key和private_key
    encrypted_public_key = cipher_suite.encrypt(public_key.encode())
    encrypted_private_key = cipher_suite.encrypt(private_key.encode())

    payload = {
        'public_key': encrypted_public_key.decode(),  # 将bytes转换为字符串以便编码
        'private_key': encrypted_private_key.decode()
    }
    return payload


def decrypt_payload(encrypted_payload):
    """
    使用从Django的SECRET_KEY生成的Fernet密钥解密payload
    """
    django_secret_key = settings.SECRET_KEY
    fernet_key = generate_fernet_key(django_secret_key)
    cipher_suite = Fernet(fernet_key)

    # 解密public_key和private_key
    decrypted_public_key = cipher_suite.decrypt(encrypted_payload['public_key'].encode())
    decrypted_private_key = cipher_suite.decrypt(encrypted_payload['private_key'].encode())

    # 将解密后的结果组合成新的payload
    decrypted_payload = {
        'public_key': decrypted_public_key.decode(),
        'private_key': decrypted_private_key.decode()
    }
    return decrypted_payload


def get_payload(request):
    """
    解码JWT token获取原始payload
    """
    token = request.headers.get('Authorization')

    if not token: return None

    # 解码JWT token获取加密的payload
    encrypted_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    # 使用密钥解密payload
    decrypted_payload = decrypt_payload(encrypted_payload)
    return decrypted_payload
