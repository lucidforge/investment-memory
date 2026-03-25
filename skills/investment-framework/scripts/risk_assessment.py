#!/usr/bin/env python3
"""
评估投资机会的综合风险
"""

import argparse
import json


def assess_market_risk(industry, valuation_level=None):
    """评估市场风险"""
    score = 50  # 基础分

    # 行业周期风险（基于常见行业）
    cycle_risks = {
        "互联网": 0,
        "科技": 5,
        "消费": -5,
        "医药": -5,
        "金融": 10,
        "地产": 15,
        "能源": 15,
        "新能源": 10,
        "半导体": 10,
    }
    score += cycle_risks.get(industry, 0)

    # 估值水平调整
    if valuation_level:
        valuation_adjustments = {
            "低估": -15,
            "合理": 0,
            "偏高": 15,
            "高估": 25,
        }
        score += valuation_adjustments.get(valuation_level, 0)

    return min(max(score, 0), 100)


def assess_company_risk(market_cap, is_profitable=True, has_competitive_advantage=True):
    """评估公司风险"""
    score = 50

    # 市值风险（市值越小风险越高）
    if market_cap:
        if market_cap > 5000:  # 大于5000亿
            score -= 15
        elif market_cap > 1000:  # 1000-5000亿
            score -= 5
        elif market_cap > 100:  # 100-1000亿
            score += 5
        else:  # 小于100亿
            score += 15

    # 盈利能力
    if not is_profitable:
        score += 20

    # 竞争优势
    if not has_competitive_advantage:
        score += 15

    return min(max(score, 0), 100)


def assess_liquidity_risk(daily_volume, market_cap):
    """评估流动性风险"""
    score = 50

    if daily_volume and market_cap:
        # 日均成交额占市值比例
        turnover_rate = daily_volume / market_cap * 100 if market_cap > 0 else 0

        if turnover_rate > 1:  # 换手率>1%
            score -= 15
        elif turnover_rate > 0.5:  # 0.5-1%
            score -= 5
        elif turnover_rate > 0.1:  # 0.1-0.5%
            score += 5
        else:  # <0.1%
            score += 15

    return min(max(score, 0), 100)


def assess_policy_risk(industry):
    """评估政策风险"""
    score = 50

    # 行业政策风险
    policy_risks = {
        "互联网": 15,  # 反垄断
        "教育": 25,  # 双减政策
        "游戏": 15,  # 版号限制
        "地产": 20,  # 三道红线
        "医药": 10,  # 集采
        "新能源": -10,  # 政策支持
        "半导体": -10,  # 国产替代
        "AI": -5,  # 政策支持
    }
    score += policy_risks.get(industry, 0)

    return min(max(score, 0), 100)


def get_risk_level(score):
    """获取风险等级"""
    if score <= 30:
        return "低风险", "green"
    elif score <= 45:
        return "中低风险", "yellow-green"
    elif score <= 55:
        return "中等风险", "yellow"
    elif score <= 70:
        return "中高风险", "orange"
    else:
        return "高风险", "red"


def get_recommendation(total_score, risk_level):
    """获取投资建议"""
    if total_score <= 35:
        return "可以积极配置"
    elif total_score <= 45:
        return "可以适当配置"
    elif total_score <= 55:
        return "谨慎配置，控制仓位"
    elif total_score <= 65:
        return "建议观望或小仓位试探"
    else:
        return "建议回避"


def risk_assessment(
    code,
    industry,
    market_cap=None,
    daily_volume=None,
    valuation_level=None,
    is_profitable=True,
    has_competitive_advantage=True,
    output_json=False,
):
    """综合风险评估"""
    result = {
        "code": code,
        "industry": industry,
        "market_cap": market_cap,
        "daily_volume": daily_volume,
    }

    # 各维度评估
    market_risk = assess_market_risk(industry, valuation_level)
    company_risk = assess_company_risk(
        market_cap, is_profitable, has_competitive_advantage
    )
    liquidity_risk = assess_liquidity_risk(daily_volume, market_cap)
    policy_risk = assess_policy_risk(industry)

    # 技术风险（简化处理）
    tech_risk = 50

    result["risk_scores"] = {
        "market_risk": market_risk,
        "company_risk": company_risk,
        "liquidity_risk": liquidity_risk,
        "policy_risk": policy_risk,
        "tech_risk": tech_risk,
    }

    # 加权总分
    weights = {
        "market_risk": 0.25,
        "company_risk": 0.25,
        "liquidity_risk": 0.20,
        "policy_risk": 0.15,
        "tech_risk": 0.15,
    }

    total_score = sum(result["risk_scores"][k] * weights[k] for k in weights)
    result["total_score"] = total_score

    risk_level, color = get_risk_level(total_score)
    result["risk_level"] = risk_level
    result["risk_color"] = color

    recommendation = get_recommendation(total_score, risk_level)
    result["recommendation"] = recommendation

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"风险评估: {code}")
        print("=" * 50)
        print(f"\n行业: {industry}")

        print(f"\n各维度风险评分（0-100，越高风险越大）:")
        print(f"  市场风险: {market_risk:.0f}")
        print(f"  公司风险: {company_risk:.0f}")
        print(f"  流动性风险: {liquidity_risk:.0f}")
        print(f"  政策风险: {policy_risk:.0f}")
        print(f"  技术风险: {tech_risk:.0f}")

        print(f"\n综合评估:")
        print(f"  总分: {total_score:.0f}/100")
        print(f"  风险等级: {risk_level}")
        print(f"  建议: {recommendation}")

        print("\n" + "=" * 50)

    return result


def main():
    parser = argparse.ArgumentParser(description="评估投资风险")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--industry", required=True, help="所属行业")
    parser.add_argument("--market-cap", type=float, help="市值（亿元）")
    parser.add_argument("--daily-volume", type=float, help="日均成交额（亿元）")
    parser.add_argument(
        "--valuation",
        choices=["低估", "合理", "偏高", "高估"],
        help="估值水平",
    )
    parser.add_argument("--not-profitable", action="store_true", help="未盈利")
    parser.add_argument(
        "--no-competitive-advantage", action="store_true", help="无竞争优势"
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = risk_assessment(
        code=args.code,
        industry=args.industry,
        market_cap=args.market_cap,
        daily_volume=args.daily_volume,
        valuation_level=args.valuation,
        is_profitable=not args.not_profitable,
        has_competitive_advantage=not args.no_competitive_advantage,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
