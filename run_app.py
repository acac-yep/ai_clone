import subprocess
import sys
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

def run_command(command, description):
    """执行命令并显示描述"""
    print(f"{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"{description}成功！")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description}失败：")
        print(e.stderr)
        return False

if __name__ == '__main__':
    # 检查是否安装了依赖
    print("检查依赖是否已安装...")
    try:
        import flask
        import flask_sqlalchemy
        import openai
        import numpy
        print("依赖已安装！")
    except ImportError:
        print("依赖未安装，正在尝试安装...")
        if not run_command("pip install -r requirements.txt", "安装依赖"):
            print("安装依赖失败，请手动安装。")
            sys.exit(1)

    # 检查DeepSeek API密钥
    print("检查DeepSeek API密钥...")
    if not os.environ.get('DEEPSEEK_API_KEY'):
        print("警告：未设置DEEPSEEK_API_KEY环境变量。")
        if os.path.exists('.env'):
            print("请在项目根目录的.env文件中设置DEEPSEEK_API_KEY。")
            print("示例: DEEPSEEK_API_KEY=your_deepseek_api_key_here")
        else:
            print("请在系统环境变量中设置DEEPSEEK_API_KEY，或创建.env文件并添加密钥。")
        input("按Enter键继续...")

    # 初始化数据库
    if not run_command("python init_db.py", "初始化数据库"):
        print("初始化数据库失败，请检查配置。")
        sys.exit(1)

    # 启动应用
    print("启动应用...")
    os.system("python app.py")