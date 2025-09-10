import os
import json
import time
from dotenv import load_dotenv
from typing import Dict, Optional


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


def calculate_metrics(factor_expression: str = None, 
                     backtest_params: Dict = None) -> Dict:
    """
    计算因子的回测指标
    
    Args:
        factor_expression: 因子表达式
        backtest_params: 回测参数配置
        
    Returns:
        包含各项回测指标的字典：
        - RankIC均值: Rank相关系数的均值
        - ICIR: 信息系数比率
        - 因子方向: 1表示正向，-1表示反向
        - 年化多头超额: 多头组合相对基准的年化超额收益
        - 多头超额收益波动比: 多头超额收益的夏普比率
        - 年化多空超额: 多空组合的年化收益
        - 多空超额收益波动比: 多空收益的夏普比率
    """
    
    # 默认回测参数
    default_params = {
        'start_date': '2024-09-01',
        'end_date': '2025-09-01',
        'universe': 'A股剔除新股ST',
        'neutralization': '市值行业中性化',
        'rebalance_freq': 'weekly',
        'transaction_price': 'next_day_vwap'
    }
    
    if backtest_params:
        default_params.update(backtest_params)
    
    print(f"开始计算回测指标...")
    print(f"因子表达式: {factor_expression}")
    print(f"回测参数: {default_params}")
    
    # ========================================
    # TODO: 在这里接入实际的回测系统
    # ========================================
    
    # 模拟回测计算过程
    time.sleep(2)  # 模拟计算延迟
    
    # 以下是模拟的回测结果
    # 实际使用时需要替换为真实的回测计算
    mock_metrics = {
        "RankIC均值": 0.038,
        "ICIR": 1.75,
        "因子方向": 1,
        "年化多头超额": 0.115,
        "多头超额收益波动比": 2.03,
        "年化多空超额": 0.178,
        "多空超额收益波动比": 2.35,
        
        # 额外的统计指标（可选）
        "胜率": 0.62,
        "最大回撤": -0.085,
        "换手率": 0.45,
        "因子覆盖度": 0.92
    }
    
    print(f"回测计算完成!")
    print(f"  RankIC: {mock_metrics['RankIC均值']:.3f}")
    print(f"  ICIR: {mock_metrics['ICIR']:.2f}")
    print(f"  年化多头超额: {mock_metrics['年化多头超额']:.1%}")
    
    return mock_metrics

