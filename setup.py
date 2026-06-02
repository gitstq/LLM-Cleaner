#!/usr/bin/env python3
"""
LLM-Cleaner
智能LLM输出内容安全检测与优化工具

A lightweight, zero-dependency Python library for detecting and sanitizing
potentially sensitive or restricted content in LLM outputs.

Author: gitstq
License: MIT
"""

from setuptools import setup, find_packages
import os

# 读取README
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "LLM-Cleaner - 智能LLM输出内容安全检测与优化工具"

# 读取版本
version = "1.0.0"

setup(
    name="llm-cleaner",
    version=version,
    description="智能LLM输出内容安全检测与优化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="gitstq",
    author_email="",
    url="https://github.com/gitstq/LLM-Cleaner",
    
    # 包配置
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    package_dir={"": "."},
    package_data={
        "llm_cleaner": ["py.typed"],
    },
    include_package_data=True,
    
    # 入口点
    entry_points={
        "console_scripts": [
            "llm-cleaner=llm_cleaner.cli:main",
        ],
    },
    
    # Python版本要求
    python_requires=">=3.8",
    
    # 依赖（零依赖）
    install_requires=[],
    
    # 分类
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
        "Topic :: Security",
    ],
    
    # 关键字
    keywords=[
        "llm", "openai", "claude", "content-filter", "safety",
        "moderation", "sanitization", "nlp", "security", "filter",
        "敏感词", "内容审核", "文本过滤", "安全检测"
    ],
    
    # 项目元数据
    project_urls={
        "Bug Reports": "https://github.com/gitstq/LLM-Cleaner/issues",
        "Source": "https://github.com/gitstq/LLM-Cleaner",
        "Documentation": "https://github.com/gitstq/LLM-Cleaner#readme",
    },
    
    # 许可证
    license="MIT",
    
    # zip安全
    zip_safe=False,
)
