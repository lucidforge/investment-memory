#!/usr/bin/env python3
"""
根据风险等级计算建议仓位
"""

import argparse
import json


def calculate_kelly_position(win_rate, risk_reward):
    """计算凯利公式仓位"""
    if risk_reward <= 0:
        return 0

    # 凯利公式: f* = (p * b - q) / b
    # p = 胜率, b = 赔率, q = 败率
    loss_rate = 1 - win_rate
    kelly = (win_rate * risk_reward - loss_rate) / risk_reward

    # 限制在0-50%之间（保守使用半凯利）
    kelly = max(0, min(kelly, 0.5))

    return kelly


def get_risk_adjusted_position(risk_level, kelly_position=None):
    """根据风险等级调整仓位"""
    # 风险等级对应的建议仓位上限
    risk_limits = {
        "very_high": 0.05,  # 5%
        "high": 0.10,  # 10%
        "medium": 0.20,  # 20%
        "low": 0.30,  # 30%
    }

    max_position = risk_limits.get(risk_level, 0.15)

    if kelly_position:
        # 取凯利公式和风险限制的较小值
        return min(kelly_position, max_position)

    return max_position


def calculate_position_sizing(
    risk_level, win_rate=None, risk_reward=None, total_capital=None, output_json=False
):
    """计算仓位"""
    result = {
        "risk_level": risk_level,
        "win_rate": win_rate,
        "risk_reward": risk_reward,
        "total_capital": total_capital,
    }

    # 风险等级中文名
    risk_names = {
        "very_high": "极高风险",
        "high": "高风险",
        "medium": "中等风险",
        "low": "低风险",
    }
    result["risk_level_name"] = risk_names.get(risk_level, "未知")

    # 凯利公式计算
    kelly_position = None
    if win_rate and risk_reward:
        kelly_position = calculate_kelly_position(win_rate, risk_reward)
        result["kelly_position"] = kelly_position

    # 风险调整后仓位
    adjusted_position = get_risk_adjusted_position(risk_level, kelly_position)
    result["suggested_position"] = adjusted_position

    # 计算具体金额
    if total_capital:
        suggested_amount = total_capital * adjusted_position
        result["suggested_amount"] = suggested_amount

    # 分散化建议
    diversification = {
        "single_stock_max": 0.20,  # 单只股票最大20%
        "single_industry_max": 0.30,  # 单个行业最大30%
        "cash_reserve": 0.10,  # 保持10%现金
    }
    result["diversification"] = diversification

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"仓位计算")
        print("=" * 50)
        print(f"\n风险等级: {result['risk_level_name']}")

        if kelly_position:
            print(f"\n凯利公式计算:")
            print(f"  胜率: {win_rate * 100:.0f}%")
            print(f"  赔率: {risk_reward:.1f}")
            print(f"  凯利仓位: {kelly_position * 100:.1f}%")

        print(f"\n建议仓位:")
        print(f"  建议仓位比例: {adjusted_position * 100:.1f}%")
        if total_capital:
            print(f"  建议投资金额: {suggested_amount:,.0f}元")

        print(f"\n分散化原则:")
        print(f"  单只股票最大仓位: {diversification['single_stock_max'] * 100:.0f}%")
        print(
            f"  单个行业最大仓位: {diversification['single_industry_max'] * 100:.0f}%"
        )
        print(f"  建议保留现金: {diversification['cash_reserve'] * 100:.0f}%")

        print("\n" + "=" * 50)

    return result


def main():
    parser = argparse.ArgumentParser(description="计算建议仓位")
    parser.add_argument(
        "--risk-level",
        choices=["very_high", "high", "medium", "low"],
        required=True,
        help="风险等级",
    )
    parser.add_argument("--win-rate", type=float, help="预期胜率（0-1）")
    parser.add_argument("--risk-reward", type=float, help="风险回报比")
    parser.add_argument("--total-capital", type=float, help="总资金")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = calculate_position_sizing(
        risk_level=args.risk_level,
        win_rate=args.win_rate,
        risk_reward=args.risk_reward,
        total_capital=args.total_capital,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
