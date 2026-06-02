#!/usr/bin/env python3
"""
内置检测器模块
Built-in Detectors Module
"""

import re
from typing import List, Dict, Set
from .cleaner import BaseDetector, DetectionMatch, RiskLevel


class SensitiveWordDetector(BaseDetector):
    """
    敏感词检测器
    检测常见的敏感词汇，包括脏话、侮辱性语言等
    """
    
    # 敏感词库（简化版，实际使用时应使用更完整的词库）
    SENSITIVE_WORDS = {
        # 脏话
        "ganda", "zanghua", "hua", "shit", "fuck", "damn", "asshole", "bastard",
        "cunt", "dick", "pussy", "cock", "faggot", "nigger", "retard",
        # 侮辱性词汇
        "白痴", "笨蛋", "蠢货", "智障", "废物", "垃圾",
    }
    
    INSULT_PATTERNS = [
        r"\b蠢材\b", r"\b废物\b", r"\b垃圾\b", r"\b白痴\b",
        r"\b笨蛋\b", r"\b智障\b", r"\b弱智\b", r"\b傻逼\b",
        r"\bsb\b", r"\bidiot\b", r"\bmoron\b", r"\bimbecile\b",
    ]
    
    def __init__(self, custom_words: Set[str] = None, sensitivity: float = 0.7):
        super().__init__(name="SensitiveWordDetector", category="sensitive_words")
        self.custom_words = custom_words or set()
        self.sensitivity = sensitivity
        self._compile_all_patterns()
    
    def _compile_all_patterns(self):
        all_words = self.SENSITIVE_WORDS | self.custom_words
        if all_words:
            # 中文没有词边界，使用无边界匹配
            word_pattern = "(" + "|".join(re.escape(w) for w in all_words) + ")"
            self._word_pattern = self._compile_pattern(word_pattern)
        self._insult_patterns = [self._compile_pattern(p) for p in self.INSULT_PATTERNS]
    
    def detect(self, text: str) -> List[DetectionMatch]:
        detections = []
        if hasattr(self, '_word_pattern'):
            for match in self._word_pattern.finditer(text):
                detections.append(self._create_match(
                    pattern_name="sensitive_word",
                    matched=match,
                    confidence=self.sensitivity,
                    risk_level=self._calculate_risk(match.group())
                ))
        for pattern in self._insult_patterns:
            for match in pattern.finditer(text):
                detections.append(self._create_match(
                    pattern_name="insult_word",
                    matched=match,
                    confidence=0.9,
                    risk_level=RiskLevel.MEDIUM
                ))
        return detections
    
    def _calculate_risk(self, word: str) -> RiskLevel:
        word_lower = word.lower()
        severe_words = {"fuck", "shit", "asshole", "cunt", "傻逼"}
        if word_lower in severe_words:
            return RiskLevel.HIGH
        medium_words = {"damn", "bastard", "智障", "弱智"}
        if word_lower in medium_words:
            return RiskLevel.MEDIUM
        low_words = {"白痴", "笨蛋", "蠢货"}
        if word_lower in low_words:
            return RiskLevel.LOW
        return RiskLevel.MEDIUM


class PoliticalContentDetector(BaseDetector):
    """
    政治敏感内容检测器
    注意：此检测器仅用于合规目的
    """
    
    POLITICAL_KEYWORDS = {
        "分裂", "颠覆", "暴动", "抗议", "政变",
        "武装", "恐怖", "极端",
    }
    
    POLITICAL_PATTERNS = [
        r"(暴力|武装|恐怖)(组织|活动|分子)",
        r"非法(集会|游行|示威)",
    ]
    
    def __init__(self, custom_keywords: Set[str] = None):
        super().__init__(name="PoliticalContentDetector", category="political")
        self.custom_keywords = custom_keywords or set()
        self._compile_patterns()
    
    def _compile_patterns(self):
        all_keywords = self.POLITICAL_KEYWORDS | self.custom_keywords
        if all_keywords:
            pattern = r"(" + "|".join(re.escape(k) for k in all_keywords) + r")"
            self._keyword_pattern = self._compile_pattern(pattern)
        self._regex_patterns = [self._compile_pattern(p) for p in self.POLITICAL_PATTERNS]
    
    def detect(self, text: str) -> List[DetectionMatch]:
        detections = []
        if hasattr(self, '_keyword_pattern'):
            for match in self._keyword_pattern.finditer(text):
                detections.append(self._create_match(
                    pattern_name="political_keyword",
                    matched=match,
                    confidence=0.8,
                    risk_level=RiskLevel.MEDIUM
                ))
        for pattern in self._regex_patterns:
            for match in pattern.finditer(text):
                detections.append(self._create_match(
                    pattern_name="political_pattern",
                    matched=match,
                    confidence=0.9,
                    risk_level=RiskLevel.HIGH
                ))
        return detections


class HarmfulContentDetector(BaseDetector):
    """
    有害内容检测器
    检测自我伤害、犯罪指导等有害内容
    """
    
    HARM_PATTERNS = [
        # 自杀/自残
        (r"(如何|怎么|能不能)(自杀|自残|结束生命)", RiskLevel.HIGH),
        (r"教.*(自杀|自残)", RiskLevel.CRITICAL),
        # 犯罪指导
        (r"(如何|怎么)(制造|制作)(炸弹|毒品|武器)", RiskLevel.CRITICAL),
        (r"(破解|盗取|入侵)(密码|账户|系统)", RiskLevel.HIGH),
        # 暴力
        (r"(如何|怎么)(杀人|伤害|攻击)", RiskLevel.HIGH),
    ]
    
    def __init__(self):
        super().__init__(name="HarmfulContentDetector", category="harmful")
        self._compile_patterns()
    
    def _compile_patterns(self):
        self._patterns = []
        for pattern, risk in self.HARM_PATTERNS:
            compiled = self._compile_pattern(pattern)
            self._patterns.append((compiled, risk))
    
    def detect(self, text: str) -> List[DetectionMatch]:
        detections = []
        for pattern, risk in self._patterns:
            for match in pattern.finditer(text):
                detections.append(self._create_match(
                    pattern_name="harmful_content",
                    matched=match,
                    confidence=0.95,
                    risk_level=risk
                ))
        return detections


class PIIDetector(BaseDetector):
    """
    个人身份信息检测器
    检测并识别可能泄露的个人身份信息
    """
    
    PII_PATTERNS = {
        "email": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", RiskLevel.MEDIUM),
        "phone_cn": (r"1[3-9]\d{9}", RiskLevel.MEDIUM),
        "phone_us": (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", RiskLevel.MEDIUM),
        "id_card_cn": (r"\b\d{17}[\dXx]\b", RiskLevel.HIGH),
        "credit_card": (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", RiskLevel.HIGH),
        "ssn": (r"\b\d{3}-\d{2}-\d{4}\b", RiskLevel.HIGH),
        "ip_address": (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", RiskLevel.LOW),
    }
    
    def __init__(self, detect_types: List[str] = None):
        super().__init__(name="PIIDetector", category="pii")
        self.detect_types = detect_types or list(self.PII_PATTERNS.keys())
        self._compile_patterns()
    
    def _compile_patterns(self):
        self._compiled = {}
        for pii_type in self.detect_types:
            if pii_type in self.PII_PATTERNS:
                pattern, risk = self.PII_PATTERNS[pii_type]
                self._compiled[pii_type] = (self._compile_pattern(pattern), risk)
    
    def detect(self, text: str) -> List[DetectionMatch]:
        detections = []
        for pii_type, (pattern, risk) in self._compiled.items():
            for match in pattern.finditer(text):
                detections.append(self._create_match(
                    pattern_name=f"pii_{pii_type}",
                    matched=match,
                    confidence=0.9,
                    risk_level=risk
                ))
        return detections
