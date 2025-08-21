import re
import os
import requests

# 初始化DeepSeek客户端配置
# 使用requests库直接调用DeepSeek API
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# 配置请求头
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
} if DEEPSEEK_API_KEY else {}

# 移除可能存在的proxies配置
# 如果需要使用代理，请在requests请求中单独配置

def process_ai_request(user_input, history):
    """
    处理用户输入并生成AI回复
    
    参数:
    user_input (str): 用户输入的文本
    history (list): 相关历史对话列表
    
    返回:
    tuple: (ai_response, keywords, importance_score)
    """
    # 构建提示信息
    prompt = build_prompt(user_input, history)

    # 调用AI模型
    ai_response = call_ai_model(prompt)

    # 提取关键词
    keywords = extract_keywords(ai_response)

    # 计算重要性评分
    importance_score = calculate_importance(user_input, ai_response)

    return ai_response, keywords, importance_score

def build_prompt(user_input, history):
    """构建发送给AI模型的提示信息"""
    prompt = "你是一个个性化AI助手，需要根据用户的对话风格和历史交流来生成回复。\n"
    
    if history:
        prompt += "以下是相关的历史对话：\n"
        for conv in history:
            prompt += f"用户: {conv['user_input']}\n"
            prompt += f"助手: {conv['ai_response']}\n"
    
    prompt += f"用户: {user_input}\n"
    prompt += "助手: "
    
    return prompt

def call_ai_model(prompt):
    """调用DeepSeek AI模型生成回复"""
    try:
        if not DEEPSEEK_API_KEY:
            raise ValueError("DeepSeek API key is not set")

        # 构建请求体
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个个性化AI助手，需要根据用户的对话风格和历史交流来生成回复。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        # 发送请求
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload
        )

        # 检查响应状态
        response.raise_for_status()

        # 提取回复内容
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling DeepSeek API: {e}")
        return "抱歉，当前AI服务不可用。请稍后再试。"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "抱歉，处理请求时发生错误。请稍后再试。"


def extract_keywords(text):
    """从文本中提取关键词"""
    # 简单实现，实际应用中可以使用更复杂的NLP方法
    keywords = re.findall(r'\b\w{4,}\b', text)
    return list(set(keywords))[:5]  # 取前5个独特的关键词

def calculate_importance(user_input, ai_response):
    """计算对话的重要性评分"""
    # 简单实现，实际应用中可以基于更复杂的逻辑
    # 例如关键词匹配、情感分析等
    return 0.5  # 默认中等重要性