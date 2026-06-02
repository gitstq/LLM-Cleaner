# 🧹 LLM-Cleaner

> 智能LLM输出内容安全检测与优化工具 | Intelligent LLM Output Content Safety Detection & Sanitization

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/LLM-Cleaner?style=social)](https://github.com/gitstq/LLM-Cleaner)

---

## 🌐 语言切换 | Language

[🇨🇳 简体中文](README.md) | [🇭🇰 繁體中文](README_zh_TW.md) | [🇺🇸 English](README_en.md) | [🇯🇵 日本語](README_ja.md) | [🇰🇷 한국어](README_ko.md)

---

## 🎉 项目介绍

**LLM-Cleaner** 是一款轻量级、零依赖的 Python 库，专门用于检测和清洗 LLM（大语言模型）输出中的敏感内容。它可以帮助开发者：

- ✨ **智能检测** - 自动识别敏感词、侮辱性语言、政治敏感内容
- 🔒 **安全清洗** - 支持多种清洗策略（脱敏、替换、重写）
- 📱 **PII保护** - 自动检测并保护个人身份信息（邮箱、电话、身份证等）
- 🛡️ **有害内容过滤** - 过滤自杀指导、犯罪指导等有害内容
- 🔌 **易于集成** - 简洁的 API，几行代码即可接入

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🧹 **敏感词检测** | 内置敏感词库，支持自定义扩展 |
| 🏛️ **政治内容检测** | 检测政治敏感话题（仅合规用途） |
| ⚠️ **有害内容过滤** | 过滤自杀、犯罪指导等有害内容 |
| 🔐 **PII 脱敏** | 自动检测邮箱、电话、身份证等 |
| 🔄 **多种清洗策略** | 脱敏、替换、重写、部分脱敏 |
| ⚡ **零依赖设计** | 仅依赖 Python 标准库 |
| 🚀 **高性能** | 处理速度 < 10ms/千字符 |
| 📦 **开箱即用** | 无需复杂配置 |

---

## 🚀 快速开始

### 📥 安装

```bash
# 使用 pip 安装
pip install llm-cleaner

# 或从源码安装
git clone https://github.com/gitstq/LLM-Cleaner.git
cd LLM-Cleaner
pip install -e .
```

### 💡 基础使用

```python
from llm_cleaner import LLMCleaner
from llm_cleaner.detectors import SensitiveWordDetector, PIIDetector
from llm_cleaner.sanitizers import RedactSanitizer

# 创建清洗器
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),  # 敏感词检测
        PIIDetector()            # PII 检测
    ],
    sanitizer=RedactSanitizer()  # 脱敏清洗
)

# 检测并清洗文本
text = "你是个白痴！联系我: test@example.com"
result = cleaner.clean(text)

print(result.cleaned_text)  # 你是个[REDACTED]！联系我: [REDACTED]
print(result.is_safe)      # True
```

### 🖥️ 命令行使用

```bash
# 检测敏感内容
echo "你是个白痴" | python -m llm_cleaner detect

# 检测并清洗
echo "你是个白痴" | python -m llm_cleaner clean

# 使用所有检测器
python -m llm_cleaner clean --detect-all

# 交互式模式
python -m llm_cleaner interactive
```

---

## 📖 详细使用指南

### 🎛️ 选择检测器

LLM-Cleaner 提供了多种内置检测器，可以根据需求组合使用：

```python
from llm_cleaner.detectors import (
    SensitiveWordDetector,      # 敏感词检测
    PoliticalContentDetector,   # 政治敏感内容
    HarmfulContentDetector,     # 有害内容
    PIIDetector                # 个人身份信息
)

# 组合使用
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),
        PoliticalContentDetector(),
        HarmfulContentDetector(),
        PIIDetector()
    ]
)
```

### 🔧 选择清洗策略

```python
from llm_cleaner.sanitizers import (
    RedactSanitizer,          # 完全脱敏 [REDACTED]
    ReplaceSanitizer,         # 替换为安全词
    RewriteSanitizer,         # 重写为提示语
    PartialRedactSanitizer    # 部分脱敏 138****5678
)

# 使用脱敏清洗器
cleaner.set_sanitizer(RedactSanitizer())

# 使用替换清洗器
cleaner.set_sanitizer(ReplaceSanitizer())

# 使用部分脱敏（保留部分可见）
cleaner.set_sanitizer(PartialRedactSanitizer(visible_chars=3))
```

### 🎨 自定义敏感词

```python
# 添加自定义敏感词
detector = SensitiveWordDetector(
    custom_words={"自定义词1", "自定义词2"},
    sensitivity=0.9  # 敏感度 0.0-1.0
)

# 添加自定义正则模式
cleaner.add_custom_pattern(
    pattern=r"违禁词汇\d+号",
    pattern_name="custom_banned",
    risk_level="high",
    category="custom"
)
```

### 🔌 集成到 LLM 调用流程

```python
# 在 LLM 响应后处理
def process_llm_response(response_text: str):
    result = cleaner.clean(response_text)
    
    if not result.is_safe:
        print("⚠️ 内容未通过安全检测")
        return result.cleaned_text
    
    return response_text
```

---

## 💡 设计思路

### 🎯 设计理念

1. **零依赖原则** - 仅使用 Python 标准库，确保在任何环境下都能运行
2. **模块化设计** - 检测器和清洗器解耦，方便扩展
3. **高性能优先** - 使用预编译正则表达式，处理速度快
4. **合规优先** - 所有检测仅用于合规目的，不涉及任何敏感话题

### 🛠️ 技术选型

| 技术 | 选择原因 |
|------|---------|
| Python re 模块 | 标准库，无需额外依赖 |
| 正则表达式 | 高效的文本模式匹配 |
| 数据类 | 清晰的结果结构 |
| 枚举类型 | 明确的风险等级定义 |

### 📋 风险等级

| 等级 | 说明 | 示例 |
|------|------|------|
| 🟢 SAFE | 安全 | 正常文本 |
| 🟡 LOW | 低风险 | 一般敏感词 |
| 🟠 MEDIUM | 中等风险 | 侮辱性词汇 |
| 🔴 HIGH | 高风险 | 严重敏感词 |
| 🚨 CRITICAL | 极高风险 | 犯罪指导 |

---

## 📦 打包与部署

### 🐳 Docker 使用

```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install llm-cleaner
CMD ["python", "-m", "llm_cleaner", "interactive"]
```

### ☁️ 在 LLM 服务中使用

```python
# OpenAI API 示例
from openai import OpenAI

client = OpenAI()
cleaner = LLMCleaner(...)
sanitizer = RedactSanitizer()

def safe_chat(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw_response = response.choices[0].message.content
    result = cleaner.clean(raw_response)
    
    return result.cleaned_text
```

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. **Fork 本仓库**
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'feat: 添加新特性'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 🐛 问题反馈

如发现问题，请提交 [Issue](https://github.com/gitstq/LLM-Cleaner/issues)。

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源。

---

## 🙏 致谢

- 灵感来源：[heretic](https://github.com/p-e-w/heretic) - LLM 审查移除工具
- 所有贡献者

---

<div align="center">

**如果这个项目对您有帮助，请给个 ⭐️！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
