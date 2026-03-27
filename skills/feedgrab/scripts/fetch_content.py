#!/usr/bin/env python3
"""
feedgrab 内容抓取脚本

用法:
    python fetch_content.py --url "https://xxx" --output ./output
    python fetch_content.py --clip --output ./output
    python fetch_content.py --search xhs-so --query "AI Agent" --output ./output
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from loguru import logger

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


def parse_args():
    parser = argparse.ArgumentParser(description="feedgrab 内容抓取")
    parser.add_argument("--url", type=str, help="要抓取的 URL")
    parser.add_argument("--clip", action="store_true", help="从剪贴板读取 URL")
    parser.add_argument("--search", type=str, help="搜索平台（xhs-so, mpweixin-so, ytb-so, x-so）")
    parser.add_argument("--query", type=str, help="搜索查询")
    parser.add_argument("--output", type=str, default="./output", help="输出目录")
    parser.add_argument("--limit", type=int, default=10, help="结果数量限制")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--download-media", action="store_true", help="下载媒体文件")
    return parser.parse_args()


def fetch_url(url: str, output_dir: str, json_output: bool = False, download_media: bool = False):
    """抓取单个 URL"""
    logger.info(f"抓取：{url}")
    
    # 构建命令
    cmd = ["feedgrab", url, "--output", output_dir]
    
    if json_output:
        cmd.append("--json")
    
    if download_media:
        # 检测平台并设置对应的下载环境变量
        if "x.com" in url or "twitter.com" in url:
            os.environ["X_DOWNLOAD_MEDIA"] = "true"
        elif "xiaohongshu.com" in url:
            os.environ["XHS_DOWNLOAD_MEDIA"] = "true"
        elif "mp.weixin.qq.com" in url:
            os.environ["MPWEIXIN_DOWNLOAD_MEDIA"] = "true"
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"抓取成功：{result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"抓取失败：{e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("feedgrab 未安装，请先运行：pip install feedgrab")
        return False


def fetch_clip(output_dir: str, json_output: bool = False):
    """从剪贴板抓取"""
    logger.info("从剪贴板读取 URL...")
    
    # 读取剪贴板（跨平台）
    try:
        import pyperclip
        url = pyperclip.paste()
        
        if not url.startswith("http"):
            logger.error("剪贴板内容不是有效的 URL")
            return False
        
        return fetch_url(url, output_dir, json_output)
    except ImportError:
        logger.error("需要安装 pyperclip: pip install pyperclip")
        return False
    except Exception as e:
        logger.error(f"读取剪贴板失败：{e}")
        return False


def search_platform(platform: str, query: str, output_dir: str, limit: int = 10):
    """搜索平台"""
    logger.info(f"搜索：{platform} - {query}")
    
    cmd = ["feedgrab", platform, query, "--limit", str(limit), "--output", output_dir]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"搜索成功：{result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"搜索失败：{e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("feedgrab 未安装，请先运行：pip install feedgrab")
        return False


def main():
    args = parse_args()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 执行抓取
    if args.url:
        success = fetch_url(args.url, args.output, args.json, args.download_media)
    elif args.clip:
        success = fetch_clip(args.output, args.json)
    elif args.search and args.query:
        success = search_platform(args.search, args.query, args.output, args.limit)
    else:
        logger.error("请提供 --url、--clip 或 --search + --query")
        sys.exit(1)
    
    if success:
        logger.info(f"完成！输出目录：{args.output}")
    else:
        logger.error("操作失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
