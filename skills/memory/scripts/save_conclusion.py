#!/usr/bin/env python3
"""
保存分析结论

功能：保存股票分析结论和投资建议
用法：python save_conclusion.py --code "HK.00700" --analysis "技术面看涨" --recommendation "买入" --confidence 0.8
"""

import argparse
import json
import sys
from config import (
    CONCLUSIONS_FILE,
    load_json_file,
    save_json_file,
    generate_id,
    get_current_datetime,
)


def save_conclusion(
    code,
    analysis,
    recommendation,
    confidence=None,
    target_price=None,
    stop_loss=None,
    output_json=False,
):
    """
    保存分析结论

    Args:
        code: 股票代码
        analysis: 分析内容
        recommendation: 投资建议（买入/持有/卖出）
        confidence: 置信度（0-1）
        target_price: 目标价格（可选）
        stop_loss: 止损价格（可选）
        output_json: 是否输出JSON格式

    Returns:
        保存的结论记录
    """
    # 验证recommendation
    valid_recommendations = ["买入", "持有", "卖出", "BUY", "HOLD", "SELL"]
    if recommendation.upper() not in [r.upper() for r in valid_recommendations]:
        print(
            f"错误: 无效的投资建议 '{recommendation}'，有效值: {', '.join(valid_recommendations)}"
        )
        sys.exit(1)

    # 标准化recommendation
    rec_map = {"BUY": "买入", "HOLD": "持有", "SELL": "卖出"}
    recommendation = rec_map.get(recommendation.upper(), recommendation)

    # 创建结论记录
    conclusion = {
        "id": generate_id(),
        "timestamp": get_current_datetime(),
        "code": code,
        "analysis": analysis,
        "recommendation": recommendation,
        "confidence": confidence,
        "target_price": target_price,
        "stop_loss": stop_loss,
    }

    # 加载现有结论
    conclusions = load_json_file(CONCLUSIONS_FILE, default=[])

    # 添加新结论
    conclusions.append(conclusion)

    # 保存结论
    save_json_file(CONCLUSIONS_FILE, conclusions)

    # 输出结果
    if output_json:
        print(json.dumps(conclusion, ensure_ascii=False, indent=2))
    else:
        print(f"分析结论已保存")
        print(f"  ID: {conclusion['id']}")
        print(f"  时间: {conclusion['timestamp']}")
        print(f"  代码: {conclusion['code']}")
        print(f"  建议: {conclusion['recommendation']}")
        if conclusion["confidence"]:
            print(f"  置信度: {conclusion['confidence'] * 100:.1f}%")
        if conclusion["target_price"]:
            print(f"  目标价: {conclusion['target_price']}")
        if conclusion["stop_loss"]:
            print(f"  止损价: {conclusion['stop_loss']}")

    return conclusion


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="保存分析结论")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--analysis", required=True, help="分析内容")
    parser.add_argument(
        "--recommendation", required=True, help="投资建议（买入/持有/卖出）"
    )
    parser.add_argument("--confidence", type=float, help="置信度（0-1）")
    parser.add_argument("--target-price", type=float, help="目标价格")
    parser.add_argument("--stop-loss", type=float, help="止损价格")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )

    args = parser.parse_args()

    save_conclusion(
        code=args.code,
        analysis=args.analysis,
        recommendation=args.recommendation,
        confidence=args.confidence,
        target_price=args.target_price,
        stop_loss=args.stop_loss,
        output_json=args.output_json,
    )
