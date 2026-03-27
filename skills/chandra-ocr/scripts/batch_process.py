#!/usr/bin/env python3
"""
chandra-ocr — 批量处理工具

用法:
    python batch_process.py input_dir/ output_dir/ [--format markdown] [--workers 4]
"""

import argparse
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from chandra import extract
except ImportError:
    print("错误：未安装 chandra-ocr")
    print("请运行：pip install chandra-ocr")
    sys.exit(1)


def process_file(args):
    """
    处理单个文件
    
    Args:
        args: (input_file, output_dir, format)
    
    Returns:
        (success, output_file, error_message)
    """
    input_file, output_dir, format = args
    output_path = Path(output_dir)
    
    try:
        # 生成输出文件名
        output_name = input_file.stem
        if format == "markdown":
            output_file = output_path / f"{output_name}.md"
        elif format == "html":
            output_file = output_path / f"{output_name}.html"
        elif format == "json":
            output_file = output_path / f"{output_name}.json"
        else:
            return (False, None, f"不支持的格式：{format}")
        
        # 提取文档
        result = extract(str(input_file), output_format=format)
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                import json
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                f.write(result)
        
        return (True, str(output_file), None)
        
    except Exception as e:
        return (False, None, str(e))


def batch_process(input_dir: str, output_dir: str, format: str = "markdown", workers: int = 4):
    """
    批量处理文档
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        format: 输出格式
        workers: 并发数
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 验证输入目录
    if not input_path.exists():
        print(f"错误：目录不存在 - {input_dir}")
        return False
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找所有 PDF 和图片文件
    files = list(input_path.glob("*.pdf")) + \
            list(input_path.glob("*.png")) + \
            list(input_path.glob("*.jpg")) + \
            list(input_path.glob("*.jpeg"))
    
    if not files:
        print(f"错误：目录中没有找到 PDF 或图片文件 - {input_dir}")
        return False
    
    print(f"找到 {len(files)} 个文件")
    print(f"并发数：{workers}")
    print(f"输出格式：{format}")
    print(f"输出目录：{output_dir}")
    print("\n开始处理...\n")
    
    # 准备任务
    tasks = [(file, output_dir, format) for file in files]
    
    # 并发处理
    success_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_file, task) for task in tasks]
        
        for future in as_completed(futures):
            success, output_file, error = future.result()
            
            if success:
                success_count += 1
                print(f"✓ {Path(output_file).name}")
            else:
                error_count += 1
                print(f"✗ {Path(input_file).name}: {error}")
    
    print(f"\n处理完成：{success_count} 成功，{error_count} 失败")
    return error_count == 0


def main():
    parser = argparse.ArgumentParser(description="chandra-ocr — 批量处理工具")
    parser.add_argument("input", help="输入目录")
    parser.add_argument("output", help="输出目录")
    parser.add_argument("--format", choices=["markdown", "html", "json"], default="markdown",
                        help="输出格式（默认：markdown）")
    parser.add_argument("--workers", type=int, default=4, help="并发数（默认：4）")
    
    args = parser.parse_args()
    
    success = batch_process(args.input, args.output, args.format, args.workers)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
