import os
import subprocess
import sys

from dir_utils import get_project_root


def run_n_m3u8dl_cli(url, work_dir=None, save_name=None, exe_path=None, save_temp=False, **kwargs):
    """
    封装调用 N_m3u8DL-CLI 并实时回显进度。

    Args:
        exe_path (str): N_m3u8DL-CLI_v3.0.2.exe 的文件路径
        url (str): m3u8 的链接地址
        work_dir (str, optional): 下载保存目录 (--workDir)
        save_name (str, optional): 保存的文件名 (--saveName)
        **kwargs: 其他可选参数，例如 enableDelAfterDone=True 会被转换为 --enableDelAfterDone
    """

    # 1. 检查 EXE
    if exe_path is None:
        # 尝试在当前目录和常见位置查找
        possible_paths = [
            "./N_m3u8DL-CLI_v3.0.2.exe",
            "./bin/N_m3u8DL-CLI_v3.0.2.exe",
            os.path.join(get_project_root(),
                         "bin/N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG/N_m3u8DL-CLI_v3.0.2.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                exe_path = path
                break
        else:
            raise FileNotFoundError("未找到 N_m3u8DL-CLI_v3.0.2.exe，请指定路径")

    # 2. 构建命令列表
    cmd = [exe_path, url]

    if work_dir:
        cmd.extend(['--workDir', work_dir])
    if save_name:
        cmd.extend(['--saveName', save_name])
    if not save_temp:
        cmd.extend(['--enableDelAfterDone'])

    # 处理其他关键字参数 (将 camelCase 转换为 CLI 参数格式)
    for key, value in kwargs.items():
        # 假设参数是布尔值且为真 (如 enableDelAfterDone=True -> --enableDelAfterDone)
        if isinstance(value, bool):
            if value:
                cmd.append(f'--{key}')
        # 假设参数是有值的 (如 headers="xxx" -> --headers "xxx")
        elif value:
            cmd.extend([f'--{key}', str(value)])

    print(f"正在执行指令: {' '.join(cmd)}")
    print("-" * 50)

    # 3. 使用 Popen 执行并捕获输出
    # bufsize=1 表示行缓冲，universal_newlines=True 表示以文本模式处理
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # 将错误输出合并到标准输出
            text=True,  # Python 3.7+ 使用 text=True 代替 universal_newlines
            bufsize=1,
            encoding='gbk',  # 该工具通常输出 utf-8，如果在 Windows 中文乱码可尝试 'gbk'
            errors='replace'  # 防止特殊字符导致解码报错
        )

        # 4. 实时读取输出并刷新
        while True:
            # 逐字符或逐行读取
            # 这里使用 readline 可以读取包含 \r 的行
            output = process.stdout.readline()

            if output == '' and process.poll() is not None:
                break

            if output.strip():
                # 关键：使用 sys.stdout.write 而不是 print
                # print 会强制加换行，破坏进度条的 \r (回车回退) 效果
                sys.stdout.write(output)
                sys.stdout.flush()  # 强制刷新缓冲区，立即显示

        # 等待子进程完全结束
        return_code = process.poll()

        if return_code == 0:
            print("\n" + "-" * 50)
            print("下载任务完成！")
            return True
        else:
            print(f"\n任务异常结束，返回码: {return_code}")
            return False

    except Exception as e:
        print(f"\n发生异常: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    url = "https://mooc2vod.stu.126.net/nos/hls/2021/04/21/66/a5d23137-b835-421b-a29f-95d458a02dea_7.m3u8?ak=7909bff134372bffca53cdc2c17adc27a4c38c6336120510aea1ae1790819de87a279161971f6b3852adf50befe8ff8bf87bfeed1987848567632deb007c84023059f726dc7bb86b92adbc3d5b34b13275e062c3bc16aaf7676ff72202681e38b8ae77e29788836745b7125f174b3914"
    run_n_m3u8dl_cli(url, work_dir="./download")
