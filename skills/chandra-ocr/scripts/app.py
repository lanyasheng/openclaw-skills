#!/usr/bin/env python3
"""
chandra-ocr — Streamlit 交互应用

用法:
    streamlit run scripts/app.py
"""

import streamlit as st
from pathlib import Path
import tempfile
import os

try:
    from chandra import extract
except ImportError:
    st.error("错误：未安装 chandra-ocr")
    st.info("请运行：`pip install chandra-ocr`")
    st.stop()


def extract_document(input_file, format="markdown"):
    """提取文档内容"""
    try:
        result = extract(input_file, output_format=format)
        return result
    except Exception as e:
        st.error(f"提取失败：{str(e)}")
        return None


def main():
    st.set_page_config(
        page_title="chandra-ocr — 文档 OCR 工具",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 chandra-ocr — 文档 OCR 工具")
    st.markdown("""
    强大的 OCR 工具，处理复杂表格、表单、手写内容和数学公式
    
    支持格式：**PDF**, **PNG**, **JPG**  
    输出格式：**Markdown**, **HTML**, **JSON**
    """)
    
    # 侧边栏配置
    st.sidebar.header("⚙️ 配置")
    
    output_format = st.sidebar.selectbox(
        "输出格式",
        ["markdown", "html", "json"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**关于**")
    st.sidebar.info("""
    - 项目：[chandra-ocr](https://github.com/datalab-to/chandra)
    - 支持：40+ 语言
    - 特色：表格、表单、手写、公式识别
    """)
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传 PDF 或图片",
        type=["pdf", "png", "jpg", "jpeg"],
        help="支持 PDF、PNG、JPG 格式"
    )
    
    if uploaded_file is not None:
        # 显示文件信息
        st.markdown(f"**上传文件**: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        # 预览（如果是图片）
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(uploaded_file, caption="预览", use_column_width=True)
        
        # 预览（如果是 PDF）
        elif uploaded_file.type == "application/pdf":
            st.info("PDF 文件预览暂不支持，将直接提取内容")
        
        # 提取按钮
        if st.button("🚀 开始提取", type="primary"):
            with st.spinner("正在提取..."):
                # 保存临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    # 提取文档
                    result = extract_document(tmp_path, output_format)
                    
                    if result:
                        st.success("✓ 提取成功！")
                        
                        # 显示结果
                        if output_format == "markdown":
                            st.markdown("### 提取结果")
                            st.markdown(result)
                        
                        elif output_format == "html":
                            st.markdown("### 提取结果")
                            st.html(result)
                        
                        elif output_format == "json":
                            st.markdown("### 提取结果")
                            st.json(result)
                        
                        # 下载按钮
                        st.download_button(
                            label="📥 下载结果",
                            data=result if isinstance(result, str) else str(result),
                            file_name=f"{Path(uploaded_file.name).stem}.{output_format}",
                            mime="text/plain"
                        )
                    else:
                        st.error("提取失败，请查看错误信息")
                
                finally:
                    # 清理临时文件
                    os.unlink(tmp_path)
    
    # 使用示例
    st.markdown("---")
    st.markdown("### 💡 使用示例")
    
    with st.expander("查看命令行用法"):
        st.code("""
# 单个文件提取
chandra document.pdf ./output

# 批量处理
python scripts/batch_process.py input_dir/ output_dir/ --workers 4

# 交互式应用
streamlit run scripts/app.py
        """, language="bash")
    
    with st.expander("查看 API 用法"):
        st.code("""
from chandra import extract

# 提取为 Markdown
result = extract("document.pdf", output_format="markdown")

# 提取为 HTML
result = extract("document.pdf", output_format="html")

# 提取为 JSON（结构化）
result = extract("document.pdf", output_format="json")
        """, language="python")


if __name__ == "__main__":
    main()
