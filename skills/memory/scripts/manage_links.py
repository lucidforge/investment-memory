#!/usr/bin/env python3
"""
管理危机事件、教训、规律之间的关联关系
"""

import argparse
import json
from config import (
    LINKS_FILE,
    load_json_file,
    save_json_file,
    get_current_date,
)


def load_links_file():
    """加载关联文件"""
    return load_json_file(
        LINKS_FILE,
        default={
            "version": "1.0",
            "last_updated": get_current_date(),
            "crisis_to_lessons": {},
            "lesson_to_crisis": {},
            "crisis_to_crisis": {},
        },
    )


def save_links_file(links):
    """保存关联文件"""
    links["last_updated"] = get_current_date()
    save_json_file(LINKS_FILE, links)
    return LINKS_FILE


def add_link(links, from_type, from_id, to_type, to_id):
    """添加关联关系"""
    # 根据类型确定关联键
    if from_type == "crisis" and to_type == "lesson":
        key = "crisis_to_lessons"
        reverse_key = "lesson_to_crisis"
    elif from_type == "lesson" and to_type == "crisis":
        key = "lesson_to_crisis"
        reverse_key = "crisis_to_lessons"
    elif from_type == "crisis" and to_type == "crisis":
        key = "crisis_to_crisis"
        reverse_key = "crisis_to_crisis"
    else:
        print(f"错误: 不支持的关联类型: {from_type} -> {to_type}")
        return False

    # 初始化键（如果不存在）
    if key not in links:
        links[key] = {}
    if from_id not in links[key]:
        links[key][from_id] = []

    # 添加关联（如果不存在）
    if to_id not in links[key][from_id]:
        links[key][from_id].append(to_id)
        print(f"添加关联: {from_type}.{from_id} -> {to_type}.{to_id}")

    # 添加反向关联
    if reverse_key not in links:
        links[reverse_key] = {}
    if to_id not in links[reverse_key]:
        links[reverse_key][to_id] = []

    if from_id not in links[reverse_key][to_id]:
        links[reverse_key][to_id].append(from_id)

    return True


def remove_link(links, from_type, from_id, to_type, to_id):
    """移除关联关系"""
    # 根据类型确定关联键
    if from_type == "crisis" and to_type == "lesson":
        key = "crisis_to_lessons"
        reverse_key = "lesson_to_crisis"
    elif from_type == "lesson" and to_type == "crisis":
        key = "lesson_to_crisis"
        reverse_key = "crisis_to_lessons"
    elif from_type == "crisis" and to_type == "crisis":
        key = "crisis_to_crisis"
        reverse_key = "crisis_to_crisis"
    else:
        print(f"错误: 不支持的关联类型: {from_type} -> {to_type}")
        return False

    # 移除关联
    if key in links and from_id in links[key]:
        if to_id in links[key][from_id]:
            links[key][from_id].remove(to_id)
            print(f"移除关联: {from_type}.{from_id} -> {to_type}.{to_id}")

            # 如果列表为空，删除键
            if not links[key][from_id]:
                del links[key][from_id]

    # 移除反向关联
    if reverse_key in links and to_id in links[reverse_key]:
        if from_id in links[reverse_key][to_id]:
            links[reverse_key][to_id].remove(from_id)

            # 如果列表为空，删除键
            if not links[reverse_key][to_id]:
                del links[reverse_key][to_id]

    return True


def query_links(links, query_type, query_id):
    """查询关联关系"""
    results = {"query_type": query_type, "query_id": query_id, "related_items": []}

    if query_type == "crisis":
        # 查询与危机事件相关的教训
        crisis_to_lessons = links.get("crisis_to_lessons", {})
        if query_id in crisis_to_lessons:
            for lesson_id in crisis_to_lessons[query_id]:
                results["related_items"].append({"type": "lesson", "id": lesson_id})

        # 查询相关的其他危机事件
        crisis_to_crisis = links.get("crisis_to_crisis", {})
        if query_id in crisis_to_crisis:
            for crisis_id in crisis_to_crisis[query_id]:
                results["related_items"].append({"type": "crisis", "id": crisis_id})

    elif query_type == "lesson":
        # 查询与教训相关的危机事件
        lesson_to_crisis = links.get("lesson_to_crisis", {})
        if query_id in lesson_to_crisis:
            for crisis_id in lesson_to_crisis[query_id]:
                results["related_items"].append({"type": "crisis", "id": crisis_id})

    return results


def main():
    parser = argparse.ArgumentParser(description="管理关联关系")
    parser.add_argument(
        "--action", choices=["add", "remove", "query"], required=True, help="操作类型"
    )
    parser.add_argument(
        "--from-type", choices=["crisis", "lesson", "pattern"], help="来源类型"
    )
    parser.add_argument("--from-id", help="来源ID")
    parser.add_argument(
        "--to-type", choices=["crisis", "lesson", "pattern"], help="目标类型"
    )
    parser.add_argument("--to-id", help="目标ID")
    parser.add_argument(
        "--type",
        choices=["crisis", "lesson", "pattern"],
        help="查询类型（用于query操作）",
    )
    parser.add_argument("--id", help="查询ID（用于query操作）")
    args = parser.parse_args()

    # 加载关联文件
    links = load_links_file()

    if args.action == "add":
        if not all([args.from_type, args.from_id, args.to_type, args.to_id]):
            print("错误: add操作需要指定 --from-type, --from-id, --to-type, --to-id")
            return 1

        print(
            f"管理关联关系: {args.from_type}.{args.from_id} -> {args.to_type}.{args.to_id}"
        )
        print(f"操作: {args.action}")

        success = add_link(
            links, args.from_type, args.from_id, args.to_type, args.to_id
        )
        if success:
            save_links_file(links)
            print("关联添加成功")
        else:
            print("关联添加失败")
            return 1

    elif args.action == "remove":
        if not all([args.from_type, args.from_id, args.to_type, args.to_id]):
            print("错误: remove操作需要指定 --from-type, --from-id, --to-type, --to-id")
            return 1

        print(
            f"管理关联关系: {args.from_type}.{args.from_id} -> {args.to_type}.{args.to_id}"
        )
        print(f"操作: {args.action}")

        success = remove_link(
            links, args.from_type, args.from_id, args.to_type, args.to_id
        )
        if success:
            save_links_file(links)
            print("关联移除成功")
        else:
            print("关联移除失败")
            return 1

    elif args.action == "query":
        if not all([args.type, args.id]):
            print("错误: query操作需要指定 --type, --id")
            return 1

        print(f"查询关联关系: {args.type}.{args.id}")
        print(f"操作: {args.action}")

        results = query_links(links, args.type, args.id)
        print("\n查询结果:")
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
