#!/usr/bin/env python3
"""
内置清洗器模块
Built-in Sanitizers Module
"""

import re
from typing import Optional, Dict
from .cleaner import BaseSanitizer, DetectionMatch


class RedactSanitizer(BaseSanitizer):
    """
    脱敏清洗器
    将敏感内容替换为 [REDACTED] 或指定字符
    """
    
    def __init__(
        self, 
        replacement: str = "[REDACTED]",
        preserve_length: bool = False
    ):
        """
        初始化脱敏清洗器
        
        Args:
            replacement: 替换文本，默认 [REDACTED]
            preserve_length: 是否保留原长度（用 * 填充）
        """
        super().__init__(name="RedactSanitizer")
        self.replacement = replacement
        self.preserve_length = preserve_length
    
    def sanitize(self, text: str, match: DetectionMatch) -> str:
        """将匹配内容替换为脱敏标记"""
        matched_text = match.matched_text
        
        if self.preserve_length:
            replacement = "*" * len(matched_text)
        else:
            replacement = self.replacement
        
        return text[:match.start_pos] + replacement + text[match.end_pos:]


class ReplaceSanitizer(BaseSanitizer):
    """
    替换清洗器
    将敏感内容替换为指定的安全词汇
    """
    
    # 默认替换映射
    DEFAULT_REPLACEMENTS = {
        # 脏话替换
        "fuck": "f***",
        "shit": "s***",
        "damn": "d***",
        "asshole": "a*****",
        "bastard": "b******",
        # 中文替换
        "白痴": "XX",
        "笨蛋": "XX",
        "智障": "XX",
        "废物": "XX",
        "垃圾": "XX",
        "傻逼": "XX",
    }
    
    def __init__(
        self, 
        custom_replacements: Optional[Dict[str, str]] = None,
        case_sensitive: bool = False
    ):
        """
        初始化替换清洗器
        
        Args:
            custom_replacements: 自定义替换映射
            case_sensitive: 是否区分大小写
        """
        super().__init__(name="ReplaceSanitizer")
        self.replacements = self.DEFAULT_REPLACEMENTS.copy()
        if custom_replacements:
            self.replacements.update(custom_replacements)
        self.case_sensitive = case_sensitive
    
    def sanitize(self, text: str, match: DetectionMatch) -> str:
        """将匹配内容替换为安全词汇"""
        matched_text = match.matched_text
        
        # 查找替换值
        lower_text = matched_text.lower()
        replacement = self.replacements.get(lower_text)
        
        if replacement is None:
            # 使用默认脱敏标记
            replacement = "[FILTERED]"
        
        if not self.case_sensitive and matched_text.isupper():
            replacement = replacement.upper()
        elif not self.case_sensitive and matched_text[0].isupper():
            replacement = replacement.capitalize()
        
        return text[:match.start_pos] + replacement + text[match.end_pos:]


class RewriteSanitizer(BaseSanitizer):
    """
    重写清洗器
    使用预定义的安全模板重写敏感内容
    """
    
    # 重写模板
    REWRITE_TEMPLATES = {
        "sensitive_word": "该内容已被过滤",
        "insult_word": "该内容已被过滤",
        "political_keyword": "相关内容不便讨论",
        "political_pattern": "相关内容不便讨论",
        "harmful_content": "抱歉，这类内容我们无法提供帮助",
        "pii_email": "[邮箱已隐藏]",
        "pii_phone_cn": "[手机号已隐藏]",
        "pii_phone_us": "[电话已隐藏]",
        "pii_id_card_cn": "[身份证号已隐藏]",
        "pii_credit_card": "[银行卡号已隐藏]",
        "pii_ssn": "[社保号已隐藏]",
        "pii_ip_address": "[IP地址已隐藏]",
        "default": "[内容已过滤]",
    }
    
    def __init__(
        self, 
        custom_templates: Optional[Dict[str, str]] = None,
        safe_phrase: str = "[内容已过滤]"
    ):
        """
        初始化重写清洗器
        
        Args:
            custom_templates: 自定义重写模板
            safe_phrase: 默认安全短语
        """
        super().__init__(name="RewriteSanitizer")
        self.templates = self.REWRITE_TEMPLATES.copy()
        if custom_templates:
            self.templates.update(custom_templates)
        self.safe_phrase = safe_phrase
    
    def sanitize(self, text: str, match: DetectionMatch) -> str:
        """使用模板重写匹配内容"""
        replacement = self.templates.get(
            match.pattern_name, 
            self.templates.get("default", self.safe_phrase)
        )
        return text[:match.start_pos] + replacement + text[match.end_pos:]


class PartialRedactSanitizer(BaseSanitizer):
    """
    部分脱敏清洗器
    保留部分内容，只脱敏敏感部分
    例如：123****4567
    """
    
    def __init__(self, visible_chars: int = 4):
        """
        初始化部分脱敏清洗器
        
        Args:
            visible_chars: 两端保留的可见字符数
        """
        super().__init__(name="PartialRedactSanitizer")
        self.visible_chars = visible_chars
    
    def sanitize(self, text: str, match: DetectionMatch) -> str:
        """部分脱敏匹配内容"""
        matched_text = match.matched_text
        n = len(matched_text)
        
        if n <= self.visible_chars * 2 + 4:
            # 内容太短，使用完全脱敏
            replacement = "*" * min(n, 8)
        else:
            # 保留首尾可见字符
            start = matched_text[:self.visible_chars]
            end = matched_text[-self.visible_chars:]
            middle = "*" * max(4, n - self.visible_chars * 2)
            replacement = f"{start}{middle}{end}"
        
        return text[:match.start_pos] + replacement + text[match.end_pos:]
