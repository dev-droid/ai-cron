# Copyright (c) 2025 dev-droid. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

from nicegui import ui
from .llm import generate_cron
from .ollama_utils import check_ollama_installed, check_ollama_running, get_install_guide
from .llm_tools import list_dir
import time
import asyncio
import json
import os

# Configure Proxy (Optional: Set HTTP_PROXY/HTTPS_PROXY env vars externally if needed)
# Detect proxy from environment or use local default for development
if not os.environ.get("HTTP_PROXY"):
    # Auto-detect common local proxy ports (for GFW bypass in development)
    os.environ["HTTP_PROXY"] = os.environ.get("AICRON_PROXY", "")
    os.environ["HTTPS_PROXY"] = os.environ.get("AICRON_PROXY", "")

# Global Config (In-memory for MVP)
app_config = {
    "model": "ollama/llama3",
    "api_base": "http://localhost:11434",
    "api_key": ""  # Users should configure their API key via UI Settings
}

@ui.page('/')
def index_page():
    # --- UI Header ---
    with ui.header().classes('items-center justify-between'):
        ui.label('ai-cron Web').classes('text-2xl font-bold')
        with ui.row():
             ui.badge('Local Mode', color='green').classes('mr-4')

    # --- Ollama Check ---
    if not check_ollama_installed():
        with ui.dialog() as install_dialog, ui.card():
            ui.label('未检测到 Ollama!')
            ui.label('ai-cron 依赖 Ollama 进行本地推理。')
            ui.markdown(get_install_guide())
            ui.button('关闭', on_click=install_dialog.close)
        install_dialog.open()
    elif not check_ollama_running():
         ui.notify('Ollama 已安装但未运行，请确保启动 Ollama 服务。', type='warning', close_button=True)

    # --- Main Content ---
    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat', label='自然语言生成')
        backup_tab = ui.tab('Backup', label='备份向导')
        settings_tab = ui.tab('Settings', label='设置')

    with ui.tab_panels(tabs, value=chat_tab).classes('w-full'):
        
        # --- Tab 1: Chat Interface ---
        with ui.tab_panel(chat_tab).classes('h-[calc(100vh-150px)] p-0'): # Use fixed height relative to viewport (removing header/tabs height approx)
            # Actually, h-screen on tab panel might be tricky if parent isn't.
            # Let's try column with flex-grow inside the panel which NiceGUI usually makes flexible.
            
            with ui.column().classes('w-full h-full no-wrap justify-between'):
                # Chat Area (Scrollable)
                chat_scroll = ui.scroll_area().classes('w-full flex-grow p-4')
                with chat_scroll:
                     chat_container = ui.column().classes('w-full')

                # Context State
                file_context = []

                def append_context(path):
                    result = list_dir(path)
                    preview = result[:100] + "..." if len(result) > 100 else result
                    file_context.append(f"Directory listing of '{path}':\n{result}")
                    ui.notify(f"已添加目录上下文: {path}", type='info')
                    with chat_container:
                        ui.chat_message(f"已读取目录: {path}\n```\n{preview}\n```", name='System', sent=False).classes('opacity-50')
                    chat_scroll.scroll_to(percent=1.0) # Auto scroll

                def on_scan_dir():
                    with ui.dialog() as d, ui.card():
                        ui.label('扫描目录上下文')
                        path_input = ui.input('目录路径', value='.')
                        ui.button('扫描', on_click=lambda: [append_context(path_input.value), d.close()])
                    d.open()

                def on_send():
                    prompt = text_input.value
                    if not prompt: return
                    
                    full_prompt = prompt
                    if file_context:
                        full_prompt += "\n\n[System Context]:\n" + "\n".join(file_context)
                    
                    with chat_container:
                        ui.chat_message(prompt, name='Me', sent=True)
                    chat_scroll.scroll_to(percent=1.0)
                    
                    text_input.value = ''
                    
                    with chat_container:
                        spinner = ui.spinner(size='lg')
                    chat_scroll.scroll_to(percent=1.0)
                    
                    ui.timer(0.1, lambda: process_response(full_prompt, spinner), once=True)

                def process_response(prompt, spinner_elem):
                    spinner_elem.delete()
                    
                    current_model = app_config["model"]
                    if "ollama" in current_model and not check_ollama_running():
                        effective_model = "mock"
                    else:
                        effective_model = current_model

                    response_str = generate_cron(prompt, model=effective_model, config=app_config)
                    
                    with chat_container:
                        try:
                            data = json.loads(response_str)
                            cron = data.get("cron", "ERROR")
                            explanation = data.get("explanation", "Parse Error")
                            command = data.get("command", "")
                            warning = data.get("warning")

                            display_name = f'AI ({effective_model})'
                            with ui.chat_message(name=display_name, sent=False):
                                ui.markdown(f"**Cron:** `{cron}`")
                                ui.markdown(f"**Explanation:** {explanation}")
                                if warning:
                                    ui.alert(warning, type='warning')
                                
                                if command:
                                    ui.markdown(f"**Command:** `{command}`")
                                
                                def add_to_system_dialog(expr, cmd):
                                    with ui.dialog() as dialog, ui.card():
                                        ui.label('添加到系统 Crontab')
                                        cmd_input = ui.input('要运行的命令', value=cmd).classes('w-full')
                                        
                                        def do_add():
                                            final_cmd = cmd_input.value
                                            if not final_cmd:
                                                ui.notify('请输入命令', type='warning')
                                                return
                                            
                                            from .cron import add_job
                                            success = add_job(expr, final_cmd, "Generated by ai-cron Web")
                                            
                                            if success:
                                                ui.notify('成功添加到系统 Crontab!', type='positive')
                                                dialog.close()
                                            else:
                                                ui.notify('写入失败，请检查日志。', type='negative')
    
                                        with ui.row().classes('justify-end w-full'):
                                            ui.button('取消', on_click=dialog.close).props('flat')
                                            ui.button('确认添加', on_click=do_add)
                                    dialog.open()
    
                                with ui.row():
                                    ui.button('添加到系统', on_click=lambda: add_to_system_dialog(cron, command))
                        
                        except json.JSONDecodeError:
                            if "|" in response_str:
                                cron, explanation = response_str.split("|", 1)
                                with ui.chat_message(name='AI', sent=False):
                                    ui.markdown(f"**Cron:** `{cron}`\n\n{explanation}")
                                    ui.label("System: Received legacy text format.")
                            else:
                                ui.chat_message(response_str, name='AI Error', sent=False)
                    
                    chat_scroll.scroll_to(percent=1.0)


                # Input Area (Static at bottom of flex column)
                with ui.row().classes('w-full items-center p-4 bg-white border-t'):
                    ui.button(icon='folder', on_click=on_scan_dir).props('flat round').tooltip('添加目录上下文')
                    text_input = ui.input(placeholder='输入计划 (例如: 每日备份 /data)').classes('w-full flex-grow').on('keydown.enter', on_send)
                    ui.button(icon='send', on_click=on_send)

        # --- Tab 2: Backup Wizard ---
        with ui.tab_panel(backup_tab):
            ui.markdown("## 备份向导")
            with ui.stepper().props('vertical').classes('w-full') as stepper:
                with ui.step('选择内容'):
                    ui.label('要备份哪些文件?')
                    ui.input('源目录', value='/var/www/html')
                    with ui.stepper_navigation():
                        ui.button('下一步', on_click=stepper.next)
                with ui.step('选择目的地'):
                    ui.label('备份到哪里?')
                    ui.input('目标目录', value='/backup/weekly')
                    with ui.stepper_navigation():
                        ui.button('下一步', on_click=stepper.next)
                        ui.button('上一步', on_click=stepper.previous).props('flat')
                with ui.step('确认并测试'):
                    ui.label('将模拟备份过程...')
                    progress = ui.linear_progress(value=0).classes('w-full')
                    status_label = ui.label('准备就绪')
                    async def run_backup_test():
                        progress.value = 0
                        status_label.text = "正在扫描文件..."
                        await asyncio.sleep(0.5)
                        steps = 10
                        for i in range(steps):
                            await asyncio.sleep(0.2) 
                            progress.value = (i + 1) / steps
                            status_label.text = f"正在复制文件 ({i+1}/{steps})..."
                        status_label.text = "备份测试完成! (Dry Run)"
                        ui.notify('备份测试成功', type='positive')
                    with ui.stepper_navigation():
                        ui.button('开始测试', on_click=run_backup_test)
                        ui.button('上一步', on_click=stepper.previous).props('flat')

        # --- Tab 3: Settings ---
        with ui.tab_panel(settings_tab):
            ui.markdown("## AI 配置")
            
            # Model Options
            model_options = {
                "ollama/llama3": "Ollama (Llama 3)",
                "ollama/mistral": "Ollama (Mistral)",
                "common/command-r": "Ollama (Command R)",
                "openai/gpt-4o": "OpenAI (GPT-4o)",
                "openai/gpt-3.5-turbo": "OpenAI (GPT-3.5 Turbo)",
                "anthropic/claude-3-opus-20240229": "Anthropic (Claude 3 Opus)",
                "anthropic/claude-3-sonnet-20240229": "Anthropic (Claude 3 Sonnet)",
                "gemini/gemini-2.0-flash": "Google (Gemini 2.0 Flash) [Quota?]",
                "gemini/gemini-2.5-flash": "Google (Gemini 2.5 Flash) [New!]",
                "gemini/gemini-2.0-flash-exp": "Google (Gemini 2.0 Flash Exp)",
                "gemini/gemini-flash-latest": "Google (Gemini Flash Latest)",
                "gemini/gemini-pro-latest": "Google (Gemini Pro Latest)",
                "gemini/models/gemini-1.5-flash-latest": "Google (Gemini 1.5 Flash Latest)",
                "deepseek/deepseek-chat": "DeepSeek (Chat)",
                "xai/grok-beta": "xAI (Grok)",
                "groq/llama3-70b-8192": "Groq (Llama 3 70B)",
                "mock": "Mock (Testing)"
            }
            
            api_base_input = ui.input('API Base URL', value=app_config['api_base']).bind_value(app_config, 'api_base').classes('w-full')
            
            def on_model_change(e):
                val = e.value
                if "ollama" in val:
                    api_base_input.value = "http://localhost:11434"
                elif "openai" in val:
                    api_base_input.value = "https://api.openai.com/v1"
                elif "anthropic" in val:
                    api_base_input.value = "https://api.anthropic.com/v1"
                elif "gemini" in val:
                    # Native Litellm support for Gemini doesn't need a base URL (it uses google.generativeai)
                    api_base_input.value = "" 
                elif "deepseek" in val:
                    api_base_input.value = "https://api.deepseek.com"
                elif "xai" in val:
                    api_base_input.value = "https://api.x.ai/v1"
                elif "groq" in val:
                    api_base_input.value = "https://api.groq.com/openai/v1"
                elif "mock" in val:
                    api_base_input.value = "mock"
                
                app_config['model'] = val

            ui.select(model_options, value=app_config['model'], label='Model Selection', on_change=on_model_change).bind_value(app_config, 'model').classes('w-full')
            # api_base_input rendered above to be accessible in scope
            
            ui.input('API Key', value=app_config['api_key'], password=True).bind_value(app_config, 'api_key').classes('w-full')
            ui.button('保存配置 (Memory Only)', on_click=lambda: ui.notify('配置已更新 (仅本次会话有效)')).classes('mt-4')

@ui.page('/test')
def test_page():
    ui.label('Test Page Works!')

def start_web(port=8080):
    print(f"Starting Web UI on port {port}...")
    ui.run(title='ai-cron Web', port=port, show=False, reload=False, host='127.0.0.1')

if __name__ in {"__main__", "__mp_main__"}:
    start_web()
