#!/usr/bin/env python3
"""
查询操作历史

功能：按时间、类型、股票代码查询历史记录
用法：python get_history.py --type "quote" --code "HK.00700" --limit 10
"""

import argparse
import json
from datetime import datetime
from config import OPERATIONS_FILE, load_json_file


def get_history(
    operation_type=None,
    code=None,
    limit=None,
    start_date=None,
    end_date=None,
    output_json=False,
):
    """
    查询操作历史

    Args:
        operation_type: 操作类型过滤
        code: 股票代码过滤
        limit: 返回记录数量限制
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）
        output_json: 是否输出JSON格式

    Returns:
        过滤后的操作记录列表
    """
    operations = load_json_file(OPERATIONS_FILE, default=[])

    # 过滤记录
    filtered = []
    for op in operations:
        # 类型过滤
        if operation_type and op.get("type") != operation_type:
            continue

        # 代码过滤
        if code and op.get("code") != code:
            continue

        # 日期过滤
        if start_date or end_date:
            op_time = datetime.fromisoformat(op["timestamp"])
            op_date = op_time.strftime("%Y-%m-%d")

            if start_date and op_date < start_date:
                continue
            if end_date and op_date > end_date:
                continue

        filtered.append(op)

    # 按时间倒序排序（最新的在前）
    filtered.sort(key=lambda x: x["timestamp"], reverse=True)

    # 限制数量
    if limit and limit > 0:
        filtered = filtered[:limit]

    # 输出结果
    if output_json:
        print(json.dumps(filtered, ensure_ascii=False, indent=2))
    else:
        if not filtered:
            print("未找到匹配的记录")
            return filtered

        print(f"找到 {len(filtered)} 条记录:")
        print("=" * 70)

        for i, op in enumerate(filtered, 1):
            timestamp = op["timestamp"][:19].replace("T", " ")
            print(f"\n{i}. [{op.get('type', 'N/A')}] {timestamp}")
            if op.get("code"):
                print(f"   代码: {op['code']}")
            print(f"   详情: {json.dumps(op.get('details', {}), ensure_ascii=False)}")
            print(f"   结果: {json.dumps(op.get('result', {}), ensure_ascii=False)}")

        print("\n" + "=" * 70)

    return filtered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询操作历史")
    parser.add_argument("--type", dest="operation_type", help="操作类型过滤")
    parser.add_argument("--code", help="股票代码过滤")
    parser.add_argument("--limit", type=int, help="返回记录数量限制")
    parser.add_argument("--start", dest="start_date", help="开始日期（YYYY-MM-DD）")
    parser.add_argument("--end", dest="end_date", help="结束日期（YYYY-MM-DD）")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )

    args = parser.parse_args()

    get_history(
        operation_type=args.operation_type,
        code=args.code,
        limit=args.limit,
        start_date=args.start_date,
        end_date=args.end_date,
        output_json=args.output_json,
    )
