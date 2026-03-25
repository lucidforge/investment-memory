#!/usr/bin/env python3
"""
更新危机事件的指定部分
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime


def load_event_file(event_id):
    """加载危机事件详情文件"""
    file_path = f".memory/crisis_knowledge/events/{event_id}.json"
    if not os.path.exists(file_path):
        print(f"错误: 未找到危机事件文件: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_event_file(event_id, event_data):
    """保存危机事件详情文件"""
    file_path = f".memory/crisis_knowledge/events/{event_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(event_data, f, ensure_ascii=False, indent=2)

    return file_path


def update_section(event_data, section, content, append=False):
    """更新事件的指定部分"""
    if section == "event_details":
        if append:
            event_data["event_details"] = event_data.get("event_details", "") + content
        else:
            event_data["event_details"] = content

    elif section == "impact_analysis":
        if append:
            event_data["impact_analysis"] = (
                event_data.get("impact_analysis", "") + content
            )
        else:
            event_data["impact_analysis"] = content

    elif section == "us_stock":
        if "market_impact" not in event_data:
            event_data["market_impact"] = {}
        if "us_stock" not in event_data["market_impact"]:
            event_data["market_impact"]["us_stock"] = {}
        if append:
            event_data["market_impact"]["us_stock"]["content"] = (
                event_data["market_impact"]["us_stock"].get("content", "") + content
            )
        else:
            event_data["market_impact"]["us_stock"]["content"] = content

    elif section == "hk_stock":
        if "market_impact" not in event_data:
            event_data["market_impact"] = {}
        if "hk_stock" not in event_data["market_impact"]:
            event_data["market_impact"]["hk_stock"] = {}
        if append:
            event_data["market_impact"]["hk_stock"]["content"] = (
                event_data["market_impact"]["hk_stock"].get("content", "") + content
            )
        else:
            event_data["market_impact"]["hk_stock"]["content"] = content

    elif section == "a_stock":
        if "market_impact" not in event_data:
            event_data["market_impact"] = {}
        if "a_stock" not in event_data["market_impact"]:
            event_data["market_impact"]["a_stock"] = {}
        if append:
            event_data["market_impact"]["a_stock"]["content"] = (
                event_data["market_impact"]["a_stock"].get("content", "") + content
            )
        else:
            event_data["market_impact"]["a_stock"]["content"] = content

    elif section == "short_term":
        if "investment_opportunities" not in event_data:
            event_data["investment_opportunities"] = {}
        if append:
            existing = event_data["investment_opportunities"].get("short_term", [])
            existing.extend([content])
            event_data["investment_opportunities"]["short_term"] = existing
        else:
            event_data["investment_opportunities"]["short_term"] = [content]

    elif section == "medium_term":
        if "investment_opportunities" not in event_data:
            event_data["investment_opportunities"] = {}
        if append:
            existing = event_data["investment_opportunities"].get("medium_term", [])
            existing.extend([content])
            event_data["investment_opportunities"]["medium_term"] = existing
        else:
            event_data["investment_opportunities"]["medium_term"] = [content]

    elif section == "long_term":
        if "investment_opportunities" not in event_data:
            event_data["investment_opportunities"] = {}
        if append:
            existing = event_data["investment_opportunities"].get("long_term", [])
            existing.extend([content])
            event_data["investment_opportunities"]["long_term"] = existing
        else:
            event_data["investment_opportunities"]["long_term"] = [content]

    elif section == "summary":
        # 更新索引中的摘要
        update_index_summary(event_id, content)

    else:
        print(f"错误: 不支持的更新部分: {section}")
        return False

    return True


def update_index_summary(event_id, summary=None):
    """更新索引中的摘要"""
    index_path = ".memory/crisis_knowledge/index.json"
    if not os.path.exists(index_path):
        print(f"错误: 索引文件不存在: {index_path}")
        return False

    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    # 查找对应的事件
    for event in index.get("events", []):
        if event.get("event_id") == event_id:
            if summary:
                event["summary"] = summary
            else:
                # 从详情文件生成摘要
                event_file = f".memory/crisis_knowledge/events/{event_id}.json"
                if os.path.exists(event_file):
                    with open(event_file, "r", encoding="utf-8") as f:
                        event_data = json.load(f)
                    # 生成摘要（取前200字符）
                    details = event_data.get("event_details", "")
                    event["summary"] = (
                        details[:200] + "..." if len(details) > 200 else details
                    )

            index["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            break

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return True


def main():
    parser = argparse.ArgumentParser(description="更新危机事件详情")
    parser.add_argument("--event-id", required=True, help="危机事件ID")
    parser.add_argument(
        "--section",
        required=True,
        choices=[
            "event_details",
            "impact_analysis",
            "us_stock",
            "hk_stock",
            "a_stock",
            "short_term",
            "medium_term",
            "long_term",
            "summary",
        ],
        help="要更新的部分",
    )
    parser.add_argument("--content", required=True, help="新的内容")
    parser.add_argument("--append", action="store_true", help="是否追加到现有内容")
    args = parser.parse_args()

    print(f"更新危机事件: {args.event_id}")
    print(f"更新部分: {args.section}")
    print(f"模式: {'追加' if args.append else '替换'}")

    # 加载事件数据
    event_data = load_event_file(args.event_id)
    if not event_data:
        return 1

    # 更新指定部分
    if not update_section(event_data, args.section, args.content, args.append):
        return 1

    # 保存更新后的事件数据
    if args.section != "summary":  # summary单独处理
        output_path = save_event_file(args.event_id, event_data)
        print(f"更新成功: {output_path}")

    # 更新索引
    update_index_summary(args.event_id)
    print(f"索引更新成功")

    return 0


if __name__ == "__main__":
    exit(main())
