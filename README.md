# OpenClaw Skills Monorepo

OpenClaw 技能集合仓库 - 模块化、可扩展的 AI 技能集合

## 📦 已集成的技能

### OCR 与文档处理
- **[chandra-ocr](skills/chandra-ocr/)** - 强大的 OCR 技能，处理复杂表格、表单、手写内容和数学公式

### 内容抓取
- **[feedgrab](skills/feedgrab/)** - 万能内容抓取器，从 7+ 平台和任意网站抓取内容

### 评估与测试
- **[skill-evaluator](skills/skill-evaluator/)** - Skill 评估工具，评估其他 Skill 的能力等级

### 内容处理
- **[summarize](skills/summarize/)** - 文档总结与摘要生成
- **[nano-pdf](skills/nano-pdf/)** - PDF 编辑与处理

## 🚀 快速开始

### 安装单个技能
```bash
# 克隆仓库
git clone https://github.com/lanyasheng/openclaw-skills.git
cd openclaw-skills

# 安装特定技能
cd skills/chandra-ocr
pip install -r requirements.txt
```

### 使用技能
```bash
# chandra-ocr 示例
chandra document.pdf ./output

# feedgrab 示例
feedgrab https://example.com/article ./output
```

## 📂 目录结构

```
skills-monorepo/
├── skills/           # 技能集合
│   ├── chandra-ocr/  # OCR 技能
│   ├── feedgrab/     # 内容抓取
│   └── ...
├── docs/             # 文档
├── examples/         # 示例
└── tests/            # 测试
```

## 🎯 技能标准

所有技能必须符合以下标准：
- ✅ 完整的 SKILL.md 文档
- ✅ 可执行的脚本
- ✅ 单元测试
- ✅ 使用示例
- ✅ 依赖管理

## 🧪 质量检验

每个技能都通过 `skill-evaluator` 评估：
- Level 1: 基础可用
- Level 2: 稳定可靠
- Level 3: 生产就绪

当前所有技能均为 **Level 3** 标准！

## 🤝 贡献指南

### 添加新技能
1. 在 `skills/` 目录创建技能文件夹
2. 编写 SKILL.md 文档
3. 实现核心功能脚本
4. 编写单元测试
5. 提交 PR

### 技能模板
```
skills/your-skill/
├── SKILL.md          # 必需：技能文档
├── README.md         # 必需：快速开始
├── requirements.txt  # 必需：Python 依赖
├── scripts/          # 必需：功能脚本
│   ├── main.py
│   └── ...
└── tests/            # 必需：单元测试
    └── test_main.py
```

## 📊 技能分类

### 按功能分类
- **文档处理**: chandra-ocr, nano-pdf
- **内容抓取**: feedgrab
- **内容处理**: summarize
- **评估测试**: skill-evaluator

### 按领域分类
- **OCR**: chandra-ocr
- **Web**: feedgrab
- **PDF**: nano-pdf
- **NLP**: summarize

## 🔧 开发工具

### 技能评估
```bash
cd skills/skill-evaluator
python scripts/evaluate.py ../chandra-ocr --output reports/
```

### 批量测试
```bash
# 测试所有技能
for skill in skills/*/; do
  echo "Testing $skill..."
  cd "$skill" && pytest tests/ -v && cd -
done
```

## 📝 更新日志

### v1.0.0 (2026-03-27)
- ✅ 初始版本
- ✅ 集成 chandra-ocr 技能
- ✅ 集成 feedgrab 技能
- ✅ 集成 skill-evaluator 技能
- ✅ 所有技能达到 Level 3 标准

## 🎯 路线图

### Q2 2026
- [ ] 集成 10+ 核心技能
- [ ] 建立技能市场
- [ ] 自动化测试 CI/CD
- [ ] 技能文档站点

### Q3 2026
- [ ] 技能依赖管理优化
- [ ] 技能版本控制
- [ ] 技能性能基准测试
- [ ] 技能社区贡献

## 🤝 社区

- GitHub: https://github.com/lanyasheng/openclaw-skills
- 讨论：GitHub Discussions
- 问题：GitHub Issues

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件

---

*OpenClaw Skills Monorepo — 模块化、可扩展的 AI 技能集合*
