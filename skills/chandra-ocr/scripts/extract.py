#!/usr/bin/env python3
"""
chandra-ocr — 文档提取脚本

用法:
    python extract.py input.pdf ./output [--format markdown|html|json] [--method hf|vllm]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from chandra import extract
except ImportError:
    print("错误：未安装 chandra-ocr")
    print("请运行：pip install chandra-ocr")
    sys.exit(1)


def extract_document(input_path: str, output_dir: str, format: str = "markdown", method: str = "hf"):
    """
    提取文档内容
    
    Args:
        input_path: 输入文件路径（PDF/图片）
        output_dir: 输出目录
        format: 输出格式（markdown/html/json）
        method: 推理方法（hf/vllm）
    """
    input_file = Path(input_path)
    output_path = Path(output_dir)
    
    # 验证输入文件
    if not input_file.exists():
        print(f"错误：文件不存在 - {input_path}")
        return False
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成输出文件名
    output_name = input_file.stem
    if format == "markdown":
        output_file = output_path / f"{output_name}.md"
    elif format == "html":
        output_file = output_path / f"{output_name}.html"
    elif format == "json":
        output_file = output_path / f"{output_name}.json"
    else:
        print(f"错误：不支持的格式 - {format}")
        return False
    
    print(f"处理文件：{input_file}")
    print(f"输出格式：{format}")
    print(f"推理方法：{method}")
    
    try:
        # 提取文档
        if method == "hf":
            # HuggingFace 推理
            result = extract(str(input_file), output_format=format)
        elif method == "vllm":
            # vLLM 推理
            result = extract(str(input_file), output_format=format, method="vllm")
        else:
            print(f"错误：不支持的推理方法 - {method}")
            return False
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                import json
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                f.write(result)
        
        print(f"✓ 提取成功：{output_file}")
        return True
        
    except Exception as e:
        print(f"错误：提取失败 - {str(e)}")
        return False


def batch_extract(input_dir: str, output_dir: str, format: str = "markdown", method: str = "hf"):
    """
    批量提取文档
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        format: 输出格式
        method: 推理方法
    """
    input_path = Path(input_dir)
    
    # 查找所有 PDF 和图片文件
    files = list(input_path.glob("*.pdf")) + \
            list(input_path.glob("*.png")) + \
            list(input_path.glob("*.jpg")) + \
            list(input_path.glob("*.jpeg"))
    
    if not files:
        print(f"错误：目录中没有找到 PDF 或图片文件 - {input_dir}")
        return False
    
    print(f"找到 {len(files)} 个文件")
    
    # 批量处理
    success_count = 0
    for file in files:
        if extract_document(str(file), output_dir, format, method):
            success_count += 1
    
    print(f"\n处理完成：{success_count}/{len(files)} 成功")
    return success_count == len(files)


def main():
    parser = argparse.ArgumentParser(description="chandra-ocr — 文档提取工具")
    parser.add_argument("input", help="输入文件路径（PDF/图片）或目录")
    parser.add_argument("output", help="输出目录")
    parser.add_argument("--format", choices=["markdown", "html", "json"], default="markdown",
                        help="输出格式（默认：markdown）")
    parser.add_argument("--method", choices=["hf", "vllm"], default="hf",
                        help="推理方法（默认：hf）")
    parser.add_argument("--batch", action="store_true", help="批量处理目录")
    
    args = parser.parse_args()
    
    if args.batch:
        success = batch_extract(args.input, args.output, args.format, args.method)
    else:
        success = extract_document(args.input, args.output, args.format, args.method)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
