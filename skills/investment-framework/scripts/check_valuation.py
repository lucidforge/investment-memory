#!/usr/bin/env python3
"""
检查资产估值是否合理
"""

import argparse
import json


def calculate_pe_percentile(pe, industry_pe=None):
    """计算PE相对行业的位置"""
    if industry_pe and industry_pe > 0:
        ratio = pe / industry_pe
        if ratio < 0.7:
            return "低估", 0.2
        elif ratio < 1.0:
            return "合理偏低", 0.4
        elif ratio < 1.3:
            return "合理偏高", 0.6
        elif ratio < 1.6:
            return "偏高", 0.8
        else:
            return "高估", 1.0
    return "未知", 0.5


def calculate_peg(pe, growth_rate):
    """计算PEG（市盈率相对盈利增长比率）"""
    if growth_rate and growth_rate > 0:
        return pe / growth_rate
    return None


def get_peg_assessment(peg):
    """获取PEG评估"""
    if peg is None:
        return "无法评估"
    if peg < 0.5:
        return "明显低估"
    elif peg < 1.0:
        return "可能低估"
    elif peg < 1.5:
        return "合理估值"
    elif peg < 2.0:
        return "合理偏高"
    elif peg < 3.0:
        return "可能高估"
    else:
        return "明显高估"


def get_recommendation(pe_assessment, peg_assessment, growth_rate):
    """获取综合建议"""
    # 评分系统
    score = 50

    # PE评估
    pe_scores = {
        "低估": 30,
        "合理偏低": 15,
        "合理偏高": -10,
        "偏高": -20,
        "高估": -30,
    }
    score += pe_scores.get(pe_assessment, 0)

    # PEG评估
    peg_scores = {
        "明显低估": 25,
        "可能低估": 15,
        "合理估值": 0,
        "合理偏高": -10,
        "可能高估": -20,
        "明显高估": -25,
    }
    score += peg_scores.get(peg_assessment, 0)

    # 增长率调整
    if growth_rate:
        if growth_rate > 30:
            score += 10
        elif growth_rate > 20:
            score += 5
        elif growth_rate < 10:
            score -= 10

    # 生成建议
    if score >= 70:
        return "强烈建议买入", score
    elif score >= 55:
        return "建议买入", score
    elif score >= 45:
        return "可以持有", score
    elif score >= 35:
        return "建议观望", score
    else:
        return "建议回避", score


def check_valuation(
    code, pe, industry_pe=None, growth_rate=None, pb=None, output_json=False
):
    """检查估值"""
    result = {
        "code": code,
        "pe": pe,
        "industry_pe": industry_pe,
        "growth_rate": growth_rate,
        "pb": pb,
    }

    # PE相对评估
    pe_assessment, pe_percentile = calculate_pe_percentile(pe, industry_pe)
    result["pe_assessment"] = pe_assessment
    result["pe_percentile"] = pe_percentile

    # PEG计算
    peg = calculate_peg(pe, growth_rate)
    result["peg"] = peg
    peg_assessment = get_peg_assessment(peg)
    result["peg_assessment"] = peg_assessment

    # 综合建议
    recommendation, score = get_recommendation(
        pe_assessment, peg_assessment, growth_rate
    )
    result["recommendation"] = recommendation
    result["score"] = score

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"估值检查: {code}")
        print("=" * 50)
        print(f"\nPE估值:")
        print(f"  当前PE: {pe}")
        if industry_pe:
            print(f"  行业PE: {industry_pe}")
            print(f"  相对位置: {pe_assessment} (PE/行业PE = {pe / industry_pe:.2f})")

        print(f"\nPEG分析:")
        if peg is not None:
            print(f"  PEG: {peg:.2f}")
            print(f"  评估: {peg_assessment}")
            print(f"  增长率: {growth_rate}%")
        else:
            print(f"  无法计算PEG（需要增长率）")

        print(f"\n综合建议:")
        print(f"  建议: {recommendation}")
        print(f"  评分: {score}/100")

        print("\n" + "=" * 50)

    return result


def main():
    parser = argparse.ArgumentParser(description="检查资产估值")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--pe", type=float, required=True, help="市盈率")
    parser.add_argument("--industry-pe", type=float, help="行业平均市盈率")
    parser.add_argument("--growth-rate", type=float, help="预期增长率（%）")
    parser.add_argument("--pb", type=float, help="市净率")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = check_valuation(
        code=args.code,
        pe=args.pe,
        industry_pe=args.industry_pe,
        growth_rate=args.growth_rate,
        pb=args.pb,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
