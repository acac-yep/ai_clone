from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# 初始化Flask应用
app = Flask(__name__)

# 配置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', 'conversation.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 导入并注册蓝图
from app.routes.main import main as main_blueprint
app.register_blueprint(main_blueprint)

# 确保instance目录存在
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance'), exist_ok=True)

# 导出必要的对象
__all__ = ['app', 'db']