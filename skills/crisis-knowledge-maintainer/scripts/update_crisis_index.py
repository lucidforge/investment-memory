#!/usr/bin/env python3
"""
更新危机事件在索引中的摘要信息
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


def load_index_file():
    """加载索引文件"""
    index_path = ".memory/crisis_knowledge/index.json"
    if not os.path.exists(index_path):
        print(f"错误: 索引文件不存在: {index_path}")
        return None

    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index_file(index_data):
    """保存索引文件"""
    index_path = ".memory/crisis_knowledge/index.json"
    index_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    return index_path


def generate_summary_from_event(event_data):
    """从事件详情生成摘要"""
    # 获取事件详情
    details = event_data.get("event_details", "")
    if not details:
        return ""

    # 生成摘要（取前200字符）
    if len(details) > 200:
        # 尝试在句号处截断
        truncated = details[:200]
        last_period = truncated.rfind("。")
        if last_period > 100:  # 如果句号位置合理
            summary = details[: last_period + 1]
        else:
            summary = truncated + "..."
    else:
        summary = details

    return summary


def update_index_event(index_data, event_id, summary=None):
    """更新索引中的事件摘要"""
    for event in index_data.get("events", []):
        if event.get("event_id") == event_id:
            if summary:
                event["summary"] = summary
                print(f"使用指定摘要更新: {event_id}")
            else:
                # 从详情文件生成摘要
                event_data = load_event_file(event_id)
                if event_data:
                    new_summary = generate_summary_from_event(event_data)
                    event["summary"] = new_summary
                    print(f"从详情生成摘要更新: {event_id}")
                else:
                    print(f"错误: 无法加载事件详情: {event_id}")
                    return False
            return True

    print(f"错误: 未找到事件: {event_id}")
    return False


def main():
    parser = argparse.ArgumentParser(description="更新危机事件索引摘要")
    parser.add_argument("--event-id", required=True, help="危机事件ID")
    parser.add_argument(
        "--summary", help="新的摘要（可选，如果不提供则自动从详情生成）"
    )
    args = parser.parse_args()

    print(f"更新索引摘要: {args.event_id}")

    # 加载索引数据
    index_data = load_index_file()
    if not index_data:
        return 1

    # 更新事件摘要
    if not update_index_event(index_data, args.event_id, args.summary):
        return 1

    # 保存更新后的索引
    output_path = save_index_file(index_data)
    print(f"索引更新成功: {output_path}")

    return 0


if __name__ == "__main__":
    exit(main())
