from flask import Blueprint, render_template, request, jsonify
from app.models.conversation_model import Conversation
from app import db
from app.utils.ai_processor import process_ai_request
from app.utils.memory_manager import retrieve_relevant_history

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # 检索相关历史对话
    history = retrieve_relevant_history(user_input)

    # 处理AI请求
    ai_response, keywords, importance_score = process_ai_request(user_input, history)

    # 存储新对话
    new_conversation = Conversation(
        user_input=user_input,
        ai_response=ai_response,
        keywords=keywords,
        importance_score=importance_score
    )
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({
        'response': ai_response,
        'conversation_id': new_conversation.id
    })

@main.route('/api/history', methods=['GET'])
def get_history():
    conversations = Conversation.query.order_by(Conversation.timestamp.desc()).limit(20).all()
    return jsonify([conv.to_dict() for conv in conversations])