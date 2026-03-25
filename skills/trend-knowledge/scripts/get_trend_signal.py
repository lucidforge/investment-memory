#!/usr/bin/env python3
"""
根据当前形势查询相关的产业趋势
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
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_relevance_score(trend, situation):
    """计算趋势与当前形势的相关性分数"""
    score = 0.0
    situation_lower = situation.lower()

    # 关键词匹配
    keywords = trend.get("keywords", [])
    for keyword in keywords:
        if keyword.lower() in situation_lower:
            score += 0.3

    # 趋势名称匹配
    trend_name = trend.get("trend_name", "").lower()
    if any(word in situation_lower for word in trend_name.split()):
        score += 0.2

    # 摘要匹配
    summary = trend.get("summary", "").lower()
    if any(word in summary for word in situation_lower.split()):
        score += 0.1

    # 触发事件匹配
    trigger = trend.get("trigger_event", "").lower()
    if any(word in trigger for word in situation_lower.split()):
        score += 0.1

    return min(score, 1.0)


def get_phase_risk_level(phase):
    """获取阶段风险等级"""
    risk_levels = {
        "emerging": "极高",
        "growth": "中高",
        "mature": "中等",
        "decline": "高",
    }
    return risk_levels.get(phase, "未知")


def get_phase_investment_strategy(phase):
    """获取阶段投资策略"""
    strategies = {
        "emerging": "小仓位试探，关注技术突破",
        "growth": "重仓龙头，长期持有",
        "mature": "关注龙头，估值合理时介入",
        "decline": "回避或做空",
    }
    return strategies.get(phase, "未知")


def search_relevant_trends(situation, limit):
    """搜索相关的产业趋势"""
    if not os.path.exists(TRENDS_INDEX_FILE):
        print(f"错误: 索引文件不存在: {TRENDS_INDEX_FILE}")
        return []

    with open(TRENDS_INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    trends = index.get("trends", [])
    scored_trends = []

    for trend in trends:
        score = calculate_relevance_score(trend, situation)
        if score > 0:
            # 加载完整详情
            full_detail = load_trend_detail(trend["trend_id"])
            if full_detail:
                scored_trends.append(
                    {
                        "trend_id": trend["trend_id"],
                        "relevance_score": score,
                        "trend_name": trend["trend_name"],
                        "current_phase": trend.get("current_phase", "emerging"),
                        "start_year": trend.get("start_year", 0),
                        "summary": trend.get("summary", ""),
                        "risk_level": get_phase_risk_level(
                            trend.get("current_phase", "emerging")
                        ),
                        "investment_strategy": get_phase_investment_strategy(
                            trend.get("current_phase", "emerging")
                        ),
                        "full_content": full_detail,
                    }
                )

    # 按相关性分数排序
    scored_trends.sort(key=lambda x: x["relevance_score"], reverse=True)

    # 返回指定数量的结果
    return scored_trends[:limit]


def main():
    parser = argparse.ArgumentParser(description="查询相关产业趋势")
    parser.add_argument("--situation", required=True, help="当前形势描述")
    parser.add_argument("--limit", type=int, default=3, help="最大返回数量")
    args = parser.parse_args()

    print(f"查询相关产业趋势: {args.situation}")
    print(f"限制: {args.limit}")

    # 搜索相关的产业趋势
    relevant_trends = search_relevant_trends(args.situation, args.limit)

    if not relevant_trends:
        print("\n未找到相关的产业趋势")
        return 0

    print(f"\n找到 {len(relevant_trends)} 个相关产业趋势:")
    print("=" * 70)

    for i, trend in enumerate(relevant_trends, 1):
        print(f"\n{i}. {trend['trend_name']} (相关度: {trend['relevance_score']:.2f})")
        print(f"   阶段: {trend['current_phase']} | 风险: {trend['risk_level']}")
        print(f"   策略: {trend['investment_strategy']}")
        if trend["summary"]:
            summary = (
                trend["summary"][:100] + "..."
                if len(trend["summary"]) > 100
                else trend["summary"]
            )
            print(f"   摘要: {summary}")

    print("\n" + "=" * 70)

    # 输出JSON格式结果
    result = {
        "situation": args.situation,
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "relevant_trends": [
            {
                "trend_id": t["trend_id"],
                "trend_name": t["trend_name"],
                "relevance_score": t["relevance_score"],
                "current_phase": t["current_phase"],
                "risk_level": t["risk_level"],
                "investment_strategy": t["investment_strategy"],
            }
            for t in relevant_trends
        ],
    }

    print("\n查询结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
