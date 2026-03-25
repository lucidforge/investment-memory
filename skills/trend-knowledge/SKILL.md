---
name: trend-knowledge
description: 产业趋势知识管理skill。当用户提到"行业趋势"、"增长点"、"新兴产业"、"行业周期"、"渗透率"、"产业生命周期"等操作时自动触发。支持自然语言触发，提供趋势分析和生命周期判断。
---

# Trend Knowledge Skill - 产业趋势知识管理

管理产业趋势知识，支持趋势查询、生命周期判断和投资时机分析。

## 核心功能

| 功能 | 说明 | 脚本 |
|------|------|------|
| 添加趋势 | 添加新的产业趋势到知识库 | `add_trend.py` |
| 更新趋势 | 更新趋势的阶段和信息 | `update_trend.py` |
| 查询趋势信号 | 根据当前形势查询相关趋势 | `get_trend_signal.py` |
| 分析趋势健康度 | 评估趋势的投资价值 | `analyze_trend.py` |
| 列出所有趋势 | 显示所有已收录的趋势 | `list_trends.py` |

## 产业生命周期

### 阶段定义

| 阶段 | 特征 | 投资策略 | 风险等级 |
|------|------|----------|----------|
| 萌芽期 | 技术验证，商业化早期 | 小仓位试探，关注技术突破 | 极高 |
| 成长期 | 渗透率快速提升，业绩高增长 | 重仓龙头，长期持有 | 中高 |
| 成熟期 | 增速放缓，行业洗牌 | 关注龙头，估值合理时介入 | 中等 |
| 衰退期 | 需求下降，产能过剩 | 回避或做空 | 高 |

### 关键指标

**萌芽期判断：**
- 技术突破（如ChatGPT发布）
- 政策支持（如双碳目标）
- 资本涌入（如VC投资热潮）

**成长期判断：**
- 渗透率突破10%
- 龙头企业业绩高增长
- 行业标准逐步确立

**成熟期判断：**
- 渗透率超过40%
- 增速放缓至20%以下
- 行业集中度提升

**衰退期判断：**
- 需求下降或替代品出现
- 产能过剩，价格战
- 企业开始退出

## 快速开始

### 1. 查询相关趋势

```bash
uv run python skills/trend-knowledge/scripts/get_trend_signal.py \
  --situation "当前AI概念很火，英伟达股价大涨"
```

### 2. 分析趋势健康度

```bash
uv run python skills/trend-knowledge/scripts/analyze_trend.py \
  --trend-id TREND_2023_AI
```

### 3. 添加新趋势

```bash
uv run python skills/trend-knowledge/scripts/add_trend.py \
  --trend-id "TREND_2025_NEW" \
  --trend-name "新趋势名称" \
  --start-year 2025 \
  --keywords "关键词1,关键词2" \
  --trigger-event "触发事件描述"
```

## 使用场景

### 场景1：分析当前市场热点是否值得投资

```
用户：最近AI很火，英伟达涨了很多，现在还能买吗？
智能体：1. 调用 get_trend_signal.py 查询AI趋势
        2. 调用 analyze_trend.py 分析趋势健康度
        3. 基于生命周期阶段给出投资建议
```

### 场景2：判断新兴产业的投资时机

```
用户：量子计算现在处于什么阶段？值得投资吗？
智能体：1. 调用 get_trend_signal.py 查询量子计算趋势
        2. 分析当前阶段和关键指标
        3. 给出投资时机建议
```

### 场景3：记录新发现的产业趋势

```
用户：我发现固态电池技术突破，可能是下一个大趋势
智能体：1. 调用 add_trend.py 添加新趋势
        2. 记录关键信息和触发事件
        3. 设置初始阶段为萌芽期
```

## 数据结构

### 趋势索引

```json
{
  "trend_id": "TREND_2023_AI",
  "trend_name": "AI/大模型革命",
  "start_year": 2023,
  "current_phase": "growth",
  "keywords": ["人工智能", "大模型", "ChatGPT"],
  "trigger_event": "ChatGPT发布",
  "affected_markets": ["美股", "A股", "港股"],
  "key_assets": ["算力芯片", "大模型", "AI应用"],
  "summary": "简短摘要..."
}
```

### 趋势详情

```json
{
  "trend_id": "TREND_2023_AI",
  "trend_name": "AI/大模型革命",
  "basic_info": {...},
  "trend_details": "详细描述...",
  "market_impact": {...},
  "investment_opportunities": {...},
  "lessons": [...],
  "current_status": {...}
}
```

## 最佳实践

1. **生命周期判断**：分析趋势时首先判断当前所处阶段
2. **关键指标验证**：使用渗透率、增速等指标验证阶段判断
3. **教训学习**：关注类似趋势的历史教训（如元宇宙泡沫）
4. **定期更新**：趋势阶段会变化，定期更新状态

## 相关Skill

- **memory**: 记忆管理skill，记录投资操作和教训
- **crisis-knowledge-maintainer**: 危机知识维护skill
- **investment-framework**: 投资决策框架skill
