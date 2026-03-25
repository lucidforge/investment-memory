#!/usr/bin/env python3
"""
生成操作总结报告

功能：按时间段生成操作总结
用法：python summarize.py --period "today"
"""

import argparse
import json
from datetime import datetime, timedelta
from collections import Counter
from config import (
    OPERATIONS_FILE,
    CONCLUSIONS_FILE,
    PORTFOLIO_FILE,
    load_json_file,
)


def get_date_range(period, start_date=None, end_date=None):
    """获取日期范围"""
    today = datetime.now().date()

    if period == "today":
        return today.isoformat(), today.isoformat()
    elif period == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday.isoformat(), yesterday.isoformat()
    elif period == "week":
        week_start = today - timedelta(days=today.weekday())
        return week_start.isoformat(), today.isoformat()
    elif period == "month":
        month_start = today.replace(day=1)
        return month_start.isoformat(), today.isoformat()
    elif start_date and end_date:
        return start_date, end_date
    else:
        return None, None


def summarize(period=None, start_date=None, end_date=None, output_json=False):
    """
    生成操作总结报告

    Args:
        period: 时间段（today/yesterday/week/month）
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）
        output_json: 是否输出JSON格式

    Returns:
        总结报告字典
    """
    # 获取日期范围
    start, end = get_date_range(period, start_date, end_date)

    # 加载数据
    operations = load_json_file(OPERATIONS_FILE, default=[])
    conclusions = load_json_file(CONCLUSIONS_FILE, default=[])
    portfolio = load_json_file(PORTFOLIO_FILE, default={})

    # 过滤日期范围内的记录
    filtered_ops = []
    filtered_concs = []

    for op in operations:
        op_date = datetime.fromisoformat(op["timestamp"]).date().isoformat()
        if start and end and start <= op_date <= end:
            filtered_ops.append(op)
        elif not start and not end:
            filtered_ops.append(op)

    for conc in conclusions:
        conc_date = datetime.fromisoformat(conc["timestamp"]).date().isoformat()
        if start and end and start <= conc_date <= end:
            filtered_concs.append(conc)
        elif not start and not end:
            filtered_concs.append(conc)

    # 统计操作类型
    type_counter = Counter(op.get("type", "unknown") for op in filtered_ops)

    # 统计涉及的股票
    code_counter = Counter(op.get("code") for op in filtered_ops if op.get("code"))

    # 统计投资建议
    rec_counter = Counter(conc.get("recommendation") for conc in filtered_concs)

    # 创建总结报告
    summary = {
        "period": {"type": period or "custom", "start": start, "end": end},
        "operations": {
            "total": len(filtered_ops),
            "by_type": dict(type_counter),
            "by_code": dict(code_counter.most_common(10)),
        },
        "conclusions": {
            "total": len(filtered_concs),
            "by_recommendation": dict(rec_counter),
        },
        "portfolio": {
            "total_positions": len(portfolio),
            "positions": list(portfolio.keys()),
        },
    }

    # 输出结果
    if output_json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("操作总结报告")
        print("=" * 70)

        if start and end:
            print(f"\n时间范围: {start} 至 {end}")
        else:
            print(f"\n时间范围: 全部")

        print(f"\n操作统计:")
        print(f"  总操作数: {summary['operations']['total']}")
        if type_counter:
            print(f"  按类型:")
            for op_type, count in type_counter.most_common():
                print(f"    - {op_type}: {count}")

        if code_counter:
            print(f"\n涉及股票:")
            for code, count in code_counter.most_common(5):
                print(f"    - {code}: {count}次")

        print(f"\n分析结论:")
        print(f"  总结论数: {summary['conclusions']['total']}")
        if rec_counter:
            print(f"  按建议:")
            for rec, count in rec_counter.most_common():
                print(f"    - {rec}: {count}")

        print(f"\n投资组合:")
        print(f"  持仓数量: {summary['portfolio']['total_positions']}")
        if portfolio:
            print(f"  持仓股票:")
            for code, pos in portfolio.items():
                print(f"    - {code}: {pos['quantity']}股")

        print("\n" + "=" * 70)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成操作总结报告")
    parser.add_argument(
        "--period", choices=["today", "yesterday", "week", "month"], help="时间段"
    )
    parser.add_argument("--start", dest="start_date", help="开始日期（YYYY-MM-DD）")
    parser.add_argument("--end", dest="end_date", help="结束日期（YYYY-MM-DD）")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )

    args = parser.parse_args()

    if not args.period and not (args.start_date and args.end_date):
        args.period = "today"

    summarize(
        period=args.period,
        start_date=args.start_date,
        end_date=args.end_date,
        output_json=args.output_json,
    )
