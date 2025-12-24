import hashlib
import time
import urllib.parse
import mmh3
import json
from typing import Dict, Any, Optional


def vdf_function_calculate(data: Dict[str, Any], calc_type: str = "sync", callback=None) -> Optional[Dict[str, Any]]:
    """
    可验证延迟函数（VDF）计算器

    实现与JS代码相同的VDF计算功能，用于工作量证明(PoW)中的时间延迟验证。
    通过连续平方取模运算产生计算上不可加速的结果，确保证明者付出了真实的时间。

    Args:
        data (Dict[str, Any]): VDF计算输入参数，具体结构如下：
            {
                "needCheck": bool,       # 是否需要进行结果验证（预留字段，JS代码中未使用）
                "sid": str,              # 会话ID，用于标识唯一计算请求
                "hashFunc": str,         # 哈希函数类型，必须为"VDF_FUNCTION"
                "maxTime": int,          # 最大计算时间（毫秒），超过此时间强制停止
                "minTime": int,          # 最小计算时间（毫秒），至少运行这么长时间
                "args": Dict[str, Any]   # 具体计算参数，包含：
                    {
                        "mod": str,      # 模数（十六进制字符串），用于模运算
                        "t": int,        # 目标迭代次数，理论上需要执行这么多次平方
                        "puzzle": str,   # 挑战谜题（Base64编码字符串），作为标识符
                        "x": str         # 初始值（十六进制字符串），计算起点
                    }
            }
        calc_type (str, optional): 计算类型，支持"sync"（同步）和"async"（异步）。默认为"sync"
        callback (Callable, optional): 异步计算时的回调函数，计算结果将通过此函数返回。默认为None

    Returns:
        Optional[Dict[str, Any]]: 同步模式下返回计算结果字典，异步模式下返回None（结果通过回调函数返回）

        返回格式：
        {
            "maxTime": int,              # 传入的最大计算时间（毫秒）
            "puzzle": str,               # 输入的挑战谜题（Base64编码字符串）
            "spendTime": int,            # 实际计算耗时（毫秒）
            "runTimes": int,             # 实际执行迭代次数
            "sid": str,                  # 会话ID，与输入一致
            "args": str                  # 计算结果参数（JSON字符串），包含：
                {
                    "x": str,            # 最终计算结果（十六进制字符串）
                    "t": int,            # 实际执行迭代次数（与runTimes相同）
                    "sign": int          # 结果签名，用于验证结果完整性和防篡改
                }
        }

    Raises:
        ValueError: 如果输入参数格式不正确或必需参数缺失
        TypeError: 如果参数类型不符合要求
    Notes:
        1. 本函数模拟了VDF的核心思想：通过重复计算x = (x² mod m)产生时间延迟
        2. 签名算法使用MurmurHash3，确保结果不可伪造
        3. 实际迭代次数可能小于目标值t，当超过maxTime时会提前停止
        4. 即使提前停止，也至少运行minTime毫秒
        5. 签名基于运行时间、迭代次数和结果计算，防止结果被篡改
    """

    # 验证输入参数格式
    if not isinstance(data, dict):
        raise TypeError("输入参数data必须是字典类型")

    # 检查必需字段
    required_fields = ["sid", "hashFunc", "maxTime", "minTime", "args"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")

    # 验证hashFunc类型
    if data["hashFunc"] != "VDF_FUNCTION":
        raise ValueError(f"不支持的hashFunc类型: {data['hashFunc']}，只支持VDF_FUNCTION")

    # 验证args参数
    args = data["args"]
    if not isinstance(args, dict):
        raise TypeError("args字段必须是字典类型")

    required_args = ["mod", "t", "puzzle", "x"]
    for arg in required_args:
        if arg not in args:
            raise ValueError(f"缺少必需的args参数: {arg}")

    # 验证数值类型
    if not isinstance(data["maxTime"], (int, float)):
        raise TypeError("maxTime必须是数值类型")
    if not isinstance(data["minTime"], (int, float)):
        raise TypeError("minTime必须是数值类型")

    # 创建计算器实例
    calculator = VDFCalculator()

    # 执行计算
    if calc_type == "sync":
        return calculator.vdf_calculate(data)
    elif calc_type == "async":
        if callback is None:
            raise ValueError("异步模式必须提供callback回调函数")

        # 异步模式下在新线程中执行计算
        import threading
        thread = threading.Thread(
            target=calculator.vdf_calculate,
            args=(data, callback)
        )
        thread.daemon = True
        thread.start()
        return None
    else:
        raise ValueError(f"不支持的calc_type: {calc_type}，只支持'sync'或'async'")


class VDFCalculator:
    """VDF计算器内部实现类"""

    def pow_sign(self, key: str, seed: int) -> int:
        """
        MurmurHash3算法实现，用于计算结果签名

        Args:
            key (str): 需要签名的字符串
            seed (int): 哈希种子

        Returns:
            int: 32位无符号整数签名
        """
        key_bytes = key.encode('utf-8')
        h = mmh3.hash(key_bytes, seed)
        return h & 0xffffffff

    def vdf_calculate(self, data: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """
        执行VDF计算的核心方法

        Args:
            data: 输入数据
            callback: 回调函数（仅异步模式使用）

        Returns:
            VDF计算结果
        """
        # 提取参数
        max_time = int(data["maxTime"])
        min_time = int(data["minTime"])
        sid = data["sid"]
        args = data["args"]

        puzzle = args["puzzle"]
        mod_hex = args["mod"]
        x_hex = args["x"]
        t_str = args["t"]

        # 将t转换为整数
        try:
            target_iterations = int(t_str)
        except (ValueError, TypeError):
            target_iterations = 0

        # 记录开始时间
        start_time = time.time() * 1000  # 转换为毫秒

        # 将十六进制字符串转换为整数
        try:
            current_x = int(x_hex, 16)
            modulus = int(mod_hex, 16)
        except (ValueError, TypeError):
            # 如果转换失败，返回错误结果
            error_result = {
                "maxTime": max_time,
                "puzzle": puzzle,
                "spendTime": 0,
                "runTimes": 0,
                "sid": sid,
                "args": json.dumps({"error": "参数格式错误"})
            }
            if callback:
                callback(error_result)
            return error_result

        # 检查模数是否有效
        if modulus <= 0:
            error_result = {
                "maxTime": max_time,
                "puzzle": puzzle,
                "spendTime": 0,
                "runTimes": 0,
                "sid": sid,
                "args": json.dumps({"error": "模数必须为正整数"})
            }
            if callback:
                callback(error_result)
            return error_result

        # VDF核心计算
        actual_iterations = 0

        # 循环执行平方取模运算
        for i in range(target_iterations):
            # 检查是否超过最大时间
            current_time = time.time() * 1000
            elapsed_time = current_time - start_time

            if elapsed_time > max_time:
                # 超过最大时间，提前退出
                break

            # 执行一次平方取模运算：x = (x * x) % mod
            current_x = (current_x * current_x) % modulus
            actual_iterations += 1

            # 确保至少运行最小时间
            if i == 0 and elapsed_time < min_time:
                # 继续运行直到达到最小时间
                continue

        # 计算实际耗时
        spend_time = int(time.time() * 1000 - start_time)

        # 准备签名参数
        sign_obj = {
            "runTimes": actual_iterations,
            "spendTime": spend_time,
            "t": actual_iterations,
            "x": format(current_x, 'x')  # 转换为十六进制字符串
        }

        # 按字母顺序排序参数并编码（与JS实现一致）
        sorted_params = sorted(sign_obj.keys())
        encoded_params = []

        for key in sorted_params:
            value = sign_obj[key]
            # 使用urllib.parse进行URL编码
            encoded_key = urllib.parse.quote(str(key), safe='')
            encoded_value = urllib.parse.quote(str(value), safe='')
            encoded_params.append(f"{encoded_key}={encoded_value}")

        encoded_string = "&".join(encoded_params)

        # 计算签名
        signature = self.pow_sign(encoded_string, actual_iterations)

        # 构建结果参数
        result_args = {
            "x": format(current_x, 'x'),
            "t": actual_iterations,
            "sign": signature
        }

        # 构建完整结果
        result = {
            "maxTime": max_time,
            "puzzle": puzzle,
            "spendTime": spend_time,
            "runTimes": actual_iterations,
            "sid": sid,
            "args": json.dumps(result_args)  # 转换为JSON字符串
        }

        # 如果有回调函数，则调用它
        if callback:
            callback(result)

        return result


def sync_vdf_work(input_data):
    result = vdf_function_calculate(input_data, calc_type="sync")
    return result

def async_vdf_work(input_data, callback):
    vdf_function_calculate(input_data, calc_type="async", callback=callback)
    time.sleep(1) # 等待异步计算完成


# 使用示例函数
def example_usage():
    """
    VDF函数使用示例

    演示如何调用vdf_function_calculate函数进行VDF计算
    """

    # 示例输入数据（与问题中的格式完全一致）
    input_data = {
        "needCheck": True,  # 是否需要验证结果（预留字段）
        "sid": "e39c41b0-46c8-432c-9eb6-12de12d5c890",  # 会话ID
        "hashFunc": "VDF_FUNCTION",  # 哈希函数类型
        "maxTime": 1050,  # 最大计算时间（毫秒）
        "minTime": 1000,  # 最小计算时间（毫秒）
        "args": {  # 计算参数
            "mod": "9f28b3e1d3afac4e724b292e1867f1a661",  # 模数（十六进制）
            "t": 200000,  # 目标迭代次数
            "puzzle": "woVmIfMmB3qI6a7ywfvS+/7oyCpQ0cGCf+o2wYqut+gwJZ88WxHOoCJe4LEoAlDCPkoIpc8cgTRB\r\nQer8QtYcLcgKO3YmOFcnzOOGzO85aYufcYBPaVSKhDlzgRBF+f5AT6rI2Fslr1usTkuQXwZaRm1M\r\nt/NGOacu/nb4AdkgDYgyCw9tEwowbpVmk0WsoVQ2uWkNvjZDWZ9NTG1NrTg/S6CVMscGivjJIsP5\r\nwmsVGyXpwMC23vK+TX20Kjc4q+9PRjBFDK48NiXT+w/0kLexJw==",
            # 挑战谜题（Base64）
            "x": "d6150539c3"  # 初始值（十六进制）
        }
    }

    print("开始VDF计算...")
    print("输入参数:")
    print(json.dumps(input_data, indent=2, ensure_ascii=False))
    print("\n" + "=" * 50 + "\n")

    try:
        # 执行同步计算
        result = vdf_function_calculate(input_data, calc_type="sync")

        print("计算完成！")
        print("输出结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # 解析结果参数
        args_dict = json.loads(result["args"])
        print("\n解析后的args参数:")
        print(f"  最终x值: {args_dict['x']}")
        print(f"  实际迭代次数: {args_dict['t']}")
        print(f"  签名: {args_dict['sign']}")

        # 性能统计
        print("\n性能统计:")
        print(f"  目标迭代次数: {input_data['args']['t']}")
        print(f"  实际迭代次数: {result['runTimes']}")
        print(f"  完成比例: {result['runTimes'] / input_data['args']['t'] * 100:.2f}%")
        print(f"  计算时间: {result['spendTime']}ms")
        print(f"  迭代速度: {result['runTimes'] / result['spendTime']:.0f} 次/ms")
    except ValueError as e:
        print(f"参数错误: {e}")
    except TypeError as e:
        print(f"类型错误: {e}")
    except Exception as e:
        print(f"计算过程中发生错误: {e}")


def async_callback(result: Dict[str, Any]):
    """
    异步计算回调函数示例

    Args:
        result: VDF计算结果
    """
    print("\n异步计算完成！")
    print("计算结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def example_async_usage():
    """
    异步模式使用示例
    """
    print("开始异步VDF计算...")

    input_data = {
        "needCheck": True,
        "sid": "async-test-001",
        "hashFunc": "VDF_FUNCTION",
        "maxTime": 500,  # 较短的超时时间用于演示
        "minTime": 100,
        "args": {
            "mod": "9f28b3e1d3afac4e724b292e1867f1a661",
            "t": 10000,
            "puzzle": "test-puzzle",
            "x": "d6150539c3"
        }
    }

    # 启动异步计算
    vdf_function_calculate(input_data, calc_type="async", callback=async_callback)

    print("异步计算已启动，主线程继续执行其他任务...")
    print("等待计算结果...")


if __name__ == "__main__":
    # 运行同步示例
    example_usage()

    print("\n" + "=" * 50 + "\n")

    # 运行异步示例
    example_async_usage()

    # 等待异步计算完成
    time.sleep(0.6)  # 等待足够时间让异步计算完成