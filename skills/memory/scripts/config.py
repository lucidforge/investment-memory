#!/usr/bin/env python3
"""
统一配置文件 - 定义常量和辅助函数
"""

import os
import json
from datetime import datetime


# 目录和文件配置
MEMORY_DIR = ".memory"
CRISIS_KNOWLEDGE_DIR = os.path.join(MEMORY_DIR, "crisis_knowledge")
CRISIS_EVENTS_DIR = os.path.join(CRISIS_KNOWLEDGE_DIR, "events")
LESSONS_DIR = os.path.join(MEMORY_DIR, "lessons_learned", "lessons")

OPERATIONS_FILE = os.path.join(MEMORY_DIR, "operations.json")
CONCLUSIONS_FILE = os.path.join(MEMORY_DIR, "conclusions.json")
PORTFOLIO_FILE = os.path.join(MEMORY_DIR, "portfolio.json")
CRISIS_INDEX_FILE = os.path.join(CRISIS_KNOWLEDGE_DIR, "index.json")
LESSONS_INDEX_FILE = os.path.join(LESSONS_DIR, "index.json")
PATTERNS_FILE = os.path.join(MEMORY_DIR, "investment_patterns.json")
LINKS_FILE = os.path.join(MEMORY_DIR, "links.json")


def ensure_memory_dir():
    """确保记忆目录存在"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    os.makedirs(CRISIS_EVENTS_DIR, exist_ok=True)
    os.makedirs(LESSONS_DIR, exist_ok=True)


def load_json_file(file_path, default=None):
    """统一的JSON文件加载函数"""
    if default is None:
        default = []

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
    ensure_memory_dir()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"错误: 保存文件失败 {file_path}: {e}")
        return False


def generate_id(prefix=""):
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if prefix:
        return f"{prefix}_{timestamp}"
    return timestamp


def get_current_date():
    """获取当前日期字符串"""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_datetime():
    """获取当前日期时间字符串"""
    return datetime.now().isoformat()
