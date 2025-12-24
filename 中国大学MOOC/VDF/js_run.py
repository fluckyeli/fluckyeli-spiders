from py_mini_racer import py_mini_racer


class FakeJsWorker:
    def __init__(self, js_code):
        self.ctx = py_mini_racer.MiniRacer()
        self.ctx.eval(js_code)

    def post_message(self, data):
        return self.ctx.call("__worker_entry__", data)

    def terminate(self):
        # 在浏览器里是终止线程
        # 在 Python 同步执行里，什么都不用做
        pass


def load_all_js():
    with open("vdf_concat.js", encoding="utf-8") as f:
        vdf_concat = f.read()

    worker_shell = """
    var __worker_listeners__ = [];
    var __worker_result__ = null;

    var self = this;
    var window = self;

    function postMessage(data) {
        __worker_result__ = data;
    }
    self.postMessage = postMessage;

    Object.defineProperty(self, "onmessage", {
        configurable: true,
        enumerable: true,
        set: function (fn) {
            __worker_listeners__ = [fn];
        }
    });

    self.addEventListener = function (type, fn) {
        if (type === "message") {
            __worker_listeners__.push(fn);
        }
    };
    """

    worker_tail = """
    function __worker_entry__(input) {
        __worker_result__ = null;

        if (__worker_listeners__.length === 0) {
            throw new Error("worker onmessage not initialized");
        }

        var event = { data: input };
        for (var i = 0; i < __worker_listeners__.length; i++) {
            __worker_listeners__[i](event);
        }

        return __worker_result__;
    }

    this.__worker_entry__ = __worker_entry__;
    """

    return "\n".join([
        worker_shell,
        vdf_concat,
        worker_tail
    ])


def web_worker_compute(e, callback, api_name):
    js_code = load_all_js()

    worker = FakeJsWorker(js_code)

    # 等价于 worker.postMessage(e)
    result = worker.post_message(e)

    # 等价于 onmessage → onPowerDone
    on_power_done(result, "webworker", callback, api_name)

    worker.terminate()


def on_power_done(e, t, callback, api_name):
    r = dict(e)  # 拷贝

    timeout = 1 if e.get("spendTime", 0) >= e.get("maxTime", 0) else 0

    r.pop("maxTime", None)
    r.pop("hashFunc", None)

    sp = 0 if t == "sync" else 1

    # 日志你可以先空实现
    # do_nss_log(...)
    # do_nginx_log(...)

    callback(r)


def my_callback(result):
    print("最终结果:", result)


if __name__ == '__main__':
    input_data = {
        "needCheck": True,
        "sid": "e39c41b0-46c8-432c-9eb6-12de12d5c890",
        "hashFunc": "VDF_FUNCTION",
        "maxTime": 1050,
        "minTime": 1000,
        "args": {
            "mod": "9f28b3e1d3afac4e724b292e1867f1a661",
            "t": 200000,
            "puzzle": "woVmIfMmB3qI6a7ywfvS+/7oyCpQ0cGCf+o2wYqut+gwJZ88WxHOoCJe4LEoAlDCPkoIpc8cgTRB\r\nQer8QtYcLcgKO3YmOFcnzOOGzO85aYufcYBPaVSKhDlzgRBF+f5AT6rI2Fslr1usTkuQXwZaRm1M\r\nt/NGOacu/nb4AdkgDYgyCw9tEwowbpVmk0WsoVQ2uWkNvjZDWZ9NTG1NrTg/S6CVMscGivjJIsP5\r\nwmsVGyXpwMC23vK+TX20Kjc4q+9PRjBFDK48NiXT+w/0kLexJw==",
            "x": "d6150539c3"
        }
    }

    web_worker_compute(
        e=input_data,
        callback=my_callback,
        api_name="mailzc"
    )
