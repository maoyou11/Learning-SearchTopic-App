# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : ai_deepseek.py
# Github : https://github.com/SJYssr
# 用途：封装DeepseekAI的HTTP API调用，负责AI问答请求与异常处理。

import requests


def call_deepseek_api(deepseek_api_key, prompt, deepseek_model):
    """
    调用DeepseekAI的API进行问答。
    :param deepseek_api_key: Deepseek API密钥
    :param prompt: 用户输入内容
    :param deepseek_model: 使用的模型名称
    :return: AI回复内容或异常信息
    """
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    # 构建标准化prompt内容
    char_prompt = f"""请严格按照以下规则回答题目：
    1. 题型适配：
       - 单选题：返回「选项字母+选项内容」（如A. 3）
       - 多选题：返回「选项字母+选项内容」，多个答案用#分隔（如A. 圆#B. 方）
       - 判断题：返回「A. 对」或「B. 错」（严格匹配选项格式）
       - 简答题：返回简洁准确的答案内容（含核心关键词）
    2. 题目信息：
       - 题目内容：{prompt}
    3. 禁止额外内容：仅返回答案，无解释、无换行、无多余字符。"""

    data = {
        "model": f"{deepseek_model}",
        "messages": [
            {"role": "system",
             "content": "你是专业的题库答案提供者，严格遵守返回格式要求，答案必须包含选项（如有）和对应内容"},
            {"role": "user", "content": char_prompt}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return e
    except KeyError as e:
        return e
    except Exception as e:
        return e 