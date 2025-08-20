from app.models.conversation_model import Conversation
from app import db
import numpy as np

def retrieve_relevant_history(user_input, max_history=3):
    """
    检索与当前用户输入相关的历史对话
    
    参数:
    user_input (str): 用户输入的文本
    max_history (int): 最大返回历史对话数量
    
    返回:
    list: 相关历史对话列表
    """
    # 获取最近的对话
    recent_conversations = Conversation.query.order_by(Conversation.timestamp.desc()).limit(20).all()
    
    if not recent_conversations:
        return []
    
    # 简单的相关性匹配 (实际应用中可以使用更复杂的算法)
    relevant_scores = []
    for conv in recent_conversations:
        score = calculate_relevance(user_input, conv.user_input, conv.ai_response)
        relevant_scores.append((score, conv))
    
    # 按相关性排序并返回前max_history个
    relevant_scores.sort(reverse=True, key=lambda x: x[0])
    relevant_conversations = [conv.to_dict() for _, conv in relevant_scores[:max_history]]
    
    return relevant_conversations

def calculate_relevance(user_input, history_input, history_response):
    """
    计算当前输入与历史对话的相关性
    
    参数:
    user_input (str): 当前用户输入
    history_input (str): 历史用户输入
    history_response (str): 历史AI回复
    
    返回:
    float: 相关性分数
    """
    # 简单实现：基于关键词匹配
    user_tokens = set(user_input.lower().split())
    history_tokens = set(history_input.lower().split()) | set(history_response.lower().split())
    
    if not user_tokens or not history_tokens:
        return 0.0
    
    # 计算交集大小
    intersection = user_tokens & history_tokens
    
    # 相关性分数 = 交集大小 / 用户输入关键词数量
    return len(intersection) / len(user_tokens)

def cleanup_low_importance_conversations(threshold=0.3, max_keep=100):
    """
    清理低重要性的对话记录
    
    参数:
    threshold (float): 重要性阈值
    max_keep (int): 保留的最大对话数量
    """
    # 1. 删除低于阈值的对话
    low_importance = Conversation.query.filter(Conversation.importance_score < threshold).all()
    for conv in low_importance:
        db.session.delete(conv)
    
    # 2. 如果对话数量仍超过max_keep，删除最早的对话
    total_conversations = Conversation.query.count()
    if total_conversations > max_keep:
        excess = total_conversations - max_keep
        oldest_conversations = Conversation.query.order_by(Conversation.timestamp).limit(excess).all()
        for conv in oldest_conversations:
            db.session.delete(conv)
    
    db.session.commit()
    return True