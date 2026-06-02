#!/usr/bin/env python3
"""
LLM-Cleaner CLI
命令行界面入口
"""

import argparse
import json
import sys
import os
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cleaner import LLMCleaner, RiskLevel
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


def create_cleaner(args) -> LLMCleaner:
    """根据参数创建LLM-Cleaner实例"""
    detectors = []
    
    if args.detect_all or args.detect_sensitive:
        detectors.append(SensitiveWordDetector())
    
    if args.detect_all or args.detect_political:
        detectors.append(PoliticalContentDetector())
    
    if args.detect_all or args.detect_harmful:
        detectors.append(HarmfulContentDetector())
    
    if args.detect_all or args.detect_pii:
        detectors.append(PIIDetector())
    
    # 选择清洗器
    sanitizer = None
    if args.sanitizer == "redact":
        sanitizer = RedactSanitizer(
            replacement=args.replacement or "[REDACTED]",
            preserve_length=args.preserve_length
        )
    elif args.sanitizer == "replace":
        sanitizer = ReplaceSanitizer()
    elif args.sanitizer == "rewrite":
        sanitizer = RewriteSanitizer()
    elif args.sanitizer == "partial":
        sanitizer = PartialRedactSanitizer()
    
    # 设置风险阈值
    risk_map = {
        "safe": RiskLevel.SAFE,
        "low": RiskLevel.LOW,
        "medium": RiskLevel.MEDIUM,
        "high": RiskLevel.HIGH,
        "critical": RiskLevel.CRITICAL
    }
    risk_threshold = risk_map.get(args.risk_threshold, RiskLevel.MEDIUM)
    
    return LLMCleaner(
        detectors=detectors,
        sanitizer=sanitizer if args.sanitize else None,
        auto_sanitize=args.sanitize,
        risk_threshold=risk_threshold
    )


def detect_mode(args):
    """仅检测模式"""
    cleaner = create_cleaner(args)
    
    # 读取输入文本
    if args.input_file:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    # 执行检测
    detections = cleaner.detect_only(text)
    
    # 输出结果
    if args.json_output:
        result = {
            "detection_count": len(detections),
            "detections": [d.to_dict() for d in detections]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not detections:
            print("✅ 未检测到敏感内容")
        else:
            print(f"⚠️  检测到 {len(detections)} 个敏感内容：\n")
            for i, detection in enumerate(detections, 1):
                risk_emoji = {
                    RiskLevel.SAFE: "🟢",
                    RiskLevel.LOW: "🟡",
                    RiskLevel.MEDIUM: "🟠",
                    RiskLevel.HIGH: "🔴",
                    RiskLevel.CRITICAL: "🚨"
                }.get(detection.risk_level, "⚪")
                
                print(f"{i}. {risk_emoji} [{detection.risk_level.value.upper()}] {detection.category}")
                print(f"   匹配内容: \"{detection.matched_text}\"")
                print(f"   位置: {detection.start_pos}-{detection.end_pos}")
                print(f"   置信度: {detection.confidence:.2%}")
                print()


def clean_mode(args):
    """检测并清洗模式"""
    cleaner = create_cleaner(args)
    
    # 读取输入文本
    if args.input_file:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    # 执行清洗
    result = cleaner.clean(text)
    
    # 输出结果
    if args.json_output:
        output = {
            "original_text": result.original_text,
            "cleaned_text": result.cleaned_text,
            "is_safe": result.is_safe,
            "statistics": result.to_dict()
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 显示统计信息
        risk_emoji = {
            RiskLevel.SAFE: "✅",
            RiskLevel.LOW: "🟢",
            RiskLevel.MEDIUM: "⚠️",
            RiskLevel.HIGH: "🔴",
            RiskLevel.CRITICAL: "🚨"
        }.get(result.overall_risk_level, "❓")
        
        print(f"{risk_emoji} 风险等级: {result.overall_risk_level.value.upper()}")
        print(f"📊 检测数量: {result.detection_count}")
        print(f"🧹 清洗数量: {result.sanitized_count}")
        print(f"⏱️ 处理时间: {result.processing_time_ms:.2f}ms")
        print()
        
        if result.cleaned_text != result.original_text:
            print("--- 原始文本 ---")
            print(result.original_text)
            print()
            print("--- 清洗后文本 ---")
            print(result.cleaned_text)
        else:
            print("✅ 文本已通过安全检测，无需清洗")


def interactive_mode(args):
    """交互式模式"""
    print("🧹 LLM-Cleaner 交互式模式")
    print("=" * 50)
    print("输入文本进行检测和清洗，输入 'quit' 或 'exit' 退出")
    print()
    
    cleaner = create_cleaner(args)
    
    while True:
        try:
            print("> ", end="")
            line = sys.stdin.readline()
            if not line:
                break
            
            text = line.strip()
            if text.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            if not text:
                continue
            
            result = cleaner.clean(text)
            
            risk_emoji = {
                RiskLevel.SAFE: "✅",
                RiskLevel.LOW: "🟢",
                RiskLevel.MEDIUM: "⚠️",
                RiskLevel.HIGH: "🔴",
                RiskLevel.CRITICAL: "🚨"
            }.get(result.overall_risk_level, "❓")
            
            print(f"  {risk_emoji} 风险: {result.overall_risk_level.value.upper()}")
            print(f"  📊 检测: {result.detection_count}, 清洗: {result.sanitized_count}")
            
            if result.has_issues:
                print(f"  🧹 清洗结果: {result.cleaned_text[:100]}...")
            else:
                print(f"  ✅ 安全，无需清洗")
            print()
            
        except KeyboardInterrupt:
            print("\n再见！")
            break


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="LLM-Cleaner - 智能LLM输出内容安全检测与优化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检测文本
  echo "你是个白痴" | python -m llm_cleaner detect
  
  # 检测并清洗
  echo "你是个白痴" | python -m llm_cleaner clean --sanitizer redact
  
  # 使用所有检测器
  python -m llm_cleaner detect --detect-all
  
  # 输出JSON格式
  python -m llm_cleaner clean --json-output
  
  # 交互式模式
  python -m llm_cleaner interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 检测命令
    detect_parser = subparsers.add_parser('detect', help='仅检测敏感内容')
    detect_parser.add_argument('input_file', nargs='?', help='输入文件路径')
    add_common_args(detect_parser)
    detect_parser.set_defaults(func=detect_mode)
    
    # 清洗命令
    clean_parser = subparsers.add_parser('clean', help='检测并清洗敏感内容')
    clean_parser.add_argument('input_file', nargs='?', help='输入文件路径')
    add_common_args(clean_parser)
    clean_parser.add_argument('--sanitizer', '-s', choices=['redact', 'replace', 'rewrite', 'partial'],
                              default='redact', help='清洗器类型')
    clean_parser.add_argument('--replacement', '-r', help='替换文本')
    clean_parser.add_argument('--preserve-length', action='store_true', help='替换时保留长度')
    clean_parser.add_argument('--sanitize', action='store_true', default=True, help='执行清洗')
    clean_parser.set_defaults(func=clean_mode)
    
    # 交互式命令
    interactive_parser = subparsers.add_parser('interactive', aliases=['i'], help='交互式模式')
    add_common_args(interactive_parser)
    interactive_parser.set_defaults(func=interactive_mode)
    
    # 默认命令
    parser.set_defaults(func=detect_mode)
    
    args = parser.parse_args()
    
    # 如果没有子命令，默认执行detect
    if args.command is None:
        args.sanitize = False
        args.detect_all = True
        args.json_output = False
    
    args.func(args)


def add_common_args(parser):
    """添加通用参数"""
    parser.add_argument('--detect-all', '-a', action='store_true', help='使用所有检测器')
    parser.add_argument('--detect-sensitive', action='store_true', help='检测敏感词')
    parser.add_argument('--detect-political', action='store_true', help='检测政治敏感内容')
    parser.add_argument('--detect-harmful', action='store_true', help='检测有害内容')
    parser.add_argument('--detect-pii', action='store_true', help='检测个人身份信息')
    parser.add_argument('--json-output', '-j', action='store_true', help='输出JSON格式')
    parser.add_argument('--risk-threshold', '-t', 
                        choices=['safe', 'low', 'medium', 'high', 'critical'],
                        default='medium', help='风险阈值')


if __name__ == '__main__':
    main()
