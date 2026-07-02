


def call_deepseek_api(client, prompt_text, model_name="deepseek-chat"):
    """
    调用 DeepSeek API 获取结构化答题结果
    """

    # 构建标准化 prompt 内容
    # 注意：这里保持了你的原始逻辑，但在 API 调用时不需要额外的 f-string 处理
    system_instruction = "你是专业的题库答案提供者，严格遵守返回格式要求，答案必须包含选项（如有）和对应内容。"

    user_prompt = f"""请严格按照以下规则回答题目：
    1. 题型适配：
       - 单选题：返回「选项字母+选项内容」（如A. 3）
       - 多选题：返回「选项字母+选项内容」，多个答案用#分隔（如A. 圆#B. 方）
       - 判断题：返回「A. 对」或「B. 错」（严格匹配选项格式）
       - 简答题：返回简洁准确的答案内容（含核心关键词）
    2. 题目信息：
       - 题目内容：{prompt_text}
    3. 禁止额外内容：仅返回答案，无解释、无换行、无多余字符。"""

    try:
        response = client.chat.completions.create(
            model=model_name,  # 例如 "deepseek-chat" 或 "deepseek-reasoner"
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            stream=False  # 结构化答案建议关闭流式传输，便于直接获取完整字符串
        )

        # 提取回复内容
        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        print(f"API 调用出错: {e}")
        return None


# --- 使用示例 ---
if __name__ == "__main__":
    question = "1+1等于几？\nA. 1\nB. 2\nC. 3"
    from openai import OpenAI
    client = OpenAI(
        api_key="",
        base_url="https://api.deepseek.com"  # 官方标准 Base URL
    )
    result = call_deepseek_api(client, question)
    print(f"最终结果: {result}")
