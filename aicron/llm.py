# Copyright (c) 2025 dev-droid. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import os
import sys
from typing import Optional

# Check if litellm is installed
try:
    from litellm import completion
except ImportError:
    completion = None

# Fallback or check for ollama specifically if needed, but litellm handles it.
# For this MVP, we will assume litellm is available or we might need to use requests for direct Ollama API if litellm is too heavy to install in some envs? 
# The plan mentioned LiteLLM or direct Ollama. Let's stick to LiteLLM for now as per plan, but handle import error gracefully-ish or just fail since it's a dep.

import json
from .llm_tools import list_dir, find_file

# Old prompt kept for reference or fallback if needed (though we will switch to JSON primarily)
LEGACY_PROMPT = """You are a Cron Expression Generator. ..."""

JSON_SYSTEM_PROMPT = """You are an intelligent System Admin Assistant.
Your task is to convert natural language into a Cron Job object in JSON format.
You have access to file system tools if the user asks to look for files.
You should generate the actual command to run, not just the time.

Output Format: JSON
{
  "cron": "str (standard 5-field expression)",
  "explanation": "str (Chinese explanation)",
  "command": "str (The full command to execute, e.g., 'tar -czf ...')",
  "warning": "str (Optional warning if the command looks dangerous or ambiguous)"
}

Rules:
1. Return ONLY valid JSON.
2. If the user asks to backup a specific file/dir, use the tool context provided (if any) or assume standard paths.
3. If the user query implies searching for a file, you can't *run* tools yourself in this turn, but you should infer the path or ask for it.
   (Wait, for this MVP we will inject context if the prompt contains keywords "find" or "list").
   Actually, let's keep it simple: The prompt will include context from tools if we run them.
"""

def generate_cron(prompt: str, model: str = "ollama/llama3", config: dict = None) -> str:
    """
    Generates a cron expression and command from natural language.
    Returns: JSON string (or plain string if legacy model fails parsing).
    """
    use_config = config or {}
    api_base = use_config.get("api_base", "http://localhost:11434" if "ollama" in model else None)
    if not api_base: api_base = None # Ensure empty strings are treated as None for native support
    api_key = use_config.get("api_key", None)

    # 1. Tool Use / Context Injection (Naive Agent)
    # If the user asks to "find" or "list", we might want to check context.
    # For now, let's purely rely on the LLM to generate the command, 
    # but we can append "Available Tools: list_dir, find_file" if we want it to *suggest* tool use?
    # Better: user manually runs tools in UI, or we inject "Current dir: ..." if irrelevant. 
    # Let's stick to the prompt update first.

    messages = [
        {"role": "system", "content": JSON_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    if model == "mock":
        # Deterministic mock response
        if "backup" in prompt.lower() or "备份" in prompt:
             return json.dumps({
                 "cron": "0 0 * * *", 
                 "explanation": "每天午夜运行", 
                 "command": "/usr/bin/tar -czf /backup/archive.tar.gz /var/www/html",
                 "warning": None
             }, ensure_ascii=False)
        return json.dumps({
            "cron": "0 8 * * *", 
            "explanation": "每天 08:00 运行", 
            "command": "echo 'Hello World'",
            "warning": None
        }, ensure_ascii=False)

    if completion is None:
        raise ImportError("LiteLLM is not installed.")

    try:
        response = completion(
            model=model, 
            messages=messages,
            api_base=api_base,
            api_key=api_key
        )
        content = response.choices[0].message.content.strip()
        # Clean markdown usually returned by LLMs
        content = content.replace("```json", "").replace("```", "").strip()
        return content
    except Exception as e:
        # Fallback error JSON
        return json.dumps({"cron": "ERROR", "explanation": str(e), "command": "", "warning": "API Error"})
    except Exception as e:
        return f"ERROR|LLM Call failed: {str(e)}"

if __name__ == "__main__":
    # Simple test
    if len(sys.argv) > 1:
        print(generate_cron(sys.argv[1]))
    else:
        print("Usage: python llm.py 'your prompts'")
