import base64
import binascii

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


# 生成公私钥对
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # 私钥序列化并编码为Base64
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    base64_private = base64.b64encode(pem_private).decode('utf-8').replace('\n', '')

    # 公钥序列化并编码为Base64
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    base64_public = base64.b64encode(pem_public).decode('utf-8').replace('\n', '')

    return base64_private, base64_public


# 加密
def encrypt_message(message, base64_public_key):
    # 解码公钥
    public_key_data = base64.b64decode(base64_public_key.encode('utf-8'))
    public_key = serialization.load_pem_public_key(
        public_key_data,
        backend=default_backend()
    )

    try:
        # 加密
        encrypted_message = public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        encrypted_message = public_key.encrypt(
            binascii.unhexlify(message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    # 加密消息编码为Base64
    return base64.b64encode(encrypted_message).decode('utf-8')


# 解密
def decrypt_message(encrypted_message, base64_private_key):
    # 解码私钥
    private_key_data = base64.b64decode(base64_private_key.encode('utf-8'))
    private_key = serialization.load_pem_private_key(
        private_key_data,
        password=None,
        backend=default_backend()
    )

    # 解密
    decrypted_message = private_key.decrypt(
        base64.b64decode(encrypted_message.encode('utf-8')),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    try:
        # 尝试将解密后的二进制数据转换为UTF-8编码的字符串
        return decrypted_message.decode('utf-8')
    except:
        # 将解密后的二进制数据转换为十六进制字符串,用于解密本身为十六进制的情况
        return binascii.hexlify(decrypted_message).decode('utf-8')


def verify_key_pair(public_key, private_key):
    # 测试消息
    test_message = "test message"

    try:
        # 使用公钥加密消息
        encrypted_message = encrypt_message(test_message, public_key)
        # 使用私钥解密消息
        decrypted_message = decrypt_message(encrypted_message, private_key)

        # 检查解密后的消息是否与原始消息相同
        return decrypted_message == test_message
    except Exception as e:
        # 如果在加密或解密过程中出现任何异常，说明公私钥不匹配
        print("An error occurred:", str(e))
        return False


# 对消息进行签名
def sign_message(message, base64_private_key):
    # 解码私钥
    private_key_data = base64.b64decode(base64_private_key.encode('utf-8'))
    private_key = serialization.load_pem_private_key(
        private_key_data,
        password=None,
        backend=default_backend()
    )

    message = message.encode('utf-8')
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    # 返回Base64编码的签名
    return base64.b64encode(signature).decode('utf-8')


# 验证签名
def verify_signature(message, signature, base64_public_key):
    # 解码公钥
    public_key_data = base64.b64decode(base64_public_key.encode('utf-8'))
    public_key = serialization.load_pem_public_key(
        public_key_data,
        backend=default_backend()
    )

    message = message.encode('utf-8')
    signature = base64.b64decode(signature)
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print("Verification failed:", e)
        return False


# 主函数
def sign_test_main():
    # 生成密钥
    private_key, public_key = generate_keys()

    # 待签名的消息
    message = "This is a message to sign"

    # 签名消息
    signature = sign_message(message, private_key)
    print("Signature:", signature)

    # 验证签名
    verification_result = verify_signature(message, signature, public_key)
    print("Verification result:", verification_result)


# 使用示例
def main_verification():
    private_key, public_key = generate_keys()
    print("Verification result:", verify_key_pair(public_key, private_key))


# 主函数
def main():
    # 生成公私钥
    private_key, public_key = generate_keys()
    # public_key, private_key = generate_keys()

    # public_key = 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDL1VWTDdoWGFPbU9Eek9hajFBWjNzdzg3bApvTjdRL0FuY0NjajhjQTdUYXUxT2w0amdUQmxSOFZVOEo5dlZkK0liN2NXc2R1UGg1TnNOcXg4NkcxQm5ZRmhXCkt3RnRJeHladjEwS2hrYmtxdm82Nys0cTJ6VzluejdrUVdh'
    # 打印公私钥
    print("Private Key is:", len(private_key), private_key)
    print("Public Key is:", len(public_key), public_key)

    # 待加密的信息
    message = "message to be encrypted"

    # 加密
    encrypted_message = encrypt_message(message, public_key)
    print("Encrypted Message is:", encrypted_message)

    # 解密
    decrypted_message = decrypt_message(encrypted_message, private_key)
    print("Decrypted Message is:", decrypted_message)


if __name__ == "__main__":
    main()
    main_verification()
    sign_test_main()
