#!/usr/bin/env python3
"""
更新产业趋势的阶段和信息
"""

import argparse
import json
import os
from datetime import datetime

# 使用相对路径，从项目根目录执行
MEMORY_DIR = ".memory"
TRENDS_DIR = os.path.join(MEMORY_DIR, "industry_trends", "trends")
TRENDS_INDEX_FILE = os.path.join(MEMORY_DIR, "industry_trends", "index.json")


def load_trend_file(trend_id):
    """加载趋势详情文件"""
    file_path = os.path.join(TRENDS_DIR, f"{trend_id}.json")
    if not os.path.exists(file_path):
        print(f"错误: 未找到趋势文件: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_trend_file(trend_id, trend_data):
    """保存趋势详情文件"""
    file_path = os.path.join(TRENDS_DIR, f"{trend_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(trend_data, f, ensure_ascii=False, indent=2)

    return file_path


def update_index_phase(trend_id, new_phase):
    """更新索引中的趋势阶段"""
    if not os.path.exists(TRENDS_INDEX_FILE):
        print(f"错误: 索引文件不存在: {TRENDS_INDEX_FILE}")
        return False

    with open(TRENDS_INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    # 查找对应的趋势
    for trend in index.get("trends", []):
        if trend.get("trend_id") == trend_id:
            trend["current_phase"] = new_phase
            index["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            break

    with open(TRENDS_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return True


def update_section(trend_data, section, content, append=False):
    """更新趋势的指定部分"""
    if section == "trend_details":
        if append:
            trend_data["trend_details"] = trend_data.get("trend_details", "") + content
        else:
            trend_data["trend_details"] = content

    elif section == "us_stock":
        if "market_impact" not in trend_data:
            trend_data["market_impact"] = {}
        if "us_stock" not in trend_data["market_impact"]:
            trend_data["market_impact"]["us_stock"] = {}
        if append:
            trend_data["market_impact"]["us_stock"]["content"] = (
                trend_data["market_impact"]["us_stock"].get("content", "") + content
            )
        else:
            trend_data["market_impact"]["us_stock"]["content"] = content

    elif section == "hk_stock":
        if "market_impact" not in trend_data:
            trend_data["market_impact"] = {}
        if "hk_stock" not in trend_data["market_impact"]:
            trend_data["market_impact"]["hk_stock"] = {}
        if append:
            trend_data["market_impact"]["hk_stock"]["content"] = (
                trend_data["market_impact"]["hk_stock"].get("content", "") + content
            )
        else:
            trend_data["market_impact"]["hk_stock"]["content"] = content

    elif section == "a_stock":
        if "market_impact" not in trend_data:
            trend_data["market_impact"] = {}
        if "a_stock" not in trend_data["market_impact"]:
            trend_data["market_impact"]["a_stock"] = {}
        if append:
            trend_data["market_impact"]["a_stock"]["content"] = (
                trend_data["market_impact"]["a_stock"].get("content", "") + content
            )
        else:
            trend_data["market_impact"]["a_stock"]["content"] = content

    elif section == "short_term":
        if "investment_opportunities" not in trend_data:
            trend_data["investment_opportunities"] = {}
        if append:
            existing = trend_data["investment_opportunities"].get("short_term", [])
            existing.extend([content])
            trend_data["investment_opportunities"]["short_term"] = existing
        else:
            trend_data["investment_opportunities"]["short_term"] = [content]

    elif section == "medium_term":
        if "investment_opportunities" not in trend_data:
            trend_data["investment_opportunities"] = {}
        if append:
            existing = trend_data["investment_opportunities"].get("medium_term", [])
            existing.extend([content])
            trend_data["investment_opportunities"]["medium_term"] = existing
        else:
            trend_data["investment_opportunities"]["medium_term"] = [content]

    elif section == "long_term":
        if "investment_opportunities" not in trend_data:
            trend_data["investment_opportunities"] = {}
        if append:
            existing = trend_data["investment_opportunities"].get("long_term", [])
            existing.extend([content])
            trend_data["investment_opportunities"]["long_term"] = existing
        else:
            trend_data["investment_opportunities"]["long_term"] = [content]

    elif section == "lessons":
        if append:
            existing = trend_data.get("lessons", [])
            existing.extend([content])
            trend_data["lessons"] = existing
        else:
            trend_data["lessons"] = [content]

    elif section == "phase":
        new_phase = content
        if "current_status" not in trend_data:
            trend_data["current_status"] = {}
        trend_data["current_status"]["phase"] = new_phase
        trend_data["basic_info"]["current_phase"] = new_phase
        # 同时更新索引
        update_index_phase(trend_data["trend_id"], new_phase)

    else:
        print(f"错误: 不支持的更新部分: {section}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="更新产业趋势")
    parser.add_argument("--trend-id", required=True, help="趋势ID")
    parser.add_argument(
        "--section",
        required=True,
        choices=[
            "trend_details",
            "us_stock",
            "hk_stock",
            "a_stock",
            "short_term",
            "medium_term",
            "long_term",
            "lessons",
            "phase",
        ],
        help="要更新的部分",
    )
    parser.add_argument("--content", required=True, help="新的内容")
    parser.add_argument("--append", action="store_true", help="是否追加到现有内容")
    args = parser.parse_args()

    print(f"更新产业趋势: {args.trend_id}")
    print(f"更新部分: {args.section}")
    print(f"模式: {'追加' if args.append else '替换'}")

    # 加载趋势数据
    trend_data = load_trend_file(args.trend_id)
    if not trend_data:
        return 1

    # 更新指定部分
    if not update_section(trend_data, args.section, args.content, args.append):
        return 1

    # 保存更新后的趋势数据
    output_path = save_trend_file(args.trend_id, trend_data)
    print(f"更新成功: {output_path}")

    return 0


if __name__ == "__main__":
    exit(main())
