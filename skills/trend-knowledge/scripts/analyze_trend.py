#!/usr/bin/env python3
"""
分析产业趋势的健康度和投资价值
"""

import argparse
import json
import os
from datetime import datetime

# 使用相对路径，从项目根目录执行
MEMORY_DIR = ".memory"
TRENDS_DIR = os.path.join(MEMORY_DIR, "industry_trends", "trends")
TRENDS_INDEX_FILE = os.path.join(MEMORY_DIR, "industry_trends", "index.json")


def load_trend_detail(trend_id):
    """加载趋势详情"""
    file_path = os.path.join(TRENDS_DIR, f"{trend_id}.json")
    if not os.path.exists(file_path):
        print(f"错误: 未找到趋势文件: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_health_score(trend_data):
    """计算趋势健康度分数（0-100）"""
    score = 0
    phase = trend_data.get("basic_info", {}).get("current_phase", "emerging")

    # 阶段分数
    phase_scores = {
        "emerging": 60,  # 萌芽期：潜力大但风险高
        "growth": 90,  # 成长期：最佳投资时机
        "mature": 70,  # 成熟期：稳定但增速放缓
        "decline": 30,  # 衰退期：风险高
    }
    score = phase_scores.get(phase, 50)

    # 投资机会数量调整
    opps = trend_data.get("investment_opportunities", {})
    total_opps = (
        len(opps.get("short_term", []))
        + len(opps.get("medium_term", []))
        + len(opps.get("long_term", []))
    )
    if total_opps > 6:
        score += 10
    elif total_opps > 3:
        score += 5

    # 教训数量调整（越多越谨慎）
    lessons = trend_data.get("lessons", [])
    if len(lessons) > 3:
        score -= 10

    return min(max(score, 0), 100)


def get_phase_analysis(phase):
    """获取阶段分析"""
    analyses = {
        "emerging": {
            "description": "技术验证阶段，商业化早期",
            "characteristics": [
                "技术突破频繁",
                "资本大量涌入",
                "商业模式未验证",
                "竞争格局未定",
            ],
            "investment_approach": "小仓位试探，关注技术突破和政策支持",
            "key_metrics": ["技术成熟度", "融资规模", "政策支持力度"],
            "risk_factors": ["技术失败", "商业化周期长", "估值泡沫"],
        },
        "growth": {
            "description": "渗透率快速提升，业绩高增长",
            "characteristics": [
                "渗透率突破10%",
                "龙头企业业绩高增长",
                "行业标准逐步确立",
                "竞争加剧",
            ],
            "investment_approach": "重仓龙头，长期持有，关注估值",
            "key_metrics": ["渗透率", "收入增速", "市占率", "估值水平"],
            "risk_factors": ["估值过高", "增速放缓", "竞争加剧", "政策变化"],
        },
        "mature": {
            "description": "增速放缓，行业洗牌完成",
            "characteristics": [
                "渗透率超过40%",
                "增速放缓至20%以下",
                "行业集中度提升",
                "价格竞争",
            ],
            "investment_approach": "关注龙头，估值合理时介入，关注出海",
            "key_metrics": ["市占率", "利润率", "出海进度", "分红率"],
            "risk_factors": ["需求饱和", "技术替代", "国际贸易壁垒"],
        },
        "decline": {
            "description": "需求下降或替代品出现",
            "characteristics": ["需求下降", "产能过剩", "价格战", "企业退出"],
            "investment_approach": "回避或做空",
            "key_metrics": ["需求增速", "产能利用率", "价格走势"],
            "risk_factors": ["行业萎缩", "企业亏损", "资产减值"],
        },
    }
    return analyses.get(phase, {})


def analyze_trend(trend_id):
    """分析趋势健康度"""
    trend_data = load_trend_detail(trend_id)
    if not trend_data:
        return None

    phase = trend_data.get("basic_info", {}).get("current_phase", "emerging")
    health_score = calculate_health_score(trend_data)
    phase_analysis = get_phase_analysis(phase)

    analysis = {
        "trend_id": trend_id,
        "trend_name": trend_data.get("trend_name", ""),
        "current_phase": phase,
        "health_score": health_score,
        "phase_analysis": phase_analysis,
        "investment_opportunities": trend_data.get("investment_opportunities", {}),
        "lessons": trend_data.get("lessons", []),
        "current_status": trend_data.get("current_status", {}),
    }

    return analysis


def main():
    parser = argparse.ArgumentParser(description="分析产业趋势健康度")
    parser.add_argument("--trend-id", required=True, help="趋势ID")
    args = parser.parse_args()

    print(f"分析产业趋势: {args.trend_id}")
    print("=" * 70)

    analysis = analyze_trend(args.trend_id)
    if not analysis:
        return 1

    # 输出分析结果
    print(f"\n趋势名称: {analysis['trend_name']}")
    print(f"当前阶段: {analysis['current_phase']}")
    print(f"健康度分数: {analysis['health_score']}/100")

    phase_info = analysis["phase_analysis"]
    print(f"\n阶段特征:")
    print(f"  描述: {phase_info.get('description', '')}")
    print(f"  特点: {', '.join(phase_info.get('characteristics', []))}")
    print(f"  投资策略: {phase_info.get('investment_approach', '')}")
    print(f"  关注指标: {', '.join(phase_info.get('key_metrics', []))}")
    print(f"  风险因素: {', '.join(phase_info.get('risk_factors', []))}")

    # 投资机会
    opps = analysis["investment_opportunities"]
    if opps.get("short_term"):
        print(f"\n短期机会:")
        for opp in opps["short_term"]:
            print(f"  - {opp}")
    if opps.get("medium_term"):
        print(f"\n中期机会:")
        for opp in opps["medium_term"]:
            print(f"  - {opp}")
    if opps.get("long_term"):
        print(f"\n长期机会:")
        for opp in opps["long_term"]:
            print(f"  - {opp}")

    # 教训
    if analysis["lessons"]:
        print(f"\n历史教训:")
        for lesson in analysis["lessons"]:
            print(f"  - {lesson}")

    # 当前状态
    status = analysis["current_status"]
    if status.get("key_watch"):
        print(f"\n关注要点:")
        for item in status["key_watch"]:
            print(f"  - {item}")
    if status.get("risk_factors"):
        print(f"\n风险因素:")
        for item in status["risk_factors"]:
            print(f"  - {item}")

    print("\n" + "=" * 70)

    # 输出JSON格式
    print("\n完整分析:")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
