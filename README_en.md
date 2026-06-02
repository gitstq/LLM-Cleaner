# 🧹 LLM-Cleaner

> Intelligent LLM Output Content Safety Detection & Sanitization Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/LLM-Cleaner?style=social)](https://github.com/gitstq/LLM-Cleaner)

---

## 🌐 Language

[🇨🇳 简体中文](README.md) | [🇭🇰 繁體中文](README_zh_TW.md) | [🇺🇸 English](README_en.md) | [🇯🇵 日本語](README_ja.md) | [🇰🇷 한국어](README_ko.md)

---

## 🎉 Introduction

**LLM-Cleaner** is a lightweight, zero-dependency Python library for detecting and sanitizing potentially sensitive or restricted content in LLM (Large Language Model) outputs. It helps developers:

- ✨ **Smart Detection** - Automatically identify sensitive words, insults, political content
- 🔒 **Safe Sanitization** - Support multiple sanitization strategies (redact, replace, rewrite)
- 📱 **PII Protection** - Automatically detect and protect personal identity information (email, phone, ID, etc.)
- 🛡️ **Harmful Content Filter** - Filter harmful content like suicide instructions, crime guides
- 🔌 **Easy Integration** - Clean API, integrate in just a few lines of code

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧹 **Sensitive Word Detection** | Built-in word list with custom extension support |
| 🏛️ **Political Content Detection** | Detect politically sensitive topics (compliance only) |
| ⚠️ **Harmful Content Filter** | Filter suicide guides, crime instructions |
| 🔐 **PII Redaction** | Auto-detect email, phone, ID numbers |
| 🔄 **Multiple Sanitization Modes** | Redact, replace, rewrite, partial redact |
| ⚡ **Zero Dependencies** | Python standard library only |
| 🚀 **High Performance** | Processing speed < 10ms/1K chars |
| 📦 **Ready to Use** | No complex configuration needed |

---

## 🚀 Quick Start

### 📥 Installation

```bash
# Install via pip
pip install llm-cleaner

# Or install from source
git clone https://github.com/gitstq/LLM-Cleaner.git
cd LLM-Cleaner
pip install -e .
```

### 💡 Basic Usage

```python
from llm_cleaner import LLMCleaner
from llm_cleaner.detectors import SensitiveWordDetector, PIIDetector
from llm_cleaner.sanitizers import RedactSanitizer

# Create cleaner
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),  # Sensitive word detection
        PIIDetector()            # PII detection
    ],
    sanitizer=RedactSanitizer()  # Redact sanitizer
)

# Detect and sanitize text
text = "You are an idiot! Contact me: test@example.com"
result = cleaner.clean(text)

print(result.cleaned_text)  # You are an [REDACTED]! Contact me: [REDACTED]
print(result.is_safe)       # True
```

### 🖥️ CLI Usage

```bash
# Detect sensitive content
echo "You are an idiot" | python -m llm_cleaner detect

# Detect and sanitize
echo "You are an idiot" | python -m llm_cleaner clean

# Use all detectors
python -m llm_cleaner clean --detect-all

# Interactive mode
python -m llm_cleaner interactive
```

---

## 📖 Detailed Usage

### 🎛️ Choose Detectors

LLM-Cleaner provides multiple built-in detectors:

```python
from llm_cleaner.detectors import (
    SensitiveWordDetector,      # Sensitive words
    PoliticalContentDetector,   # Political content
    HarmfulContentDetector,     # Harmful content
    PIIDetector                # Personal identity info
)

# Combine detectors
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),
        PoliticalContentDetector(),
        HarmfulContentDetector(),
        PIIDetector()
    ]
)
```

### 🔧 Choose Sanitization Strategy

```python
from llm_cleaner.sanitizers import (
    RedactSanitizer,          # Complete redaction [REDACTED]
    ReplaceSanitizer,         # Replace with safe words
    RewriteSanitizer,         # Rewrite with prompt
    PartialRedactSanitizer    # Partial redaction 138****5678
)

# Use redact sanitizer
cleaner.set_sanitizer(RedactSanitizer())

# Use replace sanitizer
cleaner.set_sanitizer(ReplaceSanitizer())

# Use partial redaction (keep some visible)
cleaner.set_sanitizer(PartialRedactSanitizer(visible_chars=3))
```

### 🎨 Custom Patterns

```python
# Add custom sensitive words
detector = SensitiveWordDetector(
    custom_words={"custom_word1", "custom_word2"},
    sensitivity=0.9  # Sensitivity 0.0-1.0
)

# Add custom regex pattern
cleaner.add_custom_pattern(
    pattern=r"banned_word\d+",
    pattern_name="custom_banned",
    risk_level="high",
    category="custom"
)
```

### 🔌 Integrate with LLM Pipelines

```python
# Process LLM response
def process_llm_response(response_text: str):
    result = cleaner.clean(response_text)
    
    if not result.is_safe:
        print("⚠️ Content failed safety check")
        return result.cleaned_text
    
    return response_text
```

---

## 💡 Design Philosophy

### 🎯 Design Principles

1. **Zero Dependencies** - Use Python standard library only
2. **Modular Design** - Detectors and sanitizers are decoupled for easy extension
3. **Performance First** - Pre-compiled regex for fast processing
4. **Compliance First** - All detection is for compliance purposes only

### 🛠️ Tech Stack

| Tech | Reason |
|------|--------|
| Python re module | Standard library, no extra deps |
| Regex | Efficient text pattern matching |
| Dataclass | Clear result structure |
| Enum | Defined risk levels |

### 📋 Risk Levels

| Level | Description | Example |
|-------|-------------|---------|
| 🟢 SAFE | Safe | Normal text |
| 🟡 LOW | Low risk | General sensitive words |
| 🟠 MEDIUM | Medium risk | Insulting words |
| 🔴 HIGH | High risk | Severe sensitive words |
| 🚨 CRITICAL | Critical | Crime instructions |

---

## 📦 Packaging & Deployment

### 🐳 Docker

```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install llm-cleaner
CMD ["python", "-m", "llm_cleaner", "interactive"]
```

### ☁️ Use with LLM Services

```python
# OpenAI API example
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

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create your feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'feat: add amazing feature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### 🐛 Bug Reports

Please report issues at [GitHub Issues](https://github.com/gitstq/LLM-Cleaner/issues).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Inspired by [heretic](https://github.com/p-e-w/heretic) - LLM censorship removal tool
- All contributors

---

<div align="center">

**If this project helps you, please give it a ⭐️!**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
