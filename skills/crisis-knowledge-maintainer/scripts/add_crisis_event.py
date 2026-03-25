#!/usr/bin/env python3
"""
添加新的危机事件到知识库
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime


def create_event_template(args):
    """创建危机事件模板"""
    event_data = {
        "event_id": args.event_id,
        "event_name": args.event_name,
        "basic_info": {
            "event_type": args.event_type,
            "severity": args.severity,
            "time_period": args.time_period,
            "keywords": [k.strip() for k in args.keywords.split(",")],
        },
        "event_details": "",
        "market_impact": {
            "us_stock": {"content": ""},
            "hk_stock": {"content": ""},
            "a_stock": {"content": ""},
        },
        "impact_analysis": "",
        "investment_opportunities": {
            "short_term": [],
            "medium_term": [],
            "long_term": [],
        },
    }

    return event_data


def save_event_file(event_id, event_data):
    """保存危机事件详情文件"""
    file_path = f".memory/crisis_knowledge/events/{event_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(event_data, f, ensure_ascii=False, indent=2)

    return file_path


def add_event_to_index(
    event_id, event_name, event_type, severity, time_period, keywords
):
    """添加事件到索引"""
    index_path = ".memory/crisis_knowledge/index.json"

    # 读取现有索引或创建新的
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {
            "version": "1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "events": [],
        }

    # 创建索引条目
    index_event = {
        "event_id": event_id,
        "event_name": event_name,
        "event_type": event_type,
        "severity": severity,
        "time_period": time_period,
        "keywords": keywords,
        "summary": "",
        "affected_markets": [],
        "key_assets": [],
        "similar_events": [],
    }

    # 添加到索引
    index["events"].append(index_event)
    index["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # 保存索引
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return index_path


def add_link_placeholder(event_id):
    """添加关联占位符"""
    links_path = ".memory/links.json"

    # 读取现有关联或创建新的
    if os.path.exists(links_path):
        with open(links_path, "r", encoding="utf-8") as f:
            links = json.load(f)
    else:
        links = {
            "version": "1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "crisis_to_lessons": {},
            "lesson_to_crisis": {},
            "crisis_to_crisis": {},
        }

    # 添加占位符
    if event_id not in links["crisis_to_lessons"]:
        links["crisis_to_lessons"][event_id] = []
    if event_id not in links["crisis_to_crisis"]:
        links["crisis_to_crisis"][event_id] = []

    links["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # 保存关联
    with open(links_path, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)

    return links_path


def main():
    parser = argparse.ArgumentParser(description="添加新的危机事件")
    parser.add_argument(
        "--event-id", required=True, help="事件ID（格式：CRISIS_YYYY_NAME）"
    )
    parser.add_argument("--event-name", required=True, help="事件名称")
    parser.add_argument(
        "--event-type",
        required=True,
        choices=["economic", "military", "political", "public_health"],
        help="事件类型",
    )
    parser.add_argument(
        "--severity",
        required=True,
        choices=["critical", "high", "medium"],
        help="影响程度",
    )
    parser.add_argument("--time-period", required=True, help="时间范围")
    parser.add_argument("--keywords", required=True, help="关键词（逗号分隔）")
    args = parser.parse_args()

    print(f"添加新的危机事件: {args.event_id}")
    print(f"事件名称: {args.event_name}")
    print(f"事件类型: {args.event_type}")
    print(f"影响程度: {args.severity}")

    # 创建事件模板
    event_data = create_event_template(args)

    # 保存事件详情文件
    event_file_path = save_event_file(args.event_id, event_data)
    print(f"创建事件详情文件: {event_file_path}")

    # 添加到索引
    keywords_list = [k.strip() for k in args.keywords.split(",")]
    index_path = add_event_to_index(
        args.event_id,
        args.event_name,
        args.event_type,
        args.severity,
        args.time_period,
        keywords_list,
    )
    print(f"更新索引文件: {index_path}")

    # 添加关联占位符
    links_path = add_link_placeholder(args.event_id)
    print(f"更新关联文件: {links_path}")

    print(f"\n危机事件添加成功！")
    print(f"下一步：请填充以下内容：")
    print(f"  1. 事件详情 (event_details)")
    print(f"  2. 市场影响分析 (market_impact)")
    print(f"  3. 影响原因分析 (impact_analysis)")
    print(f"  4. 投资机会分析 (investment_opportunities)")

    return 0


if __name__ == "__main__":
    exit(main())
