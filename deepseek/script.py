
from DeepSeekClient import *
from openai import OpenAI
from prompt import *
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 获取API密钥
api_key = os.getenv('DEEPSEEK_API_KEY')


client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


process_code_prompt = "算子相关代码"
available_data = "基本面因子可用数据"
sample_factor = "现有基本面因子表达式"

result = simple_chat(SYSTEMPROMPT.format(process_code_prompt=process_code_prompt, available_data=available_data, sample_factor=sample_factor), USERPROMPT_1)

calculation_logics = extract_calculation_logics()

metrics_dict = calculate_metrics()

