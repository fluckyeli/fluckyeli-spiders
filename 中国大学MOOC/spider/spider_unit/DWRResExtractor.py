from py_mini_racer import py_mini_racer
import json


def extract_dwr_objects(dwr_js_code: str) -> dict:
    """
    执行 DWR JavaScript 响应代码，提取其中定义的对象，并返回 Python dict
    """
    ctx = py_mini_racer.MiniRacer()

    # JS 沙箱 + DWR hook
    bootstrap_js = """
    var __DWR_CAPTURE__ = {
        result: null
    };

    var dwr = {
        engine: {
            _remoteHandleCallback: function(batchId, callId, data) {
                __DWR_CAPTURE__.result = data;
            }
        }
    };

    function __collectAllObjects__() {
        var out = {};
        for (var k in this) {
            try {
                if (this[k] && typeof this[k] === 'object') {
                    out[k] = this[k];
                }
            } catch (e) {}
        }
        return out;
    }
    """

    ctx.eval(bootstrap_js)

    # 执行原始 DWR JS
    ctx.eval(dwr_js_code)

    # 优先取标准 DWR 回调数据
    result = ctx.eval("""
        (function() {
            if (__DWR_CAPTURE__.result !== null) {
                return JSON.stringify(__DWR_CAPTURE__.result);
            }
            return JSON.stringify(__collectAllObjects__());
        })();
    """)

    return json.loads(result)


if __name__ == '__main__':
    dwr_js = """
    var s0={};
    s0.id=123;
    s0.name="Alice";
    var s1={};
    s1.age=18;
    s0.profile=s1;
    """

    data = extract_dwr_objects(dwr_js)
    print(json.dumps(data, ensure_ascii=False))
