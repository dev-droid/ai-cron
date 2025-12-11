# ai-cron

**AI-Powered Cron Job Generator with Modern Web UI**

Transform natural language into cron expressions using AI. Built with privacy in mind, supporting both local (Ollama) and cloud AI models (Google Gemini, OpenAI, Anthropic Claude, etc.).

## ✨ Features

- 🤖 **Multi-Model AI Support**
  - **Local Privacy**: Ollama (Llama 3, Mistral) - No internet required
  - **Cloud Power**: Google Gemini, OpenAI GPT-4o, Anthropic Claude, DeepSeek, xAI Grok
  - **Smart Fallback**: Automatic model switching when Ollama is unavailable

- 💻 **Modern Web UI**
  - **Natural Language Chat**: Generate cron jobs conversationally
  - **Backup Wizard**: Guided file backup scheduling with progress tracking
  - **AI Settings**: Configure models, API keys, and endpoints

- ⚡ **Smart Features**
  - **Instant Validation**: Verify cron expressions before scheduling
  - **Next Run Preview**: See upcoming execution times
  - **One-Click Deploy**: Add to system crontab directly from UI

## 📦 Installation

### Prerequisites

- **Python 3.10+**
- **Poetry** (recommended) or pip

### Option 1: Using Poetry (Recommended)

```bash
git clone https://github.com/dev-droid/ai-cron.git
cd ai-cron
poetry install
```

### Option 2: Using pip

```bash
git clone https://github.com/dev-droid/ai-cron.git
cd ai-cron
pip install -r requirements.txt  # Or: pip install -e .
```

### Optional: Install Ollama (for local AI)

- **Windows**: [Download Ollama](https://ollama.com/download/windows)
- **macOS**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`

After installing Ollama, pull a model:

```bash
ollama pull llama3
```

### Option 3: Using Docker (Recommended for Quick Start)

The easiest way to run ai-cron with all dependencies:

```bash
# Clone the repository
git clone https://github.com/dev-droid/ai-cron.git
cd ai-cron

# Start with Docker Compose
docker-compose up -d

# Access Web UI at http://localhost:8080
```

See [DOCKER.md](DOCKER.md) for detailed Docker configuration and deployment options.

## 🚀 Usage

### Web UI (Recommended)

```bash
# Using Poetry
poetry run python -m aicron.main web --port 8080

# Using pip
python -m aicron.main web --port 8080
```

Then open `http://localhost:8080` in your browser.

### CLI Mode

```bash
# Using Poetry
poetry run python -m aicron.main "Backup home folder every Friday at 5pm"

# Using pip
python -m aicron.main "Backup home folder every Friday at 5pm"
```

## ⚙️ Configuration

### Environment Variables

For users in regions requiring a proxy (e.g., China for Google Gemini):

```bash
# Set proxy for AI API requests
export AICRON_PROXY="http://127.0.0.1:7890"

# Or set system-wide proxy (automatically detected)
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

### API Keys (Cloud AI Models)

Configure via the Web UI Settings tab or export as environment variables:

```bash
# Google Gemini
export GEMINI_API_KEY="<YOUR_GEMINI_API_KEY>"

# OpenAI
export OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"

# Anthropic Claude
export ANTHROPIC_API_KEY="<YOUR_ANTHROPIC_API_KEY>"
```

## 📂 Project Structure

```
ai-cron/
├── aicron/
│   ├── __init__.py       # Package version
│   ├── main.py           # CLI entry point (Typer)
│   ├── web.py            # Web UI (NiceGUI)
│   ├── llm.py            # AI model integration (LiteLLM)
│   ├── cron.py           # Cron validation & system integration
│   ├── llm_tools.py      # File system context tools
│   └── ollama_utils.py   # Ollama installation checks
├── tests/
│   └── test_llm_logic.py # Unit tests
├── pyproject.toml        # Poetry dependencies
├── LICENSE               # MIT License
└── README.md             # This file
```

## 🛠️ Development

Run tests:

```bash
poetry run pytest
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

**Copyright (c) 2025 dev-droid. All rights reserved.**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 🌟 Acknowledgments

- Built with [LiteLLM](https://github.com/BerriAI/litellm) for unified AI API access
- UI powered by [NiceGUI](https://nicegui.io/)
- Inspired by the need for privacy-first AI tooling
