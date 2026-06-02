# 🧹 LLM-Cleaner

> 지능형 LLM 출력 콘텐츠 안전 감지 및 정리 도구

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/LLM-Cleaner?style=social)](https://github.com/gitstq/LLM-Cleaner)

---

## 🌐 언어 선택

[🇨🇳 简体中文](README.md) | [🇭🇰 繁體中文](README_zh_TW.md) | [🇺🇸 English](README_en.md) | [🇯🇵 日本語](README_ja.md) | [🇰🇷 한국어](README_ko.md)

---

## 🎉 소개

**LLM-Cleaner**는 LLM(대규모 언어 모델) 출력에서 잠재적으로 민감하거나 제한된 콘텐츠를 감지하고 정화하는 경량, Zero-dependency Python 라이브러리입니다:

- ✨ **지능형 감지** - 민감한 단어, 모욕적 언어, 정치적 민감한 콘텐츠 자동 식별
- 🔒 **안전한 정화** - 여러 정화 전략 지원 (삭제, 교체, 재작성)
- 📱 **PII 보호** - 이메일, 전화, 신분증 등의 개인 식별 정보 자동 감지 및 보호
- 🛡️ **유해 콘텐츠 필터** - 자살 지침, 범죄 지침 등 유해 콘텐츠 필터링
- 🔌 **쉬운 통합** - 깔끔한 API, 몇 줄의 코드로 통합 가능

### ✨ 핵심 기능

| 기능 | 설명 |
|------|------|
| 🧹 **민감한 단어 감지** | 내장 단어 목록 및 사용자 정의 확장 지원 |
| 🏛️ **정치적 콘텐츠 감지** | 정치적으로 민감한 주제 감지 (규정 준수용) |
| ⚠️ **유해 콘텐츠 필터** | 자살 가이드, 범죄 지침 등 필터링 |
| 🔐 **PII 삭제** | 이메일, 전화, 신분증 등 자동 감지 |
| 🔄 **다양한 정화 모드** | 삭제, 교체, 재작성, 부분 삭제 |
| ⚡ **Zero Dependencies** | Python 표준 라이브러리만 사용 |
| 🚀 **고성능** | 처리 속도 < 10ms/1K 문자 |
| 📦 **바로 사용** | 복잡한 설정 불필요 |

---

## 🚀 빠른 시작

### 📥 설치

```bash
# pip로 설치
pip install llm-cleaner

# 소스에서 설치
git clone https://github.com/gitstq/LLM-Cleaner.git
cd LLM-Cleaner
pip install -e .
```

### 💡 기본 사용법

```python
from llm_cleaner import LLMCleaner
from llm_cleaner.detectors import SensitiveWordDetector, PIIDetector
from llm_cleaner.sanitizers import RedactSanitizer

# 클리너 생성
cleaner = LLMCleaner(
    detectors=[
        SensitiveWordDetector(),  # 민감한 단어 감지
        PIIDetector()            # PII 감지
    ],
    sanitizer=RedactSanitizer()  # 삭제 정화
)

# 텍스트 감지 및 정화
text = "당신은 바보입니다! 연락처: test@example.com"
result = cleaner.clean(text)

print(result.cleaned_text)  # 당신은 [REDACTED]! 연락처: [REDACTED]
print(result.is_safe)       # True
```

### 🖥️ CLI 사용

```bash
# 민감한 콘텐츠 감지
echo "당신은 바보입니다" | python -m llm_cleaner detect

# 감지 및 정화
echo "당신은 바보입니다" | python -m llm_cleaner clean

# 모든 감지기 사용
python -m llm_cleaner clean --detect-all

# 대화형 모드
python -m llm_cleaner interactive
```

---

## 📖 상세 사용 가이드

### 🎛️ 감지기 선택

```python
from llm_cleaner.detectors import (
    SensitiveWordDetector,      # 민감한 단어
    PoliticalContentDetector,   # 정치적 콘텐츠
    HarmfulContentDetector,     # 유해 콘텐츠
    PIIDetector                # 개인 식별 정보
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

### 🔧 정화 전략 선택

```python
from llm_cleaner.sanitizers import (
    RedactSanitizer,          # 완전 삭제 [REDACTED]
    ReplaceSanitizer,         # 안전한 단어로 교체
    RewriteSanitizer,         # 프롬프트로 재작성
    PartialRedactSanitizer    # 부분 삭제 138****5678
)

cleaner.set_sanitizer(RedactSanitizer())
cleaner.set_sanitizer(ReplaceSanitizer())
cleaner.set_sanitizer(PartialRedactSanitizer(visible_chars=3))
```

---

## 💡 설계 철학

### 🎯 설계 원칙

1. **Zero Dependencies** - Python 표준 라이브러리만 사용
2. **모듈식 설계** - 감지기와 정화기가 분리되어 쉽게 확장 가능
3. **성능 우선** - 사전 컴파일된 정규식으로 빠른 처리
4. **규정 준수 우선** - 모든 감지는 규정 준수 목적만

### 📋 위험 수준

| 수준 | 설명 | 예시 |
|------|------|------|
| 🟢 SAFE | 안전 | 일반 텍스트 |
| 🟡 LOW | 저위험 | 일반 민감 단어 |
| 🟠 MEDIUM | 중위험 | 모욕적 표현 |
| 🔴 HIGH | 고위험 | 심각한 민감 단어 |
| 🚨 CRITICAL | 심각 | 범죄 지침 |

---

## 🤝 기여

기여를 환영합니다! 다음 단계를 따르세요:

1. **저장소 Fork**
2. **기능 브랜치 생성** (`git checkout -b feature/AmazingFeature`)
3. **변경 사항 커밋** (`git commit -m 'feat: 놀라운 기능 추가'`)
4. **브랜치에 푸시** (`git push origin feature/AmazingFeature`)
5. **Pull Request 열기**

---

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)하에 라이선스가 부여됩니다.

---

<div align="center">

**이 프로젝트가 도움이 되셨다면, ⭐️을 눌러주세요!**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
