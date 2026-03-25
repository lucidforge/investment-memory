#!/usr/bin/env python3
"""
添加新的产业趋势到知识库
"""

import argparse
import json
import os
from datetime import datetime

# 使用相对路径，从项目根目录执行
MEMORY_DIR = ".memory"
TRENDS_DIR = os.path.join(MEMORY_DIR, "industry_trends", "trends")
TRENDS_INDEX_FILE = os.path.join(MEMORY_DIR, "industry_trends", "index.json")


def ensure_dirs():
    """确保目录存在"""
    os.makedirs(TRENDS_DIR, exist_ok=True)


def load_json_file(file_path, default=None):
    """统一的JSON文件加载函数"""
    if default is None:
        default = {}

    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return default


def save_json_file(file_path, data):
    """统一的JSON文件保存函数"""
    ensure_dirs()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"错误: 保存文件失败 {file_path}: {e}")
        return False


def create_trend_template(args):
    """创建趋势模板"""
    trend_data = {
        "trend_id": args.trend_id,
        "trend_name": args.trend_name,
        "basic_info": {
            "start_year": args.start_year,
            "current_phase": args.phase if hasattr(args, "phase") else "emerging",
            "trigger_event": args.trigger_event,
            "keywords": [k.strip() for k in args.keywords.split(",")],
        },
        "trend_details": "",
        "market_impact": {
            "us_stock": {"content": ""},
            "hk_stock": {"content": ""},
            "a_stock": {"content": ""},
        },
        "investment_opportunities": {
            "short_term": [],
            "medium_term": [],
            "long_term": [],
        },
        "lessons": [],
        "current_status": {
            "phase": args.phase if hasattr(args, "phase") else "emerging",
            "key_watch": [],
            "risk_factors": [],
        },
    }

    return trend_data


def save_trend_file(trend_id, trend_data):
    """保存趋势详情文件"""
    ensure_dirs()
    file_path = os.path.join(TRENDS_DIR, f"{trend_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(trend_data, f, ensure_ascii=False, indent=2)

    return file_path


def add_trend_to_index(
    trend_id, trend_name, start_year, phase, keywords, trigger_event
):
    """添加趋势到索引"""
    ensure_dirs()

    # 读取现有索引或创建新的
    if os.path.exists(TRENDS_INDEX_FILE):
        with open(TRENDS_INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {
            "version": "1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "trends": [],
        }

    # 创建索引条目
    index_trend = {
        "trend_id": trend_id,
        "trend_name": trend_name,
        "start_year": start_year,
        "current_phase": phase,
        "keywords": keywords,
        "trigger_event": trigger_event,
        "affected_markets": [],
        "key_assets": [],
        "summary": "",
    }

    # 添加到索引
    index["trends"].append(index_trend)
    index["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # 保存索引
    with open(TRENDS_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return TRENDS_INDEX_FILE


def main():
    parser = argparse.ArgumentParser(description="添加新的产业趋势")
    parser.add_argument(
        "--trend-id", required=True, help="趋势ID（格式：TREND_YYYY_NAME）"
    )
    parser.add_argument("--trend-name", required=True, help="趋势名称")
    parser.add_argument("--start-year", type=int, required=True, help="开始年份")
    parser.add_argument("--keywords", required=True, help="关键词（逗号分隔）")
    parser.add_argument("--trigger-event", required=True, help="触发事件描述")
    parser.add_argument(
        "--phase",
        choices=["emerging", "growth", "mature", "decline"],
        default="emerging",
        help="当前阶段（默认：emerging）",
    )
    args = parser.parse_args()

    print(f"添加新的产业趋势: {args.trend_id}")
    print(f"趋势名称: {args.trend_name}")
    print(f"开始年份: {args.start_year}")
    print(f"当前阶段: {args.phase}")

    # 创建趋势模板
    trend_data = create_trend_template(args)

    # 保存趋势详情文件
    trend_file_path = save_trend_file(args.trend_id, trend_data)
    print(f"创建趋势详情文件: {trend_file_path}")

    # 添加到索引
    keywords_list = [k.strip() for k in args.keywords.split(",")]
    index_path = add_trend_to_index(
        args.trend_id,
        args.trend_name,
        args.start_year,
        args.phase,
        keywords_list,
        args.trigger_event,
    )
    print(f"更新索引文件: {index_path}")

    print(f"\n产业趋势添加成功！")
    print(f"下一步：请填充以下内容：")
    print(f"  1. 趋势详情 (trend_details)")
    print(f"  2. 市场影响分析 (market_impact)")
    print(f"  3. 投资机会分析 (investment_opportunities)")
    print(f"  4. 历史教训 (lessons)")

    return 0


if __name__ == "__main__":
    exit(main())
