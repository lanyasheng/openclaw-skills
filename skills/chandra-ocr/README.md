# chandra-ocr — OpenClaw Skill

强大的 OCR 技能，处理复杂表格、表单、手写内容和数学公式

## 快速开始

### 1. 安装

```bash
cd /Users/study/.openclaw/skills/chandra-ocr
pip install -r requirements.txt
```

### 2. 使用

```bash
# 单个文件
chandra document.pdf ./output

# 批量处理
python scripts/batch_process.py input_dir/ output_dir/

# 交互应用
streamlit run scripts/app.py
```

### 3. 测试

```bash
pytest tests/test_extract.py -v
```

## 功能特性

- ✅ 复杂表格识别
- ✅ 表单识别（含复选框）
- ✅ 手写内容识别
- ✅ 数学公式识别
- ✅ 40+ 语言支持
- ✅ Markdown/HTML/JSON 输出

## 文档

- [SKILL.md](SKILL.md) - 完整技能文档
- [requirements.txt](requirements.txt) - Python 依赖

## 原项目

- GitHub: https://github.com/datalab-to/chandra
- 主页：https://www.datalab.to

## 许可证

- 代码：MIT
- 模型：查看原项目许可证
