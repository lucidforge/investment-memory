#!/usr/bin/env python3
"""
根据当前形势查询相关的危机知识、教训和产业趋势
"""

import argparse
import json
import os
from datetime import datetime
from config import (
    CRISIS_INDEX_FILE,
    LESSONS_INDEX_FILE,
    CRISIS_EVENTS_DIR,
    LESSONS_DIR,
    PATTERNS_FILE,
    TRENDS_INDEX_FILE,
    TRENDS_DIR,
    load_json_file,
)


def load_event_detail(event_id):
    """加载事件详情"""
    file_path = os.path.join(CRISIS_EVENTS_DIR, f"{event_id}.json")
    return load_json_file(file_path, default=None)


def load_lesson_detail(lesson_id):
    """加载教训详情"""
    file_path = os.path.join(LESSONS_DIR, f"{lesson_id}.json")
    return load_json_file(file_path, default=None)


def calculate_relevance_score(event, situation):
    """计算事件与当前形势的相关性分数"""
    score = 0.0
    situation_lower = situation.lower()

    # 关键词匹配
    keywords = event.get("keywords", [])
    for keyword in keywords:
        if keyword.lower() in situation_lower:
            score += 0.3

    # 事件类型匹配
    event_type = event.get("event_type", "")
    type_keywords = {
        "military": ["战争", "冲突", "军事", "袭击", "导弹", "封锁", "石油", "原油"],
        "economic": ["危机", "崩盘", "泡沫", "银行", "金融", "经济", "衰退"],
        "political": ["脱欧", "贸易", "关税", "制裁", "政治"],
        "public_health": ["疫情", "病毒", "卫生", "疾病"],
    }

    if event_type in type_keywords:
        for keyword in type_keywords[event_type]:
            if keyword in situation_lower:
                score += 0.2

    # 摘要匹配
    summary = event.get("summary", "").lower()
    summary_keywords = ["中东", "石油", "原油", "能源", "战争", "冲突", "危机", "银行"]
    for keyword in summary_keywords:
        if keyword in summary and keyword in situation_lower:
            score += 0.1

    return min(score, 1.0)


def calculate_lesson_relevance(lesson, situation):
    """计算教训与当前形势的相关性分数"""
    score = 0.0
    situation_lower = situation.lower()

    # 关键词匹配
    keywords = lesson.get("keywords", [])
    for keyword in keywords:
        if keyword.lower() in situation_lower:
            score += 0.3

    # 相关危机匹配
    related_crisis = lesson.get("related_crisis", "")
    if related_crisis:
        # 加载相关危机信息
        crisis_event = load_event_detail(related_crisis)
        if crisis_event:
            crisis_score = calculate_relevance_score(crisis_event, situation)
            score += crisis_score * 0.5

    # 教训摘要匹配
    summary = lesson.get("summary", "").lower()
    asset_keywords = ["黄金", "原油", "石油", "股票", "债券", "汇率", "银行"]
    for keyword in asset_keywords:
        if keyword in summary and keyword in situation_lower:
            score += 0.2

    return min(score, 1.0)


def search_relevant_crises(situation, limit):
    """搜索相关的危机事件"""
    index = load_json_file(CRISIS_INDEX_FILE, default=None)
    if not index:
        return []

    events = index.get("events", [])
    scored_events = []

    for event in events:
        score = calculate_relevance_score(event, situation)
        if score > 0:
            scored_events.append(
                {
                    "event_id": event["event_id"],
                    "relevance_score": score,
                    "event_name": event["event_name"],
                    "severity": event.get("severity", "medium"),
                    "time_period": event.get("time_period", ""),
                    "summary": event.get("summary", ""),
                }
            )

    # 按相关性分数排序
    scored_events.sort(key=lambda x: x["relevance_score"], reverse=True)

    # 返回指定数量的结果
    return scored_events[:limit]


def search_relevant_lessons(situation, limit):
    """搜索相关的教训"""
    index = load_json_file(LESSONS_INDEX_FILE, default=None)
    if not index:
        return []

    lessons = index.get("lessons", [])
    scored_lessons = []

    for lesson in lessons:
        score = calculate_lesson_relevance(lesson, situation)
        if score > 0:
            scored_lessons.append(
                {
                    "lesson_id": lesson["lesson_id"],
                    "relevance_score": score,
                    "related_crisis": lesson.get("related_crisis", ""),
                    "summary": lesson.get("summary", ""),
                    "keywords": lesson.get("keywords", []),
                }
            )

    # 按相关性分数排序
    scored_lessons.sort(key=lambda x: x["relevance_score"], reverse=True)

    # 返回指定数量的结果
    return scored_lessons[:limit]


def search_relevant_patterns(situation, limit):
    """搜索相关的投资规律"""
    patterns_data = load_json_file(PATTERNS_FILE, default=None)
    if not patterns_data:
        return []

    patterns = patterns_data.get("patterns", [])
    scored_patterns = []

    for pattern in patterns:
        score = 0.0
        situation_lower = situation.lower()

        # 关键词匹配
        keywords = pattern.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in situation_lower:
                score += 0.3

        # 规律描述匹配
        description = pattern.get("description", "").lower()
        if any(word in description for word in situation_lower.split()):
            score += 0.2

        if score > 0:
            scored_patterns.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "relevance_score": score,
                    "name": pattern.get("name", ""),
                    "description": pattern.get("description", ""),
                    "confidence": pattern.get("confidence", 0.7),
                }
            )

    # 按相关性分数排序
    scored_patterns.sort(key=lambda x: x["relevance_score"], reverse=True)

    return scored_patterns[:limit]


def load_trend_detail(trend_id):
    """加载产业趋势详情"""
    file_path = os.path.join(TRENDS_DIR, f"{trend_id}.json")
    return load_json_file(file_path, default=None)


def calculate_trend_relevance(trend, situation):
    """计算产业趋势与当前形势的相关性分数"""
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
    index = load_json_file(TRENDS_INDEX_FILE, default=None)
    if not index:
        return []

    trends = index.get("trends", [])
    scored_trends = []

    for trend in trends:
        score = calculate_trend_relevance(trend, situation)
        if score > 0:
            scored_trends.append(
                {
                    "trend_id": trend["trend_id"],
                    "relevance_score": score,
                    "trend_name": trend.get("trend_name", ""),
                    "current_phase": trend.get("current_phase", "emerging"),
                    "start_year": trend.get("start_year", 0),
                    "summary": trend.get("summary", ""),
                    "risk_level": get_phase_risk_level(
                        trend.get("current_phase", "emerging")
                    ),
                    "investment_strategy": get_phase_investment_strategy(
                        trend.get("current_phase", "emerging")
                    ),
                }
            )

    # 按相关性分数排序
    scored_trends.sort(key=lambda x: x["relevance_score"], reverse=True)

    # 返回指定数量的结果
    return scored_trends[:limit]


def load_full_content(relevant_items, item_type):
    """加载相关项目的完整内容"""
    results = []

    for item in relevant_items:
        if item_type == "crisis":
            full_content = load_event_detail(item["event_id"])
        elif item_type == "lesson":
            full_content = load_lesson_detail(item["lesson_id"])
        elif item_type == "pattern":
            full_content = item  # 规律已经包含完整内容
        elif item_type == "trend":
            full_content = load_trend_detail(item["trend_id"])
        else:
            full_content = None

        if full_content:
            results.append(
                {
                    "relevance_score": item["relevance_score"],
                    "full_content": full_content,
                }
            )

    return results


def main():
    parser = argparse.ArgumentParser(description="查询相关知识")
    parser.add_argument(
        "--type",
        choices=["crisis", "lessons", "patterns", "trends", "all"],
        default="all",
        help="查询类型",
    )
    parser.add_argument("--situation", required=True, help="当前形势描述")
    parser.add_argument("--limit", type=int, default=3, help="最大返回数量")
    args = parser.parse_args()

    print(f"查询相关知识: {args.situation}")
    print(f"类型: {args.type}, 限制: {args.limit}")

    result = {
        "situation": args.situation,
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "relevant_crises": [],
        "relevant_lessons": [],
        "relevant_patterns": [],
        "relevant_trends": [],
    }

    # 搜索相关的危机事件
    if args.type in ["crisis", "all"]:
        relevant_crises = search_relevant_crises(args.situation, args.limit)
        if relevant_crises:
            result["relevant_crises"] = load_full_content(relevant_crises, "crisis")
            print(f"找到 {len(result['relevant_crises'])} 个相关危机事件")

    # 搜索相关的教训
    if args.type in ["lessons", "all"]:
        relevant_lessons = search_relevant_lessons(args.situation, args.limit)
        if relevant_lessons:
            result["relevant_lessons"] = load_full_content(relevant_lessons, "lesson")
            print(f"找到 {len(result['relevant_lessons'])} 个相关教训")

    # 搜索相关的投资规律
    if args.type in ["patterns", "all"]:
        relevant_patterns = search_relevant_patterns(args.situation, args.limit)
        if relevant_patterns:
            result["relevant_patterns"] = relevant_patterns
            print(f"找到 {len(result['relevant_patterns'])} 个相关规律")

    # 搜索相关的产业趋势
    if args.type in ["trends", "all"]:
        relevant_trends = search_relevant_trends(args.situation, args.limit)
        if relevant_trends:
            result["relevant_trends"] = load_full_content(relevant_trends, "trend")
            print(f"找到 {len(result['relevant_trends'])} 个相关产业趋势")

    # 输出结果
    print("\n查询结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
