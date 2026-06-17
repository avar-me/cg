#!/usr/bin/env python3
"""
Сборка vocabulary.json из файлов в data/vocabulary/
Читает JSON файлы по буквам и объединяет их в один vocabulary.json
"""

import json
from pathlib import Path

def build_vocabulary_from_data(data_dir):
    """Читает JSON файлы из data/vocabulary/ и объединяет их в один список"""
    data_dir = Path(data_dir)
    vocabulary = []
    
    # Читаем index.json для получения списка букв
    index_path = data_dir / "index.json"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        # Читаем файлы по буквам
        for letter in sorted(index_data.get('letters', [])):
            letter_file = data_dir / f"{letter}.json"
            if letter_file.exists():
                with open(letter_file, 'r', encoding='utf-8') as f:
                    letter_data = json.load(f)
                    entries = letter_data.get('entries', [])
                    vocabulary.extend(entries)
                    print(f"  Loaded {len(entries)} entries from {letter}.json")
    else:
        # Если нет index.json, ищем все JSON файлы
        for json_file in sorted(data_dir.glob("*.json")):
            if json_file.name == "index.json":
                continue
            with open(json_file, 'r', encoding='utf-8') as f:
                letter_data = json.load(f)
                entries = letter_data.get('entries', [])
                vocabulary.extend(entries)
                print(f"  Loaded {len(entries)} entries from {json_file.name}")
    
    return vocabulary

def main():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data" / "vocabulary"
    output_path = project_root / "docs" / "data" / "vocabulary.json"
    
    if not data_dir.exists():
        print(f"Error: {data_dir} not found")
        print("Run split_vocabulary.py first to create data/vocabulary/ structure")
        return
    
    print(f"Building vocabulary from {data_dir}...")
    vocabulary = build_vocabulary_from_data(data_dir)
    
    print(f"\nНайдено {len(vocabulary)} словарных статей")
    
    # Сохраняем в JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)
    
    print(f"Сохранено в {output_path}")
    
    # Выводим несколько примеров
    print("\nПримеры записей:")
    for entry in vocabulary[:5]:
        print(f"  {entry['english']} → {entry.get('avar', '')} ({entry.get('arabic', '')})")

if __name__ == "__main__":
    main()
