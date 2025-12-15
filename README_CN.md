# ai-cron

**基于 AI 的 Cron 任务生成器 - 现代化 Web 界面**

使用 AI 将自然语言转换为 cron 表达式。注重隐私，支持本地（Ollama）和云端 AI 模型（Google Gemini、OpenAI、Anthropic Claude 等）。

## ✨ 功能特性

- 🤖 **多模型 AI 支持**
  - **本地隐私**: Ollama (Llama 3, Mistral) - 无需联网
  - **云端强力**: Google Gemini, OpenAI GPT-4o, Anthropic Claude, DeepSeek, xAI Grok
  - **智能 Fallback**: 当 Ollama 不可用时自动切换模型

- 💻 **现代化 Web 界面**
  - **自然语言对话**: 通过聊天方式生成 cron 任务
  - **备份向导**: 引导式文件备份调度，带进度跟踪
  - **AI 设置**: 配置模型、API 密钥和端点

- ⚡ **智能特性**
  - **即时验证**: 安排前验证 cron 表达式
  - **下次运行预览**: 查看即将到来的执行时间
  - **一键部署**: 直接从 UI 添加到系统 crontab

## 📦 安装

### 前置要求

- **Python 3.10+**
- **Poetry** (推荐) 或 pip

### 方式 1: 使用 Poetry (推荐)

```bash
git clone https://github.com/dev-droid/ai-cron.git
cd ai-cron
poetry install
```

### 方式 2: 使用 pip

```bash
git clone https://github.com/dev-droid/ai-cron.git
cd ai-cron
pip install -r requirements.txt
# 或安装为可编辑包:
# pip install -e .
```

### 方式 3: 直接从 PyPI 安装

```bash
pip install ai-cron
```

### 可选: 安装 Ollama (用于本地 AI)

- **Windows**: [下载 Ollama](https://ollama.com/download/windows)
- **macOS**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`

安装 Ollama 后,拉取模型:

```bash
ollama pull llama3
```

### 方式 4: 使用 Docker (推荐快速启动)

最简单的运行方式，包含所有依赖:

```bash
# 克隆仓库
git clone https://github.com/dev-droid/ai-cron.git
cd ai-cron

# 使用 Docker Compose 启动
docker-compose up -d

# 在浏览器访问 http://localhost:8080
```

详细的 Docker 配置和部署选项请参见 [DOCKER.md](DOCKER.md)。

## 🚀 使用方法

### Web UI (推荐)

```bash
# 使用 Poetry
poetry run python -m aicron.main web --port 8080

# 使用 pip
python -m aicron.main web --port 8080
```

然后在浏览器中打开 `http://localhost:8080`。

### CLI 模式

```bash
# 使用 Poetry
poetry run python -m aicron.main "每周五下午5点备份 home 文件夹"

# 使用 pip
python -m aicron.main "每周五下午5点备份 home 文件夹"
```

## ⚙️ 配置

### 环境变量

对于需要代理的地区用户（例如中国使用 Google Gemini）:

```bash
# 为 AI API 请求设置代理
export AICRON_PROXY="http://127.0.0.1:7890"

# 或设置系统级代理（自动检测）
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

### API 密钥 (云端 AI 模型)

通过 Web UI 设置标签配置或导出为环境变量:

```bash
# Google Gemini
export GEMINI_API_KEY="<YOUR_GEMINI_API_KEY>"

# OpenAI
export OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"

# Anthropic Claude
export ANTHROPIC_API_KEY="<YOUR_ANTHROPIC_API_KEY>"
```

## 📂 项目结构

```
ai-cron/
├── aicron/
│   ├── __init__.py       # 包版本
│   ├── main.py           # CLI 入口点 (Typer)
│   ├── web.py            # Web UI (NiceGUI)
│   ├── llm.py            # AI 模型集成 (LiteLLM)
│   ├── cron.py           # Cron 验证和系统集成
│   ├── llm_tools.py      # 文件系统上下文工具
│   └── ollama_utils.py   # Ollama 安装检查
├── tests/
│   └── test_llm_logic.py # 单元测试
├── pyproject.toml        # Poetry 依赖
├── LICENSE               # MIT 许可证
└── README.md             # 本文件
```

## 🛠️ 开发

运行测试:

```bash
poetry run pytest
```

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

**版权所有 (c) 2025 dev-droid。保留所有权利。**

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request 或为 Bug 和功能请求开 Issue。

## 🌟 致谢

- 使用 [LiteLLM](https://github.com/BerriAI/litellm) 实现统一 AI API 访问
- UI 由 [NiceGUI](https://nicegui.io/) 驱动
- 灵感来自对隐私优先 AI 工具的需求
