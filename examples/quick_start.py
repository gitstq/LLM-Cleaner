#!/usr/bin/env python3
"""
LLM-Cleaner 快速使用示例
Quick Start Examples
"""

from llm_cleaner import LLMCleaner
from llm_cleaner.detectors import (
    SensitiveWordDetector,
    PoliticalContentDetector,
    HarmfulContentDetector,
    PIIDetector
)
from llm_cleaner.sanitizers import (
    RedactSanitizer,
    ReplaceSanitizer,
    RewriteSanitizer,
    PartialRedactSanitizer
)

# ============================================================
# 示例1: 基础使用 - 一行代码检测和清洗
# Example 1: Basic Usage - One-line detection and sanitization
# ============================================================

def basic_usage():
    """基础使用示例"""
    # 创建清洗器（使用默认配置）
    cleaner = LLMCleaner()
    cleaner.add_detector(SensitiveWordDetector())
    cleaner.set_sanitizer(RedactSanitizer())
    
    # 检测文本
    text = "这是一个测试文本，包含一些敏感词：白痴、笨蛋。"
    result = cleaner.clean(text)
    
    print("原始文本:", text)
    print("清洗后:", result.cleaned_text)
    print("风险等级:", result.overall_risk_level.value)
    print("检测数量:", result.detection_count)


# ============================================================
# 示例2: 自定义配置 - 使用多种检测器和清洗策略
# Example 2: Custom Configuration - Multiple detectors and sanitizers
# ============================================================

def custom_config():
    """自定义配置示例"""
    # 创建完整的清洗器
    cleaner = LLMCleaner(
        detectors=[
            SensitiveWordDetector(),      # 敏感词检测
            PoliticalContentDetector(),   # 政治敏感内容
            HarmfulContentDetector(),     # 有害内容
            PIIDetector(),                # 个人身份信息
        ],
        sanitizer=RewriteSanitizer(),     # 使用重写清洗器
        auto_sanitize=True,
        risk_threshold="medium"
    )
    
    # 批量处理
    texts = [
        "联系我: test@example.com",
        "你是个白痴，应该去死",
        "如何制造炸弹",
    ]
    
    for text in texts:
        result = cleaner.clean(text)
        print(f"\n原始: {text}")
        print(f"清洗: {result.cleaned_text}")
        print(f"风险: {result.overall_risk_level.value}")


# ============================================================
# 示例3: 仅检测模式 - 不执行清洗
# Example 3: Detection Only Mode - Without sanitization
# ============================================================

def detect_only():
    """仅检测模式示例"""
    cleaner = LLMCleaner()
    cleaner.add_detector(SensitiveWordDetector())
    cleaner.add_detector(PIIDetector())
    
    text = "请联系 admin@example.com 或致电 13812345678"
    
    # 仅检测
    detections = cleaner.detect_only(text)
    
    print(f"检测到 {len(detections)} 个敏感内容:")
    for d in detections:
        print(f"  - [{d.category}] {d.matched_text} (置信度: {d.confidence:.0%})")


# ============================================================
# 示例4: 自定义敏感词 - 添加你自己的检测规则
# Example 4: Custom Patterns - Add your own detection rules
# ============================================================

def custom_patterns():
    """自定义模式示例"""
    cleaner = LLMCleaner()
    
    # 添加自定义敏感词
    cleaner.add_detector(SensitiveWordDetector(
        custom_words={"垃圾", "废物", "蠢货"},
        sensitivity=0.9
    ))
    
    # 添加自定义正则模式
    cleaner.add_custom_pattern(
        pattern=r"违禁词汇\d+号",
        pattern_name="custom_banned",
        risk_level="high",
        category="custom"
    )
    
    text = "这是一个测试：垃圾、废物、违禁词汇123号"
    result = cleaner.clean(text)
    
    print(f"原始: {text}")
    print(f"清洗: {result.cleaned_text}")


# ============================================================
# 示例5: 集成到LLM调用流程
# Example 5: Integration with LLM Pipelines
# ============================================================

def llm_integration_example():
    """LLM集成示例（伪代码）"""
    # 这是集成到实际LLM调用流程的示例
    # 请根据你使用的LLM库进行适配
    
    # 1. 创建清洗器
    cleaner = LLMCleaner()
    cleaner.add_detector(SensitiveWordDetector())
    cleaner.add_detector(PIIDetector())
    cleaner.set_sanitizer(RedactSanitizer())
    
    # 2. 在调用LLM之前（如果需要过滤用户输入）
    # user_input = "告诉我如何攻击某人的电脑"
    # cleaned_input = cleaner.clean(user_input).cleaned_text
    # response = llm.generate(cleaned_input)
    
    # 3. 在获取LLM响应之后（必须）
    # llm_response = llm.generate(user_input)
    # cleaned_response = cleaner.clean(llm_response)
    # 
    # if not cleaned_response.is_safe:
    #     # 处理不安全的内容
    #     print("内容未通过安全检测")
    #     print(cleaned_response.cleaned_text)
    
    print("LLM集成示例（请根据实际LLM库进行适配）")


# ============================================================
# 示例6: 部分脱敏 - 保留部分可见信息
# Example 6: Partial Redaction - Keep some information visible
# ============================================================

def partial_redaction():
    """部分脱敏示例"""
    cleaner = LLMCleaner()
    cleaner.add_detector(PIIDetector())
    cleaner.set_sanitizer(PartialRedactSanitizer(visible_chars=3))
    
    texts = [
        "邮箱: test@example.com",
        "电话: 13812345678",
        "身份证: 110101199001011234",
    ]
    
    for text in texts:
        result = cleaner.clean(text)
        print(f"原始: {text}")
        print(f"清洗: {result.cleaned_text}")
        print()


# ============================================================
# 示例7: 批量处理 - 处理多个文本
# Example 7: Batch Processing - Handle Multiple Texts
# ============================================================

def batch_processing():
    """批量处理示例"""
    cleaner = LLMCleaner()
    cleaner.add_detector(SensitiveWordDetector())
    cleaner.set_sanitizer(ReplaceSanitizer())
    
    # 批量文本
    texts = [
        "你好！今天天气不错。",
        "你真是个白痴啊！",
        "请联系 support@company.com",
    ]
    
    results = []
    for text in texts:
        result = cleaner.clean(text)
        results.append(result)
    
    # 统计
    safe_count = sum(1 for r in results if r.is_safe)
    unsafe_count = len(results) - safe_count
    
    print(f"处理完成: {len(results)} 条文本")
    print(f"  ✅ 安全: {safe_count}")
    print(f"  ⚠️  需要处理: {unsafe_count}")


# ============================================================
# 示例8: 获取详细报告
# Example 8: Get Detailed Reports
# ============================================================

def detailed_report():
    """获取详细报告示例"""
    cleaner = LLMCleaner()
    cleaner.add_detector(SensitiveWordDetector())
    cleaner.add_detector(PIIDetector())
    cleaner.set_sanitizer(RedactSanitizer())
    
    text = "联系客服: spam@domain.com，你这个笨蛋！"
    result = cleaner.clean(text)
    
    # 获取详细报告
    report = result.to_dict()
    
    print("=== 详细报告 ===")
    print(f"原始长度: {report['original_length']}")
    print(f"清洗后长度: {report['cleaned_length']}")
    print(f"整体风险: {report['overall_risk_level']}")
    print(f"检测数量: {report['detection_count']}")
    print(f"清洗数量: {report['sanitized_count']}")
    print(f"处理时间: {report['processing_time_ms']:.2f}ms")
    print()
    
    print("=== 检测详情 ===")
    for detection in report['detections']:
        print(f"  [{detection['category']}] {detection['matched_text']}")
        print(f"    位置: {detection['start']}-{detection['end']}")
        print(f"    风险: {detection['risk_level']}")
        print(f"    置信度: {detection['confidence']:.0%}")


if __name__ == "__main__":
    print("=" * 60)
    print("LLM-Cleaner 使用示例")
    print("=" * 60)
    
    print("\n--- 示例1: 基础使用 ---")
    basic_usage()
    
    print("\n--- 示例2: 自定义配置 ---")
    custom_config()
    
    print("\n--- 示例3: 仅检测模式 ---")
    detect_only()
    
    print("\n--- 示例4: 自定义模式 ---")
    custom_patterns()
    
    print("\n--- 示例5: LLM集成 ---")
    llm_integration_example()
    
    print("\n--- 示例6: 部分脱敏 ---")
    partial_redaction()
    
    print("\n--- 示例7: 批量处理 ---")
    batch_processing()
    
    print("\n--- 示例8: 详细报告 ---")
    detailed_report()
