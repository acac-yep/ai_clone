# 导入已初始化的应用
from app import app

if __name__ == '__main__':
    # 确保数据库文件存在
    with app.app_context():
        db.create_all()
    app.run(debug=True)