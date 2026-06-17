#!/usr/bin/env python3
"""
Вспомогательный модуль для чтения конфигурации окружения из envs.json
"""

import json
import os
from pathlib import Path

def get_build_config():
    """Получает конфигурацию build_html для текущего окружения"""
    project_root = Path(__file__).parent.parent
    envs_path = project_root / "envs.json"
    
    # Определяем окружение из переменной окружения или используем prd по умолчанию
    env = os.environ.get("BUILD_ENV", "prd")
    
    if not envs_path.exists():
        # Если файл не существует, возвращаем значения по умолчанию
        return {
            "base_url": "",
            "minify": False,
            "cache_bust": True
        }
    
    try:
        with open(envs_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if env not in config:
            env = "prd"  # Fallback на prd
        
        return config[env].get("build_html", {})
    except Exception as e:
        print(f"Warning: Could not read envs.json: {e}")
        return {
            "base_url": "",
            "minify": False,
            "cache_bust": True
        }

def get_base_url():
    """Получает base_url из конфигурации"""
    config = get_build_config()
    return config.get("base_url", "")

def should_minify():
    """Проверяет нужно ли минифицировать файлы"""
    config = get_build_config()
    return config.get("minify", False)

def should_cache_bust():
    """Проверяет нужно ли добавлять cache busting"""
    config = get_build_config()
    return config.get("cache_bust", True)

def get_cache_bust_suffix():
    """Возвращает суффикс для cache busting (например, ?v=123)"""
    if should_cache_bust():
        import time
        return f"?v={int(time.time())}"
    return ""
