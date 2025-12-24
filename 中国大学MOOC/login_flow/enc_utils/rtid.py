import string
import random

def generate_rtid():
    length = 32
    # 定义字符池：包含数字、大写字母和小写字母
    characters = string.ascii_letters + string.digits
    # 随机选择 length 个字符并拼接
    return ''.join(random.choices(characters, k=length))

if __name__ == '__main__':
    print(generate_rtid())