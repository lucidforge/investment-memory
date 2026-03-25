#!/usr/bin/env python3
"""
查询分析结论

功能：查询保存的分析结论
用法：python get_conclusion.py --code "HK.00700"
"""

import argparse
import json
from datetime import datetime
from config import CONCLUSIONS_FILE, load_json_file


def get_conclusion(code=None, limit=None, output_json=False):
    """
    查询分析结论

    Args:
        code: 股票代码过滤
        limit: 返回记录数量限制
        output_json: 是否输出JSON格式

    Returns:
        过滤后的结论记录列表
    """
    conclusions = load_json_file(CONCLUSIONS_FILE, default=[])

    # 过滤记录
    filtered = []
    for conc in conclusions:
        # 代码过滤
        if code and conc.get("code") != code:
            continue
        filtered.append(conc)

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
            print("未找到匹配的结论")
            return filtered

        print(f"找到 {len(filtered)} 条结论:")
        print("=" * 70)

        for i, conc in enumerate(filtered, 1):
            timestamp = conc["timestamp"][:19].replace("T", " ")
            print(f"\n{i}. {conc['code']} - {timestamp}")
            print(f"   建议: {conc['recommendation']}")
            if conc.get("confidence"):
                print(f"   置信度: {conc['confidence'] * 100:.1f}%")
            print(f"   分析: {conc['analysis']}")
            if conc.get("target_price"):
                print(f"   目标价: {conc['target_price']}")
            if conc.get("stop_loss"):
                print(f"   止损价: {conc['stop_loss']}")

        print("\n" + "=" * 70)

    return filtered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询分析结论")
    parser.add_argument("--code", help="股票代码过滤")
    parser.add_argument("--limit", type=int, help="返回记录数量限制")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )

    args = parser.parse_args()

    get_conclusion(code=args.code, limit=args.limit, output_json=args.output_json)
