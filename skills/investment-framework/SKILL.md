---
name: investment-framework
description: 投资决策框架skill。当用户提到"估值"、"仓位"、"风险评估"、"投资决策"、"买入时机"、"止损"、"止盈"等操作时自动触发。提供估值检查、仓位计算和风险评估工具。
---

# Investment Framework Skill - 投资决策框架

提供结构化的投资决策工具，帮助评估投资机会的风险和收益。

## 核心功能

| 功能 | 说明 | 脚本 |
|------|------|------|
| 估值检查 | 检查资产估值是否合理 | `check_valuation.py` |
| 仓位计算 | 根据风险等级计算建议仓位 | `position_sizing.py` |
| 风险评估 | 评估投资机会的综合风险 | `risk_assessment.py` |

## 投资决策框架

### 1. 估值检查清单

**PE/PB历史分位数：**
- 0-20%：低估区域，可考虑加仓
- 20-50%：合理偏低，可持有
- 50-80%：合理偏高，谨慎
- 80-100%：高估区域，考虑减仓

**同行业对比：**
- 相对估值是否偏离行业平均
- 增长率是否匹配估值水平

**增长率匹配度：**
- PEG < 1：可能低估
- PEG 1-2：合理估值
- PEG > 2：可能高估

### 2. 仓位管理框架

**凯利公式简化版：**
```
仓位比例 = (胜率 × 赔率 - 败率) / 赔率
```

**风险等级对应仓位：**
- 极高风险：5%以内
- 高风险：5-10%
- 中等风险：10-20%
- 低风险：20-30%

**分散化原则：**
- 单只股票仓位不超过20%
- 单个行业仓位不超过30%
- 保持10-20%现金

### 3. 风险评估矩阵

| 风险类型 | 评估维度 | 权重 |
|----------|----------|------|
| 市场风险 | 行业周期、估值水平 | 25% |
| 公司风险 | 业绩稳定性、竞争格局 | 25% |
| 流动性风险 | 交易量、市值 | 20% |
| 政策风险 | 行业政策、监管环境 | 15% |
| 技术风险 | 技术路线、替代风险 | 15% |

## 快速开始

### 1. 检查估值

```bash
uv run python skills/investment-framework/scripts/check_valuation.py \
  --code "HK.00700" \
  --pe 15 \
  --industry-pe 20 \
  --growth-rate 25
```

### 2. 计算仓位

```bash
uv run python skills/investment-framework/scripts/position_sizing.py \
  --risk-level "medium" \
  --win-rate 0.6 \
  --risk-reward 2 \
  --total-capital 100000
```

### 3. 风险评估

```bash
uv run python skills/investment-framework/scripts/risk_assessment.py \
  --code "HK.00700" \
  --industry "互联网" \
  --market-cap 30000 \
  --daily-volume 100
```

## 使用场景

### 场景1：分析一只股票是否值得买入

```
用户：腾讯现在能买吗？
智能体：1. 调用 check_valuation.py 检查估值
        2. 调用 risk_assessment.py 评估风险
        3. 调用 position_sizing.py 计算建议仓位
        4. 综合给出投资建议
```

### 场景2：决定止损止盈点位

```
用户：我持有腾讯，成本价350，现在500了，该止盈吗？
智能体：1. 分析当前估值水平
        2. 评估上涨空间和下跌风险
        3. 给出分批止盈建议
```

### 场景3：评估新发现的投资机会

```
用户：我发现固态电池技术突破，想投资相关股票
智能体：1. 调用 trend-knowledge 分析趋势阶段
        2. 调用 risk_assessment.py 评估综合风险
        3. 调用 position_sizing.py 计算建议仓位
```

## 最佳实践

1. **先估值后仓位**：先检查估值是否合理，再决定仓位大小
2. **分散投资**：不要把所有资金放在一个篮子里
3. **定期复盘**：定期检查持仓的估值和风险变化
4. **设置止损**：根据风险等级设置合理的止损点位

## 相关Skill

- **memory**: 记忆管理skill，记录投资操作和教训
- **trend-knowledge**: 产业趋势知识，提供行业周期判断
- **crisis-knowledge-maintainer**: 危机知识维护skill
