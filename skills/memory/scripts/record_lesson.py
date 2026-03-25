#!/usr/bin/env python3
"""
记录智能体的学习教训
"""

import argparse
import json
import uuid
from datetime import datetime
from config import (
    LESSONS_DIR,
    LESSONS_INDEX_FILE,
    LINKS_FILE,
    load_json_file,
    save_json_file,
    get_current_date,
)


def generate_lesson_id():
    """生成教训ID"""
    date_str = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:8]
    return f"LESSON_{date_str}_{unique_id}"


def create_lesson_data(args):
    """创建教训数据结构"""
    lesson_id = generate_lesson_id()

    lesson_data = {
        "lesson_id": lesson_id,
        "date": get_current_date(),
        "related_crisis": args.related_crisis,
        "judgment": {
            "asset": args.asset,
            "direction": args.judgment,
            "reasoning": args.reasoning if hasattr(args, "reasoning") else "",
            "confidence": args.confidence,
        },
        "actual_result": {
            "asset": args.asset,
            "actual_change": args.actual_result,
            "time_period": args.time_period if hasattr(args, "time_period") else "",
        },
        "error_analysis": {
            "root_cause": args.root_cause,
            "missed_factors": args.missed_factors
            if hasattr(args, "missed_factors")
            else [],
            "correct_pattern": args.correct_pattern
            if hasattr(args, "correct_pattern")
            else "",
        },
        "lessons_learned": [args.lesson],
        "avoidance_strategy": args.avoidance_strategy,
    }

    return lesson_id, lesson_data


def save_lesson_file(lesson_id, lesson_data):
    """保存教训详情文件"""
    import os

    os.makedirs(LESSONS_DIR, exist_ok=True)

    file_path = os.path.join(LESSONS_DIR, f"{lesson_id}.json")
    save_json_file(file_path, lesson_data)

    return file_path


def update_lessons_index(lesson_id, lesson_data, keywords):
    """更新教训索引文件"""
    # 读取现有索引或创建新的
    index = load_json_file(LESSONS_INDEX_FILE, default=None)
    if index is None:
        index = {
            "version": "1.0",
            "last_updated": get_current_date(),
            "lessons": [],
            "categories": {
                "asset_misjudgment": "资产方向误判",
                "timing_error": "时机判断错误",
                "risk_underestimation": "风险低估",
                "pattern_misread": "模式误读",
            },
        }

    # 添加新教训
    lesson_summary = {
        "lesson_id": lesson_id,
        "date": lesson_data["date"],
        "related_crisis": lesson_data["related_crisis"],
        "keywords": keywords,
        "summary": f"判断{lesson_data['judgment']['asset']}{lesson_data['judgment']['direction']}，实际{lesson_data['actual_result']['actual_change']}。原因：{lesson_data['error_analysis']['root_cause']}",
        "lesson_category": "asset_misjudgment",
    }

    index["lessons"].append(lesson_summary)
    index["last_updated"] = get_current_date()

    save_json_file(LESSONS_INDEX_FILE, index)

    return LESSONS_INDEX_FILE


def update_links_file(lesson_id, related_crisis):
    """更新关联关系文件"""
    # 读取现有关联或创建新的
    links = load_json_file(LINKS_FILE, default=None)
    if links is None:
        links = {
            "version": "1.0",
            "last_updated": get_current_date(),
            "crisis_to_lessons": {},
            "lesson_to_crisis": {},
            "crisis_to_crisis": {},
        }

    # 更新教训到危机的关联
    if lesson_id not in links["lesson_to_crisis"]:
        links["lesson_to_crisis"][lesson_id] = []

    if related_crisis not in links["lesson_to_crisis"][lesson_id]:
        links["lesson_to_crisis"][lesson_id].append(related_crisis)

    # 更新危机到教训的关联
    if related_crisis not in links["crisis_to_lessons"]:
        links["crisis_to_lessons"][related_crisis] = []

    if lesson_id not in links["crisis_to_lessons"][related_crisis]:
        links["crisis_to_lessons"][related_crisis].append(lesson_id)

    links["last_updated"] = get_current_date()

    save_json_file(LINKS_FILE, links)

    return LINKS_FILE


def main():
    parser = argparse.ArgumentParser(description="记录学习教训")
    parser.add_argument("--related-crisis", required=True, help="相关危机事件ID")
    parser.add_argument("--asset", required=True, help="资产名称")
    parser.add_argument("--judgment", required=True, help="判断方向（上涨/下跌）")
    parser.add_argument("--confidence", type=float, required=True, help="置信度（0-1）")
    parser.add_argument(
        "--actual-result", required=True, dest="actual_result", help="实际结果"
    )
    parser.add_argument("--root-cause", required=True, help="根本原因")
    parser.add_argument("--lesson", required=True, help="教训总结")
    parser.add_argument("--avoidance-strategy", required=True, help="避免策略")
    parser.add_argument("--keywords", required=True, help="关键词（逗号分隔）")
    parser.add_argument("--reasoning", help="判断理由（可选）")
    parser.add_argument("--time-period", dest="time_period", help="时间段（可选）")
    parser.add_argument(
        "--missed-factors", dest="missed_factors", help="遗漏因素（可选，逗号分隔）"
    )
    parser.add_argument(
        "--correct-pattern", dest="correct_pattern", help="正确模式（可选）"
    )
    args = parser.parse_args()

    print(f"记录教训: {args.asset} - {args.judgment}")
    print(f"相关危机: {args.related_crisis}")

    # 解析关键词
    keywords = [k.strip() for k in args.keywords.split(",")]

    # 创建教训数据
    lesson_id, lesson_data = create_lesson_data(args)

    # 保存教训详情文件
    lesson_file_path = save_lesson_file(lesson_id, lesson_data)
    print(f"创建教训详情文件: {lesson_file_path}")

    # 更新教训索引
    index_path = update_lessons_index(lesson_id, lesson_data, keywords)
    print(f"更新教训索引: {index_path}")

    # 更新关联文件
    links_path = update_links_file(lesson_id, args.related_crisis)
    print(f"更新关联文件: {links_path}")

    print(f"教训记录完成！Lesson ID: {lesson_id}")
    return 0


if __name__ == "__main__":
    exit(main())
