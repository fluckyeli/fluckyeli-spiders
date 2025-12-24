import json
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT


def sm4_encrypt(data, hex_key="BC60B8B9E4FFEFFA219E5AD77F11F9E2"):
    """
    模拟前端加密逻辑
    :param data: 字典或对象 (会被 JSON.stringify)
    :param hex_key: 16进制字符串密钥 (32位字符)
    """
    # 1. 序列化数据 (对应 JSON.stringify)
    # 注意：ensure_ascii=False 保证中文处理与 JS 一致，separators 去除空格
    input_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    # 2. 初始化 SM4 实例
    crypt_sm4 = CryptSM4()

    # 3. 设置密钥 (将 16 进制字符串转为 bytes)
    key_bytes = bytes.fromhex(hex_key)
    crypt_sm4.set_key(key_bytes, SM4_ENCRYPT)

    # 4. 加密 (gmssl 默认处理 PKCS7 填充，默认模式通常为 ECB)
    encrypt_bytes = crypt_sm4.crypt_ecb(input_str.encode('utf-8'))

    # 5. 返回 16 进制字符串 (对应前端常见输出)
    return encrypt_bytes.hex()


def sm4_decrypt(hex_data, hex_key="BC60B8B9E4FFEFFA219E5AD77F11F9E2"):
    """
    实现与前端对应的 SM4 解密
    :param hex_data: 16进制加密字符串
    :param hex_key: 16进制字符串密钥 (32位字符)
    :return: 解密后的原始对象 (dict 或 list)
    """
    # 1. 初始化 SM4 实例
    crypt_sm4 = CryptSM4()

    # 2. 设置密钥并指定为解密模式
    key_bytes = bytes.fromhex(hex_key)
    crypt_sm4.set_key(key_bytes, SM4_DECRYPT)

    # 3. 将加密的 16 进制字符串转为字节流并解密
    # gmssl 的 crypt_ecb 在 DECRYPT 模式下会自动处理 PKCS7 去填充
    decrypt_bytes = crypt_sm4.crypt_ecb(bytes.fromhex(hex_data))

    # 4. 将字节流解码为 UTF-8 字符串
    decrypted_str = decrypt_bytes.decode('utf-8')

    return decrypted_str


if __name__ == '__main__':
    _sm4pubkey = "BC60B8B9E4FFEFFA219E5AD77F11F9E2"
    s_data = {
        "un": "test123@163.com",
        "pkid": "cjJVGQM",
        "pd": "imooc",
        "channel": 0,
        "topURL": "https://www.icourse163.org/",
        "rtid": "QjEo5lOdukBXvcjjFrs2IvWVFm4Gmxfv"
    }

    result = sm4_encrypt(s_data, _sm4pubkey)
    print(f"加密后的结果: {result}")

    last_encrypted_result = "84497406fe47bded5c26fa9830987a18feb68d4e9342b4b7a76d6c2ebb3686a1455909dee61047a38361045020c74aab0a682f7a88c2052aa516992a23c6da55383d92b5128cc34083b5549a63425684a123e33ebf2ee575be166b6728128f7f1c103f6c9d0acf7b0fc4c20f8194073b5c0132c16451cd667c902403d8afb947834301bed3600a6d62b49f299aeae2b1583cd73dd36c2a8817671dcdcb947d5f9c76f07ad7391d77518de13a694c301116c468d38ae39712f4f91834dab60abb28e25907136fd71850d5ba3829df50649169d6d04dab8e6ad8331c4fcd4ce1fc4d9293953ca84b80e7521dad0723225b43cf4b4ea45ee7cd1f033f7ddc3edb8f01b7ee894ddf42da7c149de6c183782061bcd2c7d8f88394f150fc898ccf7f7541788f2e93fbbdc36d35c9f82ba11ee2d9b2d98df5aa91f58179f98ebac1f47dbdf5b0828ee381085d7e40eed19c4f5ef2264615e099a8a70ca7cbccd78c80e2d46ccf95720d15bd9e59b5f953b42680cfb2ea40838cef581de9b047415696582dd521a60f40aa3833aaa23ccf8898c9a395f425ae9bf5ceaba512da192eea2ac7cf27db51d0327945ca613c081dd26673d66adcbeb2a37e554e691c81c8f5688701d2ff1ac01343e9ea29196453177363c6408873be9c361370491e0babdaea3a59fce3d62192a0397c5bfe30c731aa77e4487cf397bd0d209fe2fb4bb1da49cfdd5a57ae97fe7dbe002511c0bc5f01f4492ec56b98a54c5258c82512b5abbaba6410f18c782e0deb67bfe8b3cf88f648afcc5b6a68eacf0613ad32dce8f41668bfd77308f204c217641fbfba3340d5ea8d3c622d22ca70bee601b19c7b13c798c87184cfbf24e71901cd1a7bf50684ce67090e1d2e5f979c0e215413a10bcc4d50a010e2e42731de47e345cecb6603b8ae3e71d178d712a320c17ebc61799326da4ee00fcc7399e5e5625611f2ed78df8351b0c5878bd7bc2f93a430ac5a27ce72d1db46d675e66d2468fb0824361798cd49a6b9f18259be1fc0bda0287695c438b1d9068d97beae847835bf11d2d4d18394bf7b4dbcf24500c31d2e26e1a2050f7dce570c19f2b44454c48fe7b6916a8cdfe8537a555a17b2d6303d75bed95ee1d1ffe0b698886592c090f36692aa3625b954585b7dc2a354ec78ac114a6ad24f42c9a06c89e6f4d930cf1e25f24e8e467dd3c6a4c14d0a92423a291f217794b07ac528e7df8466334985afa835c0740cc70ef102815e444b6ba9d5b93133dbbe706b6dd0e7b751f0c69016dfcad5f1067ae839b226143cb06870c87d3d48cbac47a4b97a1c3f84d72971c7720a6a"
    print(result == last_encrypted_result)

    decrypted_result_my = sm4_decrypt(result, _sm4pubkey)
    print(f"我的加密解密后的结果: {decrypted_result_my}")

    encode = "ed72279d0e51430a02d946f482f3f26ef55fe67674fce34b9c0f09f4b0c2e7cbfbb302f361b69dfae639d48f839abf7f3520d346ebea5c6d7fb9914d66d0c5993af0176b1c7f13691d1286f4e51310c094ae7e704faa2a8694e719e285cadea69225b741f5aba3ade9d1309e32fe910cc4d999fb422c8da71e92ec552329d770"
    decrypted_result = sm4_decrypt(encode, _sm4pubkey)
    print(f"解密后的结果: {decrypted_result}")
