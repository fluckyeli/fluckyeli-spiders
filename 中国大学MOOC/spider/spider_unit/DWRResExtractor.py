import json
import re
from py_mini_racer import MiniRacer
from typing import Dict, List, Optional


class DWRObjectExtractor:
    """DWR 多对象响应解析器（修复版）"""

    def __init__(self):
        self.ctx = MiniRacer()
        self._init_js_context()

    def _init_js_context(self):
        """初始化 JavaScript 上下文"""
        # 修复：不使用 window，使用全局作用域
        init_code = """
        // 工具函数：提取所有 s0, s1, s2 等对象
        function extractAllObjects(code) {
            // 创建一个沙盒环境来执行代码
            const sandbox = {};

            // 在沙盒中执行代码
            try {
                // 使用 Function 构造函数在沙盒中执行
                const execute = new Function('global', `
                    with(global) {
                        ${code}
                    }
                    // 返回所有 s 开头的对象
                    const result = {};
                    for (const key in global) {
                        if (key.match(/^s\\d+$/) && global[key] && typeof global[key] === 'object') {
                            result[key] = global[key];
                        }
                    }
                    return result;
                `);

                const result = execute(sandbox);
                return JSON.stringify(result);

            } catch (error) {
                // 备用方法：直接 eval
                try {
                    eval(code);
                    const result = {};
                    // 从当前作用域查找对象
                    const global = this;
                    for (const key in global) {
                        if (key.match(/^s\\d+$/) && global[key] && typeof global[key] === 'object') {
                            result[key] = global[key];
                        }
                    }
                    return JSON.stringify(result);
                } catch (e2) {
                    return "{}";
                }
            }
        }

        // 工具函数：提取特定对象（简化版）
        function extractSpecificObjects(code, objectNames) {
            // 方法1：使用全局作用域
            try {
                // 先清空可能存在的旧对象
                for (const name of objectNames) {
                    this[name] = undefined;
                }

                // 执行代码
                eval(code);

                const result = {};
                for (const name of objectNames) {
                    if (this[name] !== undefined && this[name] !== null) {
                        result[name] = this[name];
                    }
                }

                return JSON.stringify(result);

            } catch (error) {
                // 方法2：使用沙盒
                try {
                    const sandbox = {};
                    const execute = new Function('sandbox', `
                        with(sandbox) {
                            ${code}
                        }
                        const result = {};
                        ${objectNames.map(name => `
                            if (sandbox.${name} !== undefined) {
                                result.${name} = sandbox.${name};
                            }
                        `).join('')}
                        return result;
                    `);

                    const result = execute(sandbox);
                    return JSON.stringify(result);

                } catch (e2) {
                    return "{}";
                }
            }
        }
        """
        self.ctx.eval(init_code)

    def extract_all_objects(self, dwr_js_code: str) -> Dict[str, Dict]:
        """
        提取 DWR 响应中的所有 s0, s1, s2... 对象

        Args:
            dwr_js_code: DWR JavaScript 响应代码

        Returns:
            包含所有对象的字典，键为对象名（如 's0', 's1'）
        """
        try:
            # 调用 JS 工具函数
            json_str = self.ctx.call("extractAllObjects", dwr_js_code)
            return json.loads(json_str) if json_str != "{}" else {}

        except Exception as e:
            print(f"提取所有对象失败，尝试备用方法: {e}")
            # 备用方法：直接执行并手动提取
            return self._extract_with_backup_method(dwr_js_code)

    def _extract_with_backup_method(self, dwr_js_code: str) -> Dict[str, Dict]:
        """备用提取方法"""
        try:
            # 在 JS 代码末尾添加提取逻辑
            extract_code = dwr_js_code + """
            // 提取所有 s 开头的数字对象
            var result = {};
            var keys = Object.keys(this);
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                if (key.match(/^s\\d+$/) && this[key] && typeof this[key] === 'object') {
                    result[key] = this[key];
                }
            }
            JSON.stringify(result);
            """

            json_str = self.ctx.eval(extract_code)
            return json.loads(json_str) if json_str else {}

        except Exception as e:
            print(f"备用方法也失败: {e}")
            return {}

    def extract_specific_objects(self, dwr_js_code: str,
                                 object_names: List[str]) -> Dict[str, Dict]:
        """
        提取指定的 DWR 对象

        Args:
            dwr_js_code: DWR JavaScript 响应代码
            object_names: 要提取的对象名列表，如 ['s0', 's1']

        Returns:
            包含指定对象的字典
        """
        try:
            # 创建对象名字符串用于 JS
            js_object_names = json.dumps(object_names)

            # 执行提取
            js_code = f"""
            var objectNames = {js_object_names};
            var extractSpecificObjects = {self._get_extract_function()};
            extractSpecificObjects(`{self._escape_js_string(dwr_js_code)}`, objectNames);
            """

            json_str = self.ctx.eval(js_code)
            return json.loads(json_str) if json_str and json_str != "{}" else {}

        except Exception as e:
            print(f"提取指定对象失败: {e}")
            # 尝试直接方法
            return self._extract_directly(dwr_js_code, object_names)

    def _extract_directly(self, dwr_js_code: str, object_names: List[str]) -> Dict[str, Dict]:
        """直接提取方法"""
        try:
            # 为每个对象构建提取代码
            extract_code = dwr_js_code + "\n"
            extract_code += "var result = {};\n"

            for name in object_names:
                extract_code += f"""
                try {{
                    if (typeof {name} !== 'undefined' && {name} !== null) {{
                        result['{name}'] = {name};
                    }}
                }} catch (e) {{}}
                """

            extract_code += "JSON.stringify(result);"

            json_str = self.ctx.eval(extract_code)
            return json.loads(json_str) if json_str else {}

        except Exception as e:
            print(f"直接提取失败: {e}")
            return {}

    def _escape_js_string(self, s: str) -> str:
        """转义 JS 字符串中的特殊字符"""
        return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    def _get_extract_function(self) -> str:
        """获取提取函数的 JS 代码"""
        return """
        function(code, objectNames) {
            // 简单直接的提取方法
            try {
                eval(code);
                var result = {};
                for (var i = 0; i < objectNames.length; i++) {
                    var name = objectNames[i];
                    try {
                        if (eval('typeof ' + name) !== 'undefined') {
                            var obj = eval(name);
                            if (obj && typeof obj === 'object') {
                                result[name] = obj;
                            }
                        }
                    } catch (e) {
                        // 忽略单个对象错误
                    }
                }
                return JSON.stringify(result);
            } catch (error) {
                return "{}";
            }
        }
        """

    def extract_by_pattern(self, dwr_js_code: str,
                           pattern: str = r's\d+') -> Dict[str, Dict]:
        """
        使用正则表达式模式提取对象

        Args:
            dwr_js_code: DWR JavaScript 响应代码
            pattern: 正则表达式模式，默认匹配 s0, s1, s2...

        Returns:
            包含匹配对象的字典
        """
        try:
            # 使用正则表达式查找所有匹配的对象名
            matches = re.findall(pattern, dwr_js_code)
            object_names = list(set(matches))  # 去重

            if not object_names:
                return {}

            return self.extract_specific_objects(dwr_js_code, object_names)

        except Exception as e:
            print(f"按模式提取对象失败: {e}")
            return {}

    def extract_single_object(self, dwr_js_code: str,
                              object_name: str = 's0') -> Optional[Dict]:
        """
        提取单个对象

        Args:
            dwr_js_code: DWR JavaScript 响应代码
            object_name: 对象名，默认为 's0'

        Returns:
            单个对象的数据，未找到则返回 None
        """
        try:
            # 最简单直接的方法
            js_code = dwr_js_code + f"""
            try {{
                if (typeof {object_name} !== 'undefined' && {object_name} !== null) {{
                    JSON.stringify({object_name});
                }} else {{
                    "null";
                }}
            }} catch (e) {{
                "null";
            }}
            """

            json_str = self.ctx.eval(js_code)
            if json_str and json_str != "null":
                return json.loads(json_str)
            return None

        except Exception as e:
            print(f"提取单个对象失败: {e}")
            return None

    def extract_and_save(self, dwr_js_code: str,
                         output_file: str = 'dwr_objects.json',
                         pattern: str = r's\d+') -> Dict[str, Dict]:
        """
        提取对象并保存到文件

        Args:
            dwr_js_code: DWR JavaScript 响应代码
            output_file: 输出文件名
            pattern: 对象名匹配模式
        """
        try:
            # 提取对象
            objects = self.extract_by_pattern(dwr_js_code, pattern)

            # 保存到文件
            if objects:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(objects, f, ensure_ascii=False, indent=2)
                print(f"已保存 {len(objects)} 个对象到 {output_file}")
            else:
                print("未找到匹配的对象")

            return objects

        except Exception as e:
            print(f"提取并保存失败: {e}")
            return {}


# 使用示例
if __name__ == "__main__":
    # 示例 DWR 代码（包含多个对象）
    sample_dwr_code = """
    //#DWR-INSERT
    //#DWR-REPLY
    var s0 = {};
    s0.videoId = 1263014;
    s0.duration = 330;
    s0.title = "视频标题";

    var s1 = {};
    s1.userId = 1001;
    s1.userName = "张三";
    s1.age = 25;

    var s2 = {};
    s2.status = "success";
    s2.code = 200;
    s2.message = "操作成功";
    """

    # 创建解析器实例
    extractor = DWRObjectExtractor()

    print("=== 测试提取功能 ===")

    # 1. 提取单个对象（最可靠的方法）
    print("\n1. 提取单个对象 s0:")
    s0_data = extractor.extract_single_object(sample_dwr_code, 's0')
    if s0_data:
        print(json.dumps(s0_data, ensure_ascii=False, indent=2))

    # 2. 提取多个指定对象
    print("\n2. 提取指定对象 s0, s1:")
    specific_objects = extractor.extract_specific_objects(sample_dwr_code, ['s0', 's1'])
    if specific_objects:
        for name, data in specific_objects.items():
            print(f"{name}: {data}")

    # 3. 使用正则表达式提取
    print("\n3. 使用正则表达式提取所有 s 对象:")
    all_objects = extractor.extract_by_pattern(sample_dwr_code, r's\d+')
    if all_objects:
        print(f"找到对象: {list(all_objects.keys())}")
        for name, data in all_objects.items():
            print(f"{name}: {json.dumps(data, ensure_ascii=False)}")

    # 4. 提取并保存
    # print("\n4. 提取并保存到文件:")
    # saved_objects = extractor.extract_and_save(sample_dwr_code, 'test_output.json')

    # 5. 测试更复杂的情况
    print("\n5. 测试复杂 DWR 代码:")
    complex_dwr = """
    //#DWR-INSERT
    //#DWR-REPLY

    var s3 = {id: 3, name: "对象3"};
    var s4 = {value: 400, active: true};
    var not_s_object = "不应该被提取";
    """

    complex_objects = extractor.extract_all_objects(complex_dwr)
    print(f"从复杂代码中提取到: {list(complex_objects.keys())}")