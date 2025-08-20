from app import db
from datetime import datetime

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_input = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.PickleType)
    importance_score = db.Column(db.Float, default=0.5)

    def __repr__(self):
        return f'<Conversation {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'user_input': self.user_input,
            'ai_response': self.ai_response,
            'keywords': self.keywords,
            'importance_score': self.importance_score
        }