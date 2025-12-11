# Copyright (c) 2025 dev-droid. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import shutil
import platform
import requests

def check_ollama_installed() -> bool:
    """
    Checks if Ollama executable is available in PATH.
    """
    return shutil.which("ollama") is not None

def check_ollama_running() -> bool:
    """
    Checks if Ollama service is running by pinging the localhost API.
    """
    try:
        response = requests.get("http://localhost:11434/", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_install_guide() -> str:
    """
    Returns installation instructions based on OS.
    """
    os_name = platform.system()
    if os_name == "Windows":
        return "请访问 https://ollama.com/download/windows 下载并安装 Ollama (Preview)。"
    elif os_name == "Darwin": # macOS
        return "请访问 https://ollama.com/download/mac 下载或者运行 `brew install ollama` (如果可用)。"
    elif os_name == "Linux":
        return "请运行: `curl -fsSL https://ollama.com/install.sh | sh`"
    else:
        return "请访问 https://ollama.com/download 查找适合您系统的安装方式。"
