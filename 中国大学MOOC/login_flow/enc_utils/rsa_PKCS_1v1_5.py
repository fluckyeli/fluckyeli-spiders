# pip install pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


def rsa_encrypt(key_base64, message):
    try:
        # 1. 彻底去除可能存在的标签和换行符，只保留 Base64 核心内容
        pure_base64 = (
            key_base64.replace("-----BEGIN PUBLIC KEY-----", "")
            .replace("-----END PUBLIC KEY-----", "")
            .replace("\n", "")
            .replace("\r", "")
            .strip()
        )

        # 2. 将 Base64 解码为二进制 DER 格式
        key_der = base64.b64decode(pure_base64)

        # 3. 直接从二进制导入
        key = RSA.import_key(key_der)

        # 4. 加密逻辑保持不变
        cipher = PKCS1_v1_5.new(key)
        ciphertext = cipher.encrypt(message.encode('utf-8'))
        return base64.b64encode(ciphertext).decode('utf-8')

    except Exception as e:
        return f"加密失败: {str(e)}"

if __name__ == '__main__':
    pub_key = """-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB-----END PUBLIC KEY-----"""
    result = rsa_encrypt(pub_key, "123456")
    print(result)