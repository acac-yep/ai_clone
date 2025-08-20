from app import app, db
from app.models.conversation_model import Conversation

# 在应用上下文中创建数据库表
with app.app_context():
    db.create_all()
    print("数据库表已创建成功！")