# 🧹 LLM-Cleaner

> 智慧LLM輸出內容安全檢測與優化工具 | Intelligent LLM Output Content Safety Detection & Sanitization

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/LLM-Cleaner?style=social)](https://github.com/gitstq/LLM-Cleaner)

---

## 🌐 語言切換 | Language

[🇨🇳 简体中文](README.md) | [🇭🇰 繁體中文](README_zh_TW.md) | [🇺🇸 English](README_en.md) | [🇯🇵 日本語](README_ja.md) | [🇰🇷 한국어](README_ko.md)

---

## 🎉 專案介紹

**LLM-Cleaner** 是一款輕量級、零依賴的 Python 庫，專門用於檢測和清洗 LLM（大語言模型）輸出中的敏感內容。它可以幫助開發者：

- ✨ **智慧檢測** - 自動識別敏感詞、侮辱性語言、政治敏感內容
- 🔒 **安全清洗** - 支援多種清洗策略（脫敏、替換、重寫）
- 📱 **PII保護** - 自動檢測並保護個人身份資訊（郵箱、電話、身份證等）
- 🛡️ **有害內容過濾** - 過濾自殺指導、犯罪指導等有害內容
- 🔌 **易於集成** - 簡潔的 API，幾行程式碼即可接入

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🧹 **敏感詞檢測** | 內建敏感詞庫，支援自訂擴展 |
| 🏛️ **政治內容檢測** | 檢測政治敏感話題（僅合規用途） |
| ⚠️ **有害內容過濾** | 過濾自殺、犯罪指導等有害內容 |
| 🔐 **PII 脫敏** | 自動檢測郵箱、電話、身份證等 |
| 🔄 **多種清洗策略** | 脫敏、替換、重寫、部分脫敏 |
| ⚡ **零依賴設計** | 僅依賴 Python 標準庫 |
| 🚀 **高性能** | 處理速度 < 10ms/千字符 |
| 📦 **開箱即用** | 無需複雜配置 |

---

## 🚀 快速開始

### 📥 安裝

```bash
# 使用 pip 安裝
pip install llm-cleaner

# 或從原始碼安裝
git clone https://github.com/gitstq/LLM-Cleaner.git
cd LLM-Cleaner
pip install -e .
```

### 💡 基礎使用

```python
from llm_cleaner import LLMCleaner
from llm_cleaner.detectors import SensitiveWordDetector, PIIDetector
from llm_cleaner.sanitizers import RedactSanitizer

# 創建清洗器
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),  # 敏感詞檢測
        PIIDetector()            # PII 檢測
    ],
    sanitizer=RedactSanitizer()  # 脫敏清洗
)

# 檢測並清洗文本
text = "你是個白癡！聯繫我: test@example.com"
result = cleaner.clean(text)

print(result.cleaned_text)  # 你是個[REDACTED]！聯繫我: [REDACTED]
print(result.is_safe)      # True
```

### 🖥️ 命令列使用

```bash
# 檢測敏感內容
echo "你是個白癡" | python -m llm_cleaner detect

# 檢測並清洗
echo "你是個白癡" | python -m llm_cleaner clean

# 使用所有檢測器
python -m llm_cleaner clean --detect-all

# 互動式模式
python -m llm_cleaner interactive
```

---

## 📖 詳細使用指南

### 🎛️ 選擇檢測器

LLM-Cleaner 提供了多種內建檢測器，可以根據需求組合使用：

```python
from llm_cleaner.detectors import (
    SensitiveWordDetector,      # 敏感詞檢測
    PoliticalContentDetector,   # 政治敏感內容
    HarmfulContentDetector,     # 有害內容
    PIIDetector                # 個人身份資訊
)

# 組合使用
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),
        PoliticalContentDetector(),
        HarmfulContentDetector(),
        PIIDetector()
    ]
)
```

### 🔧 選擇清洗策略

```python
from llm_cleaner.sanitizers import (
    RedactSanitizer,          # 完全脫敏 [REDACTED]
    ReplaceSanitizer,         # 替換為安全詞
    RewriteSanitizer,         # 重寫為提示語
    PartialRedactSanitizer    # 部分脫敏 138****5678
)

# 使用脫敏清洗器
cleaner.set_sanitizer(RedactSanitizer())

# 使用替換清洗器
cleaner.set_sanitizer(ReplaceSanitizer())

# 使用部分脫敏（保留部分可見）
cleaner.set_sanitizer(PartialRedactSanitizer(visible_chars=3))
```

### 🎨 自訂敏感詞

```python
# 新增自訂敏感詞
detector = SensitiveWordDetector(
    custom_words={"自訂詞1", "自訂詞2"},
    sensitivity=0.9  # 敏感度 0.0-1.0
)

# 新增自訂正則模式
cleaner.add_custom_pattern(
    pattern=r"違禁詞彙\d+號",
    pattern_name="custom_banned",
    risk_level="high",
    category="custom"
)
```

### 🔌 集成到 LLM 調用流程

```python
# 在 LLM 回應後處理
def process_llm_response(response_text: str):
    result = cleaner.clean(response_text)
    
    if not result.is_safe:
        print("⚠️ 內容未通過安全檢測")
        return result.cleaned_text
    
    return response_text
```

---

## 💡 設計思路

### 🎯 設計理念

1. **零依賴原則** - 僅使用 Python 標準庫，確保在任何環境下都能運行
2. **模組化設計** - 檢測器和清洗器解耦，方便擴展
3. **高性能優先** - 使用預編譯正則表達式，處理速度快
4. **合規優先** - 所有檢測僅用於合規目的，不涉及任何敏感話題

### 🛠️ 技術選型

| 技術 | 選擇原因 |
|------|---------|
| Python re 模組 | 標準庫，無需額外依賴 |
| 正則表達式 | 高效的文本模式匹配 |
| 數據類 | 清晰的結果結構 |
| 列舉類型 | 明確的風險等級定義 |

### 📋 風險等級

| 等級 | 說明 | 示例 |
|------|------|------|
| 🟢 SAFE | 安全 | 正常文本 |
| 🟡 LOW | 低風險 | 一般敏感詞 |
| 🟠 MEDIUM | 中等風險 | 侮辱性詞彙 |
| 🔴 HIGH | 高風險 | 嚴重敏感詞 |
| 🚨 CRITICAL | 極高風險 | 犯罪指導 |

---

## 📦 打包與部署

### 🐳 Docker 使用

```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install llm-cleaner
CMD ["python", "-m", "llm_cleaner", "interactive"]
```

### ☁️ 在 LLM 服務中使用

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

## 🤝 貢獻指南

歡迎貢獻程式碼！請遵循以下步驟：

1. **Fork 本倉庫**
2. **建立特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'feat: 添加新特性'`)
4. **推送至分支** (`git push origin feature/AmazingFeature`)
5. **建立 Pull Request**

### 🐛 問題回饋

如發現問題，請提交 [Issue](https://github.com/gitstq/LLM-Cleaner/issues)。

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源。

---

## 🙏 致謝

- 靈感來源：[heretic](https://github.com/p-e-w/heretic) - LLM 審查移除工具
- 所有貢獻者

---

<div align="center">

**如果這個專案對您有幫助，請給個 ⭐️！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
