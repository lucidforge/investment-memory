#!/usr/bin/env python3
"""
列出所有已收录的产业趋势
"""

import argparse
import json
import os

# 使用相对路径，从项目根目录执行
MEMORY_DIR = ".memory"
TRENDS_INDEX_FILE = os.path.join(MEMORY_DIR, "industry_trends", "index.json")


def get_phase_emoji(phase):
    """获取阶段对应的emoji"""
    emojis = {
        "emerging": "🌱",
        "growth": "📈",
        "mature": "🏭",
        "decline": "📉",
    }
    return emojis.get(phase, "❓")


def get_phase_label(phase):
    """获取阶段标签"""
    labels = {
        "emerging": "萌芽期",
        "growth": "成长期",
        "mature": "成熟期",
        "decline": "衰退期",
    }
    return labels.get(phase, "未知")


def list_trends(output_json=False):
    """列出所有趋势"""
    if not os.path.exists(TRENDS_INDEX_FILE):
        print(f"错误: 索引文件不存在: {TRENDS_INDEX_FILE}")
        return []

    with open(TRENDS_INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    trends = index.get("trends", [])

    if output_json:
        print(json.dumps(trends, ensure_ascii=False, indent=2))
        return trends

    if not trends:
        print("未找到任何产业趋势")
        return []

    print(f"产业趋势知识库 (共 {len(trends)} 个趋势)")
    print("=" * 70)

    # 按阶段分组
    phases = {"emerging": [], "growth": [], "mature": [], "decline": []}
    for trend in trends:
        phase = trend.get("current_phase", "emerging")
        if phase in phases:
            phases[phase].append(trend)

    # 按阶段输出
    for phase, phase_trends in phases.items():
        if phase_trends:
            print(
                f"\n{get_phase_emoji(phase)} {get_phase_label(phase)} ({len(phase_trends)}个)"
            )
            for trend in phase_trends:
                print(f"  - {trend['trend_name']} ({trend['start_year']}年起)")
                if trend.get("summary"):
                    summary = (
                        trend["summary"][:60] + "..."
                        if len(trend["summary"]) > 60
                        else trend["summary"]
                    )
                    print(f"    {summary}")

    print("\n" + "=" * 70)

    return trends


def main():
    parser = argparse.ArgumentParser(description="列出所有产业趋势")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    trends = list_trends(output_json=args.output_json)

    return 0


if __name__ == "__main__":
    exit(main())
