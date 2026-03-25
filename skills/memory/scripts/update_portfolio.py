#!/usr/bin/env python3
"""
更新投资组合

功能：管理持仓信息
用法：python update_portfolio.py --action "add" --code "HK.00700" --quantity 100 --price 350.5
"""

import argparse
import json
import sys
from config import (
    PORTFOLIO_FILE,
    load_json_file,
    save_json_file,
    get_current_datetime,
)


def update_portfolio(action, code, quantity=None, price=None, output_json=False):
    """
    更新投资组合

    Args:
        action: 操作类型（add/update/remove）
        code: 股票代码
        quantity: 数量（add/update时必填）
        price: 价格（add时必填）
        output_json: 是否输出JSON格式

    Returns:
        更新后的持仓信息
    """
    # 验证action
    valid_actions = ["add", "update", "remove"]
    if action not in valid_actions:
        print(f"错误: 无效的操作 '{action}'，有效值: {', '.join(valid_actions)}")
        sys.exit(1)

    # 加载投资组合
    portfolio = load_json_file(PORTFOLIO_FILE, default={})

    if action == "add":
        if quantity is None or price is None:
            print("错误: 添加持仓需要指定 --quantity 和 --price")
            sys.exit(1)

        # 添加或更新持仓
        portfolio[code] = {
            "quantity": quantity,
            "avg_price": price,
            "total_cost": quantity * price,
            "added_at": get_current_datetime(),
            "updated_at": get_current_datetime(),
        }
        message = f"已添加持仓: {code}"

    elif action == "update":
        if quantity is None:
            print("错误: 更新持仓需要指定 --quantity")
            sys.exit(1)

        if code not in portfolio:
            print(f"错误: 未找到 {code} 的持仓记录")
            sys.exit(1)

        # 更新持仓数量
        portfolio[code]["quantity"] = quantity
        portfolio[code]["updated_at"] = get_current_datetime()
        message = f"已更新持仓: {code}"

    elif action == "remove":
        if code not in portfolio:
            print(f"错误: 未找到 {code} 的持仓记录")
            sys.exit(1)

        # 删除持仓
        del portfolio[code]
        message = f"已删除持仓: {code}"

    # 保存投资组合
    save_json_file(PORTFOLIO_FILE, portfolio)

    # 输出结果
    if output_json:
        result = {"action": action, "code": code, "portfolio": portfolio}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(message)
        if action != "remove" and code in portfolio:
            pos = portfolio[code]
            print(f"  数量: {pos['quantity']}")
            print(f"  均价: {pos['avg_price']}")
            print(f"  总成本: {pos['total_cost']}")

    return portfolio.get(code) if action != "remove" else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新投资组合")
    parser.add_argument(
        "--action", required=True, choices=["add", "update", "remove"], help="操作类型"
    )
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--quantity", type=int, help="数量")
    parser.add_argument("--price", type=float, help="价格")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )

    args = parser.parse_args()

    update_portfolio(
        action=args.action,
        code=args.code,
        quantity=args.quantity,
        price=args.price,
        output_json=args.output_json,
    )
