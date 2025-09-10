import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional


class DeepSeekClient:
    """DeepSeek API 客户端封装类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 DeepSeek 客户端
        
        Args:
            api_key: API密钥，如果不提供则从环境变量读取
        """
        # 加载.env文件
        load_dotenv()
        
        # 获取API密钥
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("未找到 DEEPSEEK_API_KEY，请在.env文件中设置或作为参数传入")
        
        # 初始化客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        
        # 存储对话历史
        self.messages: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """
        添加消息到对话历史
        
        Args:
            role: 角色类型 ("system", "user", "assistant")
            content: 消息内容
        """
        self.messages.append({"role": role, "content": content})
    
    def chat(self, user_prompt: str, system_prompt: Optional[str] = None, 
             model: str = "deepseek-reasoner", append_to_history: bool = True) -> str:
        """
        发送聊天请求
        
        Args:
            user_prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            model: 模型名称
            append_to_history: 是否将响应添加到对话历史
            
        Returns:
            模型响应内容
        """
        # 如果提供了系统提示词且对话历史为空，添加系统消息
        if system_prompt and not self.messages:
            self.add_message("system", system_prompt)
        
        # 添加用户消息
        self.add_message("user", user_prompt)
        
        # 调用API
        response = self.client.chat.completions.create(
            model=model,
            messages=self.messages
        )
        
        # 获取响应
        assistant_message = response.choices[0].message
        
        # 如果需要，添加到对话历史
        if append_to_history:
            self.messages.append({
                "role": assistant_message.role,
                "content": assistant_message.content
            })
        
        return assistant_message.content
    
    def reset_conversation(self):
        """重置对话历史"""
        self.messages = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取完整对话历史"""
        return self.messages.copy()


def simple_chat(system_prompt: str, user_prompt: str, 
                api_key: Optional[str] = None, model: str = "deepseek-reasoner") -> Dict:
    """
    简单的单轮对话函数
    
    Args:
        system_prompt: 系统提示词
        user_prompt: 用户提示词
        api_key: API密钥（可选）
        model: 模型名称
        
    Returns:
        包含响应内容和对话历史的字典
    """
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("未找到 DEEPSEEK_API_KEY")
    
    # 初始化客户端
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # 构建消息
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # 调用API
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    # 添加响应到消息历史
    messages.append({
        "role": response.choices[0].message.role,
        "content": response.choices[0].message.content
    })
    
    return {
        "response": response.choices[0].message.content,
        "messages": messages,
        "full_response": response
    }


def multi_round_chat(system_prompt: str, user_prompts: List[str], 
                     api_key: Optional[str] = None, model: str = "deepseek-reasoner") -> List[Dict]:
    """
    多轮对话函数
    
    Args:
        system_prompt: 系统提示词
        user_prompts: 用户提示词列表
        api_key: API密钥（可选）
        model: 模型名称
        
    Returns:
        每轮对话的响应列表
    """
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("未找到 DEEPSEEK_API_KEY")
    
    # 初始化客户端
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # 初始化消息历史
    messages = [{"role": "system", "content": system_prompt}]
    
    # 存储所有轮次的响应
    all_responses = []
    
    # 逐轮对话
    for i, user_prompt in enumerate(user_prompts, 1):
        # 添加用户消息
        messages.append({"role": "user", "content": user_prompt})
        
        # 调用API
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        # 添加助手响应到消息历史
        assistant_message = response.choices[0].message
        messages.append({
            "role": assistant_message.role,
            "content": assistant_message.content
        })
        
        # 存储本轮结果
        round_result = {
            "round": i,
            "user_prompt": user_prompt,
            "response": assistant_message.content,
            "messages_snapshot": messages.copy()
        }
        all_responses.append(round_result)
        
        print(f"Round {i}: 完成")
    
    return all_responses



# 使用示例
if __name__ == "__main__":
    # 示例1：使用简单函数
    SYSTEMPROMPT = "你是一个有帮助的助手"
    USERPROMPT_1 = "你好，请介绍一下你自己"
    
    result = simple_chat(SYSTEMPROMPT, USERPROMPT_1)
    print(f"响应: {result['response']}")
    print(f"完整对话历史: {result['messages']}")
    
    # 示例2：使用类进行多轮对话
    client = DeepSeekClient()
    client.chat("你好", system_prompt="你是一个友好的助手")
    response = client.chat("今天天气怎么样？")
    print(f"第二轮响应: {response}")
    
    # 示例3：批量多轮对话
    prompts = ["你好", "1+1等于几？", "再见"]
    results = multi_round_chat("你是一个数学助手", prompts)
    for r in results:
        print(f"第{r['round']}轮: {r['response'][:50]}...")