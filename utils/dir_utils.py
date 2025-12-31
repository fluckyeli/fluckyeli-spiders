import os


def get_project_root():
    """自动查找项目根目录（查找包含 .git、requirements.txt、setup.py 等标志的目录）"""
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # 定义项目根目录的标志文件
    markers = ['.git','.gitignore']

    while current_dir != os.path.dirname(current_dir):  # 到达根目录时停止
        for marker in markers:
            if os.path.exists(os.path.join(current_dir, marker)):
                return current_dir
        # 向上级目录查找
        current_dir = os.path.dirname(current_dir)

    return current_dir

if __name__ == '__main__':
    project_root = get_project_root()
    print(f"项目根目录: {project_root}")