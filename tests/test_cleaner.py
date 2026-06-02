#!/usr/bin/env python3
"""
LLM-Cleaner 单元测试
Unit Tests for LLM-Cleaner
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.cleaner import LLMCleaner, RiskLevel, DetectionMatch
from src.detectors import (
    SensitiveWordDetector,
    PoliticalContentDetector,
    HarmfulContentDetector,
    PIIDetector
)
from src.sanitizers import (
    RedactSanitizer,
    ReplaceSanitizer,
    RewriteSanitizer,
    PartialRedactSanitizer
)


class TestSensitiveWordDetector:
    """测试敏感词检测器"""
    
    def test_detect_sensitive_words(self):
        """测试检测敏感词"""
        detector = SensitiveWordDetector()
        text = "这是一个白痴的笨蛋"
        matches = detector.detect(text)
        
        assert len(matches) >= 2
        assert any(m.matched_text == "白痴" for m in matches)
        assert any(m.matched_text == "笨蛋" for m in matches)
    
    def test_no_detection_clean_text(self):
        """测试正常文本不检测"""
        detector = SensitiveWordDetector()
        text = "今天天气很好，适合出门散步"
        matches = detector.detect(text)
        
        # 正常文本不应该被检测为敏感词
        # (除非恰好匹配某些词)
        sensitive_matches = [m for m in matches if m.category == "sensitive_words"]
        assert len(sensitive_matches) == 0
    
    def test_custom_words(self):
        """测试自定义敏感词"""
        detector = SensitiveWordDetector(custom_words={"自定义敏感词"})
        text = "这是一个自定义敏感词"
        matches = detector.detect(text)
        
        assert len(matches) >= 1


class TestPIIDetector:
    """测试PII检测器"""
    
    def test_detect_email(self):
        """测试检测邮箱"""
        detector = PIIDetector(detect_types=["email"])
        text = "联系我: test@example.com"
        matches = detector.detect(text)
        
        assert len(matches) >= 1
        assert any("test@example.com" in m.matched_text for m in matches)
    
    def test_detect_phone_cn(self):
        """测试检测中国手机号"""
        detector = PIIDetector(detect_types=["phone_cn"])
        text = "电话: 13812345678"
        matches = detector.detect(text)
        
        assert len(matches) >= 1
        assert any("13812345678" in m.matched_text for m in matches)
    
    def test_detect_id_card(self):
        """测试检测身份证号"""
        detector = PIIDetector(detect_types=["id_card_cn"])
        text = "身份证: 110101199001011234"
        matches = detector.detect(text)
        
        assert len(matches) >= 1


class TestHarmfulContentDetector:
    """测试有害内容检测器"""
    
    def test_detect_harmful_content(self):
        """测试检测有害内容"""
        detector = HarmfulContentDetector()
        text = "如何自杀"
        matches = detector.detect(text)
        
        assert len(matches) >= 1
    
    def test_detect_crime_guide(self):
        """测试检测犯罪指导"""
        detector = HarmfulContentDetector()
        text = "如何制造炸弹"
        matches = detector.detect(text)
        
        assert len(matches) >= 1
        assert matches[0].risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]


class TestSanitizers:
    """测试清洗器"""
    
    def test_redact_sanitizer(self):
        """测试脱敏清洗器"""
        sanitizer = RedactSanitizer()
        match = DetectionMatch(
            pattern_name="test",
            matched_text="白痴",
            start_pos=5,
            end_pos=7,
            confidence=0.9,
            risk_level=RiskLevel.MEDIUM,
            category="test"
        )
        
        text = "这是一个白痴的测试"
        result = sanitizer.sanitize(text, match)
        
        assert "[REDACTED]" in result
        assert "白痴" not in result
    
    def test_replace_sanitizer(self):
        """测试替换清洗器"""
        sanitizer = ReplaceSanitizer()
        match = DetectionMatch(
            pattern_name="sensitive_word",
            matched_text="白痴",
            start_pos=5,
            end_pos=7,
            confidence=0.9,
            risk_level=RiskLevel.MEDIUM,
            category="sensitive_words"
        )
        
        text = "这是一个白痴的测试"
        result = sanitizer.sanitize(text, match)
        
        assert "白痴" not in result
        assert "XX" in result or "[FILTERED]" in result
    
    def test_partial_redact_sanitizer(self):
        """测试部分脱敏清洗器"""
        sanitizer = PartialRedactSanitizer(visible_chars=3)
        match = DetectionMatch(
            pattern_name="test",
            matched_text="13812345678",
            start_pos=5,
            end_pos=15,
            confidence=0.9,
            risk_level=RiskLevel.MEDIUM,
            category="test"
        )
        
        text = "电话: 13812345678"
        result = sanitizer.sanitize(text, match)
        
        assert "138" in result
        assert "***" in result or "*" in result


class TestLLMCleaner:
    """测试LLM-Cleaner主类"""
    
    def test_basic_clean(self):
        """测试基本清洗功能"""
        cleaner = LLMCleaner(
            detectors=[SensitiveWordDetector()],
            sanitizer=RedactSanitizer()
        )
        
        text = "这是一个白痴的测试"
        result = cleaner.clean(text)
        
        assert result.is_safe or result.cleaned_text != text
        assert "[REDACTED]" in result.cleaned_text
        assert result.processing_time_ms > 0
    
    def test_detect_only(self):
        """测试仅检测模式"""
        cleaner = LLMCleaner(
            detectors=[SensitiveWordDetector()],
            sanitizer=RedactSanitizer()
        )
        
        text = "这是一个白痴的测试"
        detections = cleaner.detect_only(text)
        
        assert len(detections) >= 1
        assert detections[0].matched_text == "白痴"
    
    def test_add_custom_pattern(self):
        """测试添加自定义模式"""
        cleaner = LLMCleaner()
        cleaner.add_custom_pattern(
            pattern="自定义词",
            pattern_name="custom",
            risk_level=RiskLevel.HIGH,
            category="custom"
        )
        
        text = "这是一个自定义词的测试"
        result = cleaner.clean(text)
        
        assert result.has_issues
    
    def test_batch_processing(self):
        """测试批量处理"""
        cleaner = LLMCleaner(
            detectors=[SensitiveWordDetector()],
            sanitizer=RedactSanitizer()
        )
        
        texts = [
            "正常文本",
            "包含白痴的文本",
            "也是正常的"
        ]
        
        results = [cleaner.clean(text) for text in texts]
        
        assert len(results) == 3
        assert results[1].has_issues
        assert not results[0].has_issues


class TestEdgeCases:
    """测试边界情况"""
    
    def test_empty_text(self):
        """测试空文本"""
        cleaner = LLMCleaner()
        result = cleaner.clean("")
        
        assert result.cleaned_text == ""
        assert result.detection_count == 0
    
    def test_unicode_text(self):
        """测试Unicode文本"""
        cleaner = LLMCleaner()
        text = "中文测试 🎉 Emoji测试"
        result = cleaner.clean(text)
        
        assert result.cleaned_text == text
        assert result.detection_count == 0
    
    def test_long_text(self):
        """测试长文本"""
        cleaner = LLMCleaner()
        text = "测试文本 " * 1000 + "白痴"
        result = cleaner.clean(text)
        
        assert "白痴" not in result.cleaned_text
        assert result.processing_time_ms < 1000  # 应在1秒内完成


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
