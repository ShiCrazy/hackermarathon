import os
import json
import time
from dotenv import load_dotenv
from typing import Dict, Optional
import pandas as pd


def extract_calculation_logics(response: str) -> Optional[Dict]:
    """
    从AI响应中提取因子计算逻辑
    
    Args:
        response: AI的响应文本
        
    Returns:
        包含因子名称、逻辑和表达式的字典
    """
    try:
        # 尝试直接解析JSON
        factor = json.loads(response)
        
        # 验证必要字段
        required_fields = ['因子名称', '因子逻辑', '因子表达式']
        if all(field in factor for field in required_fields):
            print(f"成功提取因子: {factor['因子名称']}")
            return factor
        else:
            print(f"响应缺少必要字段")
            return None
            
    except json.JSONDecodeError:
        # 如果直接解析失败，尝试提取JSON部分
        try:
            # 查找JSON开始和结束位置
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                factor = json.loads(json_str)
                
                # 验证必要字段
                required_fields = ['因子名称', '因子逻辑', '因子表达式']
                if all(field in factor for field in required_fields):
                    print(f"成功从响应中提取因子: {factor['因子名称']}")
                    return factor
                    
        except Exception as e:
            print(f"提取因子信息失败: {e}")
            
    return None

# 计算指标只有RankIC均值和ICIR够不够？
# 这些回测指标的计算方式（代码形式和计算表达式形式）
def calculate_metrics(factor_expression: str, mode: str = "developer") -> Dict:
    """
    计算因子的回测指标
    
    Args:
        factor_expression: 因子表达式
        backtest_params: 回测参数配置
        
    Returns:
        包含各项回测指标的字典：
        - RankIC均值: Rank相关系数的均值
        - ICIR: 信息系数比率，用来衡量股票因子的稳定性和预测能力，其是信息系数（IC）的均值与IC标准化的比值（ICIR = Mean(IC)/Std(IC)）

    """
    
    # 载入数据，写清楚数据的地址
    data_path = "./data/..."
    data = pd.read

    # 默认回测参数
    default_params = {
        "回测区间": "2024.09.01-2025.09.01",
        "样本空间": "剔除上市不满365个自然日的新股，剔除ST股",
        "中性化处理": "对因子进行市值行业中性化",
        "测试方式": "周频调仓，以下周第一个交易日的VWAP价格成交，计算VWAP收益率的RankIC均值与ICIR。",
        "方向调整": "根据RankIC均值的正负，对因子方向进行调整，使得RankIC为正，便于比较"
    }
    

    
    print(f"开始计算回测指标...")
    print(f"因子表达式: {factor_expression}")
    print(f"回测参数: {default_params}")
    
    # ========================================
    # TODO: 在这里接入实际的回调函数，生成回调函数的方式有两种，一种是我们自己写，另一种是调用大模型API来写，然后在本地将代码用exec()执行
    # ① 自己提前写好，这样的坏处是整个流程不能串起来，要割裂开来，好处是比较容易控制
    if mode == "developer":
        true_metrics = callback_by_developer(factor_expression, data)
    elif mode == "deepseek":
    # ② 调用大模型API来写，这样的好处是整个流程可以串起来，坏处是不可控性
        true_metrics = callback_by_deepseek(factor_expression, data)
    else:
        raise ValueError("请选择回测框架的模式：'developer' 或 'deepseek'")
    # ========================================



    # # 以下是模拟的回测结果
    # mock_metrics = {
    #     "RankIC均值": 0.038,
    #     "ICIR": 1.75
    # }
    
    # print(f"回测计算完成!")
    # print(f"  RankIC: {mock_metrics['RankIC均值']:.3f}")
    # print(f"  ICIR: {mock_metrics['ICIR']:.2f}")
    
    # return mock_metrics


    # 以下是真实的回测结果
    print(f" RankIC: {true_metrics['RankIC均值']:.3f}")
    print(f"  ICIR: {true_metrics['ICIR']:.2f}")



def callback_by_developer(factor_expression: str, data: Dict) -> Dict:
    """
    使用开发者模式计算回测指标

    Args:
        factor_expression: 因子表达式
        data: 数据字典

    Returns:
        包含各项回测指标的字典
    """
    # TODO: 在这里实现开发者模式下的回测指标计算
    return {}

def callback_by_deepseek(factor_expression: str, data: Dict) -> Dict:
    """
    使用大模型API模式计算回测指标

    Args:
        factor_expression: 因子表达式
        data: 数据字典

    Returns:
        包含各项回测指标的字典
    """
    # TODO: 在这里实现大模型API模式下的回测指标计算
    return {}

