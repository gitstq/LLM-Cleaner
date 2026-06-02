# 🧹 LLM-Cleaner

> インテリジェントLLM出力コンテンツ安全検出・消毒ツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/LLM-Cleaner?style=social)](https://github.com/gitstq/LLM-Cleaner)

---

## 🌐 言語切替

[🇨🇳 简体中文](README.md) | [🇭🇰 繁體中文](README_zh_TW.md) | [🇺🇸 English](README_en.md) | [🇯🇵 日本語](README_ja.md) | [🇰🇷 한국어](README_ko.md)

---

## 🎉 紹介

**LLM-Cleaner** は、LLM（大規模言語モデル）の出力から機密コンテンツを検出・消毒する軽量なゼロ依存Pythonライブラリです：

- ✨ **インテリジェント検出** - 機密言葉、侮辱的表現、政治的敏感なコンテンツを自動識別
- 🔒 **安全な消毒** - 複数の消毒戦略（墨消し、置換、書き直し）をサポート
- 📱 **PII保護** - メールアドレス、電話番号、身長証明書などの個人識別情報を自動検出・保護
- 🛡️ **有害コンテンツフィルタ** - 自殺指南、犯罪指南などの有害コンテンツをフィルタ
- 🔌 **簡単な統合** - クリーンなAPIで、数行のコードで統合可能

### ✨ コア機能

| 機能 | 説明 |
|------|------|
| 🧹 **機密言葉検出** | 内蔵の機密言葉リスト、カスタム拡張をサポート |
| 🏛️ **政治的コンテンツ検出** | 政治的に敏感なトピックを検出（コンプライアンスのみ） |
| ⚠️ **有害コンテンツフィルタ** - 自殺指南、犯罪指南をフィルタ |
| 🔐 **PII墨消し** | メール、電話、身長証明書などを自動検出 |
| 🔄 **複数の消毒モード** | 墨消し、置換、書き直し、部分墨消し |
| ⚡ **ゼロ依存** | Python標準ライブラリのみ |
| 🚀 **高性能** | 処理速度 < 10ms/1K文字 |
| 📦 **すぐ使える** | 複雑な設定不要 |

---

## 🚀 クイックスタート

### 📥 インストール

```bash
# pipでインストール
pip install llm-cleaner

# ソースからインストール
git clone https://github.com/gitstq/LLM-Cleaner.git
cd LLM-Cleaner
pip install -e .
```

### 💡 基本的な使用法

```python
from llm_cleaner import LLMCleaner
from llm_cleaner.detectors import SensitiveWordDetector, PIIDetector
from llm_cleaner.sanitizers import RedactSanitizer

# クリーナーを作成
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),  # 機密言葉検出
        PIIDetector()            # PII検出
    ],
    sanitizer=RedactSanitizer()  # 墨消し消毒
)

# テキストを検出して消毒
text = "あなたは馬鹿です！連絡先: test@example.com"
result = cleaner.clean(text)

print(result.cleaned_text)  # あなたは[REDACTED]！連絡先: [REDACTED]
print(result.is_safe)       # True
```

### 🖥️ CLI使用

```bash
# 機密コンテンツを検出
echo "あなたは馬鹿です" | python -m llm_cleaner detect

# 検出して消毒
echo "あなたは馬鹿です" | python -m llm_cleaner clean

# すべての検出器を使用
python -m llm_cleaner clean --detect-all

# インタラクティブモード
python -m llm_cleaner interactive
```

---

## 📖 詳細な使用方法

### 🎛️ 検出器の選択

```python
from llm_cleaner.detectors import (
    SensitiveWordDetector,      # 機密言葉
    PoliticalContentDetector,   # 政治的コンテンツ
    HarmfulContentDetector,   # 有害コンテンツ
    PIIDetector               # 個人識別情報
)

cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),
        PoliticalContentDetector(),
        HarmfulContentDetector(),
        PIIDetector()
    ]
)
```

### 🔧 消毒戦略の選択

```python
from llm_cleaner.sanitizers import (
    RedactSanitizer,          # 完全墨消し [REDACTED]
    ReplaceSanitizer,         # 安全言葉で置換
    RewriteSanitizer,         # プロンプトで書き直し
    PartialRedactSanitizer    # 部分墨消し 138****5678
)

cleaner.set_sanitizer(RedactSanitizer())
cleaner.set_sanitizer(ReplaceSanitizer())
cleaner.set_sanitizer(PartialRedactSanitizer(visible_chars=3))
```

---

## 💡 設計思想

### 🎯 設計原則

1. **ゼロ依存** - Python標準ライブラリのみ使用
2. **モジュラー設計** - 検出器と消毒器は分離、拡張が容易
3. **パフォーマンス優先** - プリコンパイル正規表現で高速処理
4. **コンプライアンス優先** - すべての検出はコンプライアンス目的のみ

### 📋 リスクレベル

| レベル | 説明 | 例 |
|--------|------|------|
| 🟢 SAFE | 安全 | 通常のテキスト |
| 🟡 LOW | 低リスク | 一般的な機密言葉 |
| 🟠 MEDIUM | 中リスク | 侮辱的表現 |
| 🔴 HIGH | 高リスク | 重大な機密言葉 |
| 🚨 CRITICAL | 重大リスク | 犯罪指南 |

---

## 🤝 コントリビュート

コントリビュートを歓迎します！以下の手順に従ってください：

1. **リポジトリをFork**
2. **機能ブランチを作成** (`git checkout -b feature/AmazingFeature`)
3. **変更をコミット** (`git commit -m 'feat: 素晴らしい機能を追加'`)
4. **ブランチにプッシュ** (`git push origin feature/AmazingFeature`)
5. **Pull Requestを作成**

---

## 📄 ライセンス

このプロジェクトは[MIT License](LICENSE)の元で公開されています。

---

<div align="center">

**このプロジェクトが役に立ったら、⭐️を주세요！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
