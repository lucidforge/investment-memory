#!/usr/bin/env python3
"""
根据当前形势查询相关的危机知识和教训
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
        choices=["crisis", "lessons", "patterns", "all"],
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

    # 输出结果
    print("\n查询结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
