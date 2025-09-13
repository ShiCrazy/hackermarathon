
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


# Part1.初始化  由开发者定义实验元规则，包括设定大模型的system_prompt、提供可用的算子处理列表和财务数据，还要输入一组经过验证的“样例因子”及其历史表现作为大模型的初始prompt
# TODO: ① 要提供什么样的算子处理列表和财务数据，以什么样的形式提供？需不需要提供算子表达式？   answer: 不需要算子表达式
# ② 样例因子取哪个？
# ③ 样例因子的历史表现该怎么计算获得？

# 算子相关代码
process_code_prompt = """
算子名称,释义
get,取财务或市值数据
quarter,将财务数据累计值转为单季度值
ttm,将财务数据累计值转为TTM值
diff,当期财务数据减去上个季度财务数据
yoy,计算财务数据同比
qoq,计算财务数据环比
refq,财务数据前移N个季度
op,对多个财务数据进行运算
op2,用于财务数据与市值数据之间的运算
"""



# 基本面因子可用数据
# TODO:介绍基本面因子可用数据如何用
# Answer: 调查一下如何用API传文件

available_data = """


"""

# 现有基本面样例因子表达式
# TODO：① 是否需要其他的评价指标 Answer: 只需要RankIC均值和ICIR
# ② 需要准备RankIC均值和ICIR的计算表达式和计算程序脚本 Answer：网上搜对应的计算表达式
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


output_file = "../data/generated_factor.json"

# Part2.大模型生成。在接收到上述prompt之后，大模型生成一个新的因子，并以JSON格式输出该新因子的名称、逻辑释义及表达式
# TODO: ① 需要函数将result中的结果落到文件中 Answer：shigb做

result = simple_chat(formatted_prompt, USERPROMPT_GENERAL)

# Part3.验证与评估。开发人员提取大模型生成的因子表达式，利用定义好的标准化回测框架，对新因子的历史选股效果（如RankIC均值、ICIR等）进行评估
# TODO：① 标准化的回测框架脚本代码的编写
calculation_logics = extract_calculation_logics(result['response'])

if calculation_logics:
    print("\n提取的因子信息:")
    print(json.dumps(calculation_logics, ensure_ascii=False, indent=2))
    
    # 提取因子表达式，计算回测指标
    metrics_dict = calculate_metrics(
        factor_expression=calculation_logics['因子表达式']
    )
    
    # 合并结果
    calculation_logics.update(metrics_dict)
    
    # 保存结果

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(calculation_logics, f, ensure_ascii=False, indent=2)
    
    print(f"\n因子已保存到: {output_file}")

else:
    print("因子生成失败")


# Part4. 反馈与迭代
