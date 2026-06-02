#!/usr/bin/env python3
"""
LLM-Cleaner Core Module
核心检测与清洗引擎
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum


class RiskLevel(Enum):
    """风险等级枚举"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DetectionMatch:
    """检测匹配结果"""
    pattern_name: str
    matched_text: str
    start_pos: int
    end_pos: int
    confidence: float
    risk_level: RiskLevel
    category: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_name": self.pattern_name,
            "matched_text": self.matched_text,
            "start": self.start_pos,
            "end": self.end_pos,
            "confidence": self.confidence,
            "risk_level": self.risk_level.value,
            "category": self.category
        }


@dataclass
class CleanResult:
    """清洗结果"""
    original_text: str
    cleaned_text: str
    detections: List[DetectionMatch]
    overall_risk_level: RiskLevel
    detection_count: int
    sanitized_count: int
    processing_time_ms: float
    
    @property
    def is_safe(self) -> bool:
        return self.overall_risk_level in [RiskLevel.SAFE, RiskLevel.LOW]
    
    @property
    def has_issues(self) -> bool:
        return len(self.detections) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_length": len(self.original_text),
            "cleaned_length": len(self.cleaned_text),
            "detections": [d.to_dict() for d in self.detections],
            "overall_risk_level": self.overall_risk_level.value,
            "detection_count": self.detection_count,
            "sanitized_count": self.sanitized_count,
            "processing_time_ms": self.processing_time_ms,
            "is_safe": self.is_safe,
            "has_issues": self.has_issues
        }


class BaseDetector:
    """检测器基类"""
    
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self._compiled_patterns: Dict[str, re.Pattern] = {}
    
    def detect(self, text: str) -> List[DetectionMatch]:
        """检测文本中的敏感内容"""
        raise NotImplementedError
    
    def _compile_pattern(self, pattern: str) -> re.Pattern:
        """编译正则表达式并缓存"""
        if pattern not in self._compiled_patterns:
            self._compiled_patterns[pattern] = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        return self._compiled_patterns[pattern]
    
    def _create_match(
        self, 
        pattern_name: str, 
        matched: re.Match, 
        confidence: float, 
        risk_level: RiskLevel
    ) -> DetectionMatch:
        return DetectionMatch(
            pattern_name=pattern_name,
            matched_text=matched.group(),
            start_pos=matched.start(),
            end_pos=matched.end(),
            confidence=confidence,
            risk_level=risk_level,
            category=self.category
        )


class BaseSanitizer:
    """清洗器基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def sanitize(self, text: str, match: DetectionMatch) -> str:
        """清洗匹配的敏感内容"""
        raise NotImplementedError
    
    def batch_sanitize(self, text: str, matches: List[DetectionMatch]) -> str:
        """批量清洗所有匹配项（按位置倒序处理，避免索引偏移）"""
        sorted_matches = sorted(matches, key=lambda m: (m.start_pos, -m.end_pos), reverse=True)
        result = text
        for match in sorted_matches:
            result = self.sanitize(result, match)
        return result


class LLMCleaner:
    """
    LLM输出内容安全检测与优化工具
    主要功能：
    1. 多维度敏感内容检测
    2. 灵活的清洗策略
    3. 易于集成到任何LLM调用流程
    """
    
    def __init__(
        self,
        detectors: Optional[List[BaseDetector]] = None,
        sanitizer: Optional[BaseSanitizer] = None,
        auto_sanitize: bool = True,
        risk_threshold: RiskLevel = RiskLevel.MEDIUM
    ):
        """
        初始化LLM-Cleaner
        
        Args:
            detectors: 检测器列表，默认使用所有内置检测器
            sanitizer: 清洗器，默认使用脱敏清洗器
            auto_sanitize: 是否自动清洗，默认True
            risk_threshold: 风险阈值，超过此阈值的内容将被标记
        """
        self.detectors = detectors or []
        self.sanitizer = sanitizer
        self.auto_sanitize = auto_sanitize
        self.risk_threshold = risk_threshold
        self._risk_weights = {
            RiskLevel.SAFE: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }
    
    def add_detector(self, detector: BaseDetector) -> "LLMCleaner":
        """添加检测器"""
        self.detectors.append(detector)
        return self
    
    def set_sanitizer(self, sanitizer: BaseSanitizer) -> "LLMCleaner":
        """设置清洗器"""
        self.sanitizer = sanitizer
        return self
    
    def clean(self, text: str) -> CleanResult:
        """
        检测并清洗文本
        
        Args:
            text: 待处理的文本
            
        Returns:
            CleanResult: 清洗结果
        """
        import time
        start_time = time.time()
        
        all_detections: List[DetectionMatch] = []
        
        # 执行所有检测器
        for detector in self.detectors:
            detections = detector.detect(text)
            all_detections.extend(detections)
        
        # 计算整体风险等级
        overall_risk = self._calculate_overall_risk(all_detections)
        
        # 执行清洗
        cleaned_text = text
        sanitized_count = 0
        
        if self.auto_sanitize and self.sanitizer and all_detections:
            # 按位置排序（倒序）避免索引偏移
            sorted_detections = sorted(
                all_detections, 
                key=lambda m: (m.start_pos, -m.end_pos), 
                reverse=True
            )
            for detection in sorted_detections:
                new_text = self.sanitizer.sanitize(cleaned_text, detection)
                if new_text != cleaned_text:
                    sanitized_count += 1
                cleaned_text = new_text
        
        # 重新检测清洗后的文本
        if sanitized_count > 0:
            remaining_detections = []
            for detector in self.detectors:
                remaining = detector.detect(cleaned_text)
                remaining_detections.extend(remaining)
            all_detections = remaining_detections
            overall_risk = self._calculate_overall_risk(all_detections)
        
        processing_time = (time.time() - start_time) * 1000
        
        return CleanResult(
            original_text=text,
            cleaned_text=cleaned_text,
            detections=all_detections,
            overall_risk_level=overall_risk,
            detection_count=len(all_detections),
            sanitized_count=sanitized_count,
            processing_time_ms=processing_time
        )
    
    def detect_only(self, text: str) -> List[DetectionMatch]:
        """
        仅检测文本，不进行清洗
        
        Args:
            text: 待检测的文本
            
        Returns:
            List[DetectionMatch]: 检测结果列表
        """
        all_detections = []
        for detector in self.detectors:
            detections = detector.detect(text)
            all_detections.extend(detections)
        return all_detections
    
    def sanitize_only(self, text: str, matches: List[DetectionMatch]) -> str:
        """
        仅清洗文本，不进行检测
        
        Args:
            text: 待清洗的文本
            matches: 检测匹配结果
            
        Returns:
            str: 清洗后的文本
        """
        if not self.sanitizer:
            return text
        return self.sanitizer.batch_sanitize(text, matches)
    
    def _calculate_overall_risk(self, detections: List[DetectionMatch]) -> RiskLevel:
        """计算整体风险等级"""
        if not detections:
            return RiskLevel.SAFE
        
        max_risk = RiskLevel.SAFE
        for detection in detections:
            if self._risk_weights[detection.risk_level] > self._risk_weights[max_risk]:
                max_risk = detection.risk_level
        
        return max_risk
    
    def add_custom_pattern(
        self,
        pattern: str,
        pattern_name: str,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        category: str = "custom"
    ) -> "LLMCleaner":
        """添加自定义检测模式"""
        custom_detector = _CustomPatternDetector(pattern, pattern_name, risk_level, category)
        return self.add_detector(custom_detector)


class _CustomPatternDetector(BaseDetector):
    """自定义模式检测器"""
    
    def __init__(
        self, 
        pattern: str, 
        pattern_name: str, 
        risk_level: RiskLevel,
        category: str
    ):
        super().__init__(name=pattern_name, category=category)
        self.pattern = pattern
        self.pattern_name = pattern_name
        self.risk_level = risk_level
    
    def detect(self, text: str) -> List[DetectionMatch]:
        detections = []
        compiled = self._compile_pattern(self.pattern)
        
        for match in compiled.finditer(text):
            detections.append(self._create_match(
                pattern_name=self.pattern_name,
                matched=match,
                confidence=1.0,
                risk_level=self.risk_level
            ))
        
        return detections
