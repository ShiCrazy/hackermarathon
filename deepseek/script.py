
from DeepSeekClient import *
from calculationFunctions import *
from openai import OpenAI
from prompt import *
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 获取API密钥
api_key = os.getenv('DEEPSEEK_API_KEY')


client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")



# 算子相关代码
process_code_prompt = """
算子名称    计算代码
get         ...
quarter     ...
ttm         ...
...
"""


# 基本面因子可用数据
available_data = """


"""

# 现有基本面因子表达式
sample_factor = """
    [
        {
            "因子名称": "",
            "因子逻辑": "",
            "因子表达式": "",
            "RankIC均值": ,
            "ICIR": 
        }
    ]
"""



formatted_prompt = SYSTEMPROMPT.format(
        process_code_prompt=process_code_prompt,
        available_data=available_data,
        sample_factor=sample_factor
    )


result = simple_chat(formatted_prompt, USERPROMPT_START)

calculation_logics = extract_calculation_logics(result['response'])

if calculation_logics:
    print("\n提取的因子信息:")
    print(json.dumps(calculation_logics, ensure_ascii=False, indent=2))
    
    # 计算回测指标
    metrics_dict = calculate_metrics(
        factor_expression=calculation_logics['因子表达式']
    )
    
    # 合并结果
    calculation_logics.update(metrics_dict)
    
    # 保存结果
    output_file = "generated_factor_test.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(calculation_logics, f, ensure_ascii=False, indent=2)
    
    print(f"\n因子已保存到: {output_file}")

else:
    print("因子生成失败")

