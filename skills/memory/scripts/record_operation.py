#!/usr/bin/env python3
"""
记录操作到记忆文件

功能：记录每次OpenAPI调用和分析操作
用法：python record_operation.py --type "quote" --details '{"code": "HK.00700"}' --result '{"price": 350.5}'
"""

import argparse
import json
import sys
from config import (
    OPERATIONS_FILE,
    load_json_file,
    save_json_file,
    generate_id,
    get_current_datetime,
)


def record_operation(operation_type, details, result, code=None, output_json=False):
    """
    记录操作到记忆文件

    Args:
        operation_type: 操作类型（quote/trade/analysis等）
        details: 操作详情（JSON字符串或字典）
        result: 操作结果（JSON字符串或字典）
        code: 股票代码（可选）
        output_json: 是否输出JSON格式

    Returns:
        记录的条目
    """
    # 解析details和result
    if isinstance(details, str):
        try:
            details = json.loads(details)
        except json.JSONDecodeError:
            details = {"raw": details}

    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            result = {"raw": result}

    # 从details中提取code（如果未提供）
    if code is None and isinstance(details, dict):
        code = details.get("code") or details.get("stock_code")

    # 创建记录
    record = {
        "id": generate_id(),
        "timestamp": get_current_datetime(),
        "type": operation_type,
        "code": code,
        "details": details,
        "result": result,
    }

    # 加载现有记录
    operations = load_json_file(OPERATIONS_FILE, default=[])

    # 添加新记录
    operations.append(record)

    # 保存记录
    save_json_file(OPERATIONS_FILE, operations)

    # 输出结果
    if output_json:
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        print(f"操作已记录")
        print(f"  ID: {record['id']}")
        print(f"  时间: {record['timestamp']}")
        print(f"  类型: {record['type']}")
        if record["code"]:
            print(f"  代码: {record['code']}")

    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="记录操作到记忆文件")
    parser.add_argument(
        "--type", required=True, help="操作类型（quote/trade/analysis等）"
    )
    parser.add_argument("--details", required=True, help="操作详情（JSON字符串）")
    parser.add_argument("--result", required=True, help="操作结果（JSON字符串）")
    parser.add_argument("--code", help="股票代码（可选）")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )

    args = parser.parse_args()

    record_operation(
        operation_type=args.type,
        details=args.details,
        result=args.result,
        code=args.code,
        output_json=args.output_json,
    )
