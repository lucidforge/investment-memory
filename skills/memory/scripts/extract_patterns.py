#!/usr/bin/env python3
"""
从危机知识中提取投资规律
"""

import argparse
import json
import os
from datetime import datetime
from config import (
    CRISIS_EVENTS_DIR,
    PATTERNS_FILE,
    load_json_file,
    save_json_file,
    get_current_date,
)


def load_patterns_file():
    """加载现有的投资规律文件"""
    return load_json_file(
        PATTERNS_FILE,
        default={
            "version": "1.0",
            "last_updated": get_current_date(),
            "patterns": [],
        },
    )


def save_patterns_file(patterns):
    """保存投资规律文件"""
    patterns["last_updated"] = get_current_date()
    save_json_file(PATTERNS_FILE, patterns)
    return PATTERNS_FILE


def load_event_detail(event_id):
    """加载事件详情"""
    file_path = os.path.join(CRISIS_EVENTS_DIR, f"{event_id}.json")
    return load_json_file(file_path, default=None)


def extract_patterns_from_event(event):
    """从单个事件中提取投资规律"""
    patterns = []
    event_id = event.get("event_id", "")
    event_name = event.get("event_name", "")
    event_type = event.get("basic_info", {}).get("event_type", "other")
    keywords = event.get("basic_info", {}).get("keywords", [])

    investment_opps = event.get("investment_opportunities", {})

    # 提取短期投资规律
    short_term = investment_opps.get("short_term", [])
    if short_term:
        pattern = {
            "pattern_id": f"PATTERN_{event_id}_SHORT",
            "name": f"{event_name}短期投资规律",
            "description": f"{event_name}期间的短期投资机会：{'; '.join(short_term[:3])}",
            "crisis_types": [event_type],
            "keywords": keywords,
            "confidence": 0.7,
            "exceptions": [],
            "source_events": [event_id],
        }
        patterns.append(pattern)

    # 提取中期投资规律
    medium_term = investment_opps.get("medium_term", [])
    if medium_term:
        pattern = {
            "pattern_id": f"PATTERN_{event_id}_MEDIUM",
            "name": f"{event_name}中期投资规律",
            "description": f"{event_name}后1-2年的投资机会：{'; '.join(medium_term[:3])}",
            "crisis_types": [event_type],
            "keywords": keywords,
            "confidence": 0.7,
            "exceptions": [],
            "source_events": [event_id],
        }
        patterns.append(pattern)

    # 提取长期投资规律
    long_term = investment_opps.get("long_term", [])
    if long_term:
        pattern = {
            "pattern_id": f"PATTERN_{event_id}_LONG",
            "name": f"{event_name}长期投资规律",
            "description": f"{event_name}后3年以上的投资机会：{'; '.join(long_term[:3])}",
            "crisis_types": [event_type],
            "keywords": keywords,
            "confidence": 0.7,
            "exceptions": [],
            "source_events": [event_id],
        }
        patterns.append(pattern)

    # 提取市场影响规律
    market_impact = event.get("market_impact", {})
    us_stock = market_impact.get("us_stock", {}).get("content", "")
    hk_stock = market_impact.get("hk_stock", {}).get("content", "")
    a_stock = market_impact.get("a_stock", {}).get("content", "")

    if us_stock or hk_stock or a_stock:
        impact_summary = []
        if us_stock:
            impact_summary.append("美股受影响")
        if hk_stock:
            impact_summary.append("港股受影响")
        if a_stock:
            impact_summary.append("A股受影响")

        pattern = {
            "pattern_id": f"PATTERN_{event_id}_IMPACT",
            "name": f"{event_name}市场影响规律",
            "description": f"{event_name}对各市场的影响：{', '.join(impact_summary)}",
            "crisis_types": [event_type],
            "keywords": keywords,
            "confidence": 0.8,
            "exceptions": [],
            "source_events": [event_id],
        }
        patterns.append(pattern)

    return patterns


def extract_patterns_from_single_event(event_id):
    """从单个指定事件提取投资规律"""
    event = load_event_detail(event_id)
    if not event:
        print(f"错误: 未找到事件 {event_id}")
        return []

    return extract_patterns_from_event(event)


def extract_patterns_from_all_events():
    """从所有事件批量提取投资规律"""
    if not os.path.exists(CRISIS_EVENTS_DIR):
        print(f"错误: 事件目录不存在: {CRISIS_EVENTS_DIR}")
        return []

    all_patterns = []

    for filename in os.listdir(CRISIS_EVENTS_DIR):
        if filename.endswith(".json"):
            event_id = filename[:-5]  # 去掉 .json 后缀
            event = load_event_detail(event_id)
            if event:
                patterns = extract_patterns_from_event(event)
                all_patterns.extend(patterns)

    return all_patterns


def deduplicate_patterns(patterns):
    """去重重规律"""
    unique_patterns = []
    seen_ids = set()

    for pattern in patterns:
        pattern_id = pattern.get("pattern_id", "")
        if pattern_id not in seen_ids:
            unique_patterns.append(pattern)
            seen_ids.add(pattern_id)

    return unique_patterns


def merge_patterns(existing_patterns, new_patterns):
    """合并现有规律和新规律"""
    merged = existing_patterns.copy()
    existing_ids = {p.get("pattern_id") for p in merged}

    for new_pattern in new_patterns:
        new_id = new_pattern.get("pattern_id", "")
        if new_id not in existing_ids:
            merged.append(new_pattern)
            existing_ids.add(new_id)

    return merged


def main():
    parser = argparse.ArgumentParser(description="提取投资规律")
    parser.add_argument("--from-crisis", help="从指定危机事件提取规律")
    parser.add_argument(
        "--mode", choices=["single", "batch"], default="single", help="提取模式"
    )
    args = parser.parse_args()

    print(f"提取投资规律")
    print(f"危机事件: {args.from_crisis or '所有'}")
    print(f"模式: {args.mode}")

    # 加载现有规律
    patterns = load_patterns_file()
    existing_patterns = patterns.get("patterns", [])

    # 提取新规律
    new_patterns = []

    if args.mode == "single" and args.from_crisis:
        # 从单个事件提取
        new_patterns = extract_patterns_from_single_event(args.from_crisis)
    else:
        # 批量提取
        new_patterns = extract_patterns_from_all_events()

    print(f"提取到 {len(new_patterns)} 个新规律")

    # 去重
    unique_new_patterns = deduplicate_patterns(new_patterns)
    print(f"去重后 {len(unique_new_patterns)} 个规律")

    # 合并
    merged_patterns = merge_patterns(existing_patterns, unique_new_patterns)
    print(f"合并后共 {len(merged_patterns)} 个规律")

    # 更新规律结构
    patterns["patterns"] = merged_patterns

    # 保存
    output_path = save_patterns_file(patterns)
    print(f"保存投资规律文件: {output_path}")

    return 0


if __name__ == "__main__":
    exit(main())
