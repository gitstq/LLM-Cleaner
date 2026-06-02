#!/usr/bin/env python3
"""
LLM-Cleaner - 智能LLM输出内容安全检测与优化工具
LLM Output Content Safety Detection and Optimization Tool

A lightweight, zero-dependency Python library for detecting and sanitizing
potentially sensitive or restricted content in LLM outputs.

Author: gitstq
License: MIT
"""

__version__ = "1.0.0"
__author__ = "gitstq"

from .cleaner import LLMCleaner, CleanResult
from .detectors import (
    SensitiveWordDetector,
    PoliticalContentDetector,
    HarmfulContentDetector,
    PIIDetector
)
from .sanitizers import (
    ReplaceSanitizer,
    RedactSanitizer,
    RewriteSanitizer
)

__all__ = [
    "LLMCleaner",
    "CleanResult",
    "SensitiveWordDetector",
    "PoliticalContentDetector",
    "HarmfulContentDetector",
    "PIIDetector",
    "ReplaceSanitizer",
    "RedactSanitizer",
    "RewriteSanitizer",
]
