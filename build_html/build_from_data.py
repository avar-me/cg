#!/usr/bin/env python3
"""
Сборка HTML из данных в папке data/
Читает JSON файлы из data/ и собирает HTML страницы
"""

import json
import re
from pathlib import Path

def format_text_as_html(text):
    """Форматирует текст в HTML параграфы"""
    if not text:
        return ""
    
    # Разбиваем на параграфы по двойным переносам строк
    paragraphs = text.split('\n\n')
    
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # Если это заголовок (все заглавные и короткий)
        if para.isupper() and len(para) < 100:
            html_paragraphs.append(f'<h3>{para.title()}</h3>')
        else:
            # Обычный параграф
            # Заменяем одинарные переносы на <br>
            para = para.replace('\n', '<br>')
            html_paragraphs.append(f'<p>{para}</p>')
    
    return '\n'.join(html_paragraphs)

def build_about_page():
    """Собирает страницу About из data/about/"""
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "about" / "introduction.json"
    template_path = project_root / "build_html" / "templates" / "about.html"
    html_path = project_root / "docs" / "about.html"
    
    if not data_path.exists():
        print(f"  Warning: {data_path} not found, skipping About page")
        return
    
    if not template_path.exists():
        print(f"  Warning: {template_path} not found, skipping About page")
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Читаем шаблон HTML
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Собираем контент из секций
    sections_html = []
    for section in data.get('sections', []):
        title = section.get('title', '')
        content = section.get('content', '')
        
        if title:
            sections_html.append(f'<h3>{title}</h3>')
        if content:
            sections_html.append(format_text_as_html(content))
    
    content_html = '\n'.join(sections_html)
    
    # Добавляем информацию об источнике
    source_html = f'''
                <h3>Source</h3>
                <p>
                    {data.get('source', '')}<br>
                    {data.get('article_number', '')} — {data.get('title', '')} by {data.get('author', '')}
                </p>
    '''
    
    # Заменяем контент в HTML
    pattern = r'(<div class="content-section">\s*<h2>The Avâr Language</h2>\s*)(.*?)(\s*</div>\s*</div>\s*</main>)'
    
    replacement = f'\\1\n                {content_html}\n                {source_html}\n                \\3'
    
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Сохраняем
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"  Built about.html from data/about/introduction.json")

def build_alphabet_page():
    """Собирает страницу Alphabet из data/alphabet/"""
    import unicodedata
    
    project_root = Path(__file__).parent.parent
    template_path = project_root / "build_html" / "templates" / "alphabet.html"
    correspondence_path = project_root / "data" / "alphabet" / "correspondence.json"
    content_path = project_root / "data" / "alphabet" / "content.json"
    
    # Загружаем данные из correspondence.json
    correspondence_data = {}
    
    if correspondence_path.exists():
        with open(correspondence_path, 'r', encoding='utf-8') as f:
            correspondence_data = json.load(f)
    
    # Загружаем текст из content.json
    content_data = {}
    if content_path.exists():
        with open(content_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    
    # Получаем соответствия и проверяем структуру
    correspondences = correspondence_data.get('correspondences', [])
    
    # Если данные в старой структуре (с полем 'latin'), преобразуем их
    # НО только если нет полей latin_upper и latin_lower
    if correspondences and 'latin_upper' not in correspondences[0]:
        def get_upper_lower(latin_str):
            if not latin_str:
                return '', ''
            if len(latin_str) > 1 and latin_str[0].isupper():
                return latin_str, latin_str.lower()
            char = latin_str[0]
            try:
                name = unicodedata.name(char)
                if 'CAPITAL' in name:
                    try:
                        lower_name = name.replace('CAPITAL', 'SMALL')
                        lower_char = unicodedata.lookup(lower_name)
                        return char, lower_char
                    except:
                        return char, char.lower()
                elif 'SMALL' in name:
                    try:
                        upper_name = name.replace('SMALL', 'CAPITAL')
                        upper_char = unicodedata.lookup(upper_name)
                        return upper_char, char
                    except:
                        return char.upper(), char
                return char, char.lower()
            except:
                return char.upper(), char.lower()
        
        # Преобразуем старую структуру в новую
        new_correspondences = []
        for corr in correspondences:
            latin = corr.get('latin', '')
            upper, lower = get_upper_lower(latin)
            new_correspondences.append({
                'arabic': corr.get('arabic', ''),
                'latin_upper': upper,
                'latin_lower': lower,
                'description': corr.get('description', '')
            })
        correspondences = new_correspondences
    
    # Если данные уже в правильной структуре, используем их как есть
    # НЕ перезаписываем существующие значения!
    
    # Генерируем данные для таблицы Latin Alphabet с Unicode информацией
    seen = set()
    latin_chars = []
    
    for corr in correspondences:
        # Добавляем заглавную версию
        if corr.get('latin_upper') and corr['latin_upper'] not in seen:
            seen.add(corr['latin_upper'])
            char = corr['latin_upper'][0] if corr['latin_upper'] else ''
            if char:
                try:
                    unicode_name = unicodedata.name(char)
                    unicode_category = unicodedata.category(char)
                except:
                    unicode_name = 'UNKNOWN'
                    unicode_category = '?'
                
                latin_chars.append({
                    'char': corr['latin_upper'],
                    'unicode': f"U+{ord(char):04X}",
                    'name': unicode_name,
                    'category': unicode_category,
                    'description': corr.get('description', '')
                })
        
        # Добавляем строчную версию, если она отличается
        if corr.get('latin_lower') and corr['latin_lower'] != corr.get('latin_upper', '') and corr['latin_lower'] not in seen:
            seen.add(corr['latin_lower'])
            char = corr['latin_lower'][0] if corr['latin_lower'] else ''
            if char:
                try:
                    unicode_name = unicodedata.name(char)
                    unicode_category = unicodedata.category(char)
                except:
                    unicode_name = 'UNKNOWN'
                    unicode_category = '?'
                
                latin_chars.append({
                    'char': corr['latin_lower'],
                    'unicode': f"U+{ord(char):04X}",
                    'name': unicode_name,
                    'category': unicode_category,
                    'description': corr.get('description', '')
                })
    
    # Сохраняем в docs/data/alphabet.json для использования JavaScript
    output_data = {
        'correspondence': correspondences,
        'latin': latin_chars,
        'source_pages': correspondence_data.get('source_pages', []),
        # Добавляем текст из content.json
        'introduction': content_data.get('introduction', ''),
        'main_text_before_table': content_data.get('main_text_before_table', ''),
        'main_text_after_table': content_data.get('main_text_after_table', ''),
        'notes': content_data.get('notes', ''),
        'full_text': content_data.get('full_text', ''),
        # Добавляем новые поля для согласных и гласных
        'consonants_before_table': content_data.get('Consonats_before_table', ''),
        'consonants_after_table': content_data.get('Consonats_after_table', ''),
        'vowels_before_table': content_data.get('Vowels_before_table', '')
    }
    
    # Сохраняем JSON
    json_output_path = project_root / "docs" / "data" / "alphabet.json"
    json_output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"  Built alphabet.json from data/alphabet/")

def build_grammar_pages():
    """Собирает страницы Grammar из data/grammar/"""
    project_root = Path(__file__).parent.parent
    grammar_dir = project_root / "data" / "grammar"
    html_grammar_dir = project_root / "docs" / "grammar"
    
    if not grammar_dir.exists():
        print(f"  Warning: {grammar_dir} not found, skipping Grammar pages")
        return
    
    # Маппинг файлов на HTML страницы
    grammar_files = {
        'numerals.json': 'numerals.html',
        'substantive.json': 'substantive.html',
        'plural.json': 'plural.html',
        'declension.json': 'declension.html',
        'declension-tables.json': 'declension-tables.html',
        'adjective.json': 'adjective.html',
        'pronouns.json': 'pronouns.html',
        'verbs.json': 'verbs.html',
        'prepositions.json': 'prepositions.html',
        'conjunctions.json': 'conjunctions.html',
        'interjections.json': 'interjections.html',
        'end.json': 'end.html'
    }
    
    for json_file, html_file in grammar_files.items():
        json_path = grammar_dir / json_file
        html_path = html_grammar_dir / html_file
        
        if not json_path.exists():
            continue
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Читаем шаблон HTML (используем файл, созданный build_grammar.py)
        # build_grammar.py создает базовые HTML файлы из шаблона, которые мы затем заполняем контентом
        if not html_path.exists():
            continue
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Собираем контент
        content_html = ""

        # Топ-уровневое intro (текст или HTML), если есть
        if data.get('intro'):
            content_html += format_text_as_html(data['intro']) + '\n'
        if data.get('intro_html'):
            content_html += data['intro_html'] + '\n'

        if 'sections' in data:
            # Если есть секции
            for section in data['sections']:
                title = section.get('title', '')
                section_id = section.get('id', '')

                if title:
                    if section_id:
                        content_html += f'<h3 id="{section_id}">{title}</h3>\n'
                    else:
                        content_html += f'<h3>{title}</h3>\n'

                # content (text prose) идет первым — обычно вводит тему/таблицу
                if section.get('content'):
                    content_html += format_text_as_html(section['content']) + '\n'
                # body — сырой HTML (таблицы и т.п.), рендерится как есть
                if section.get('body'):
                    content_html += section['body'] + '\n'
        elif data.get('body'):
            content_html += data['body']
        elif 'content' in data:
            # Если просто контент
            content_html = format_text_as_html(data['content'])

        # Концевая нота (текст или HTML)
        if data.get('outro'):
            content_html += format_text_as_html(data['outro']) + '\n'
        if data.get('outro_html'):
            content_html += data['outro_html'] + '\n'
        
        # Заменяем контент
        pattern = r'(<div class="content-section">\s*<h2>.*?</h2>\s*)(.*?)(\s*<p>\s*<a href="index.html">← Back to Grammar Index</a>\s*</p>\s*</div>)'
        
        replacement = f'\\1\n                {content_html}\n                \\3'
        
        new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # Сохраняем
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"  Built {html_file} from data/grammar/{json_file}")

def main():
    print("Building HTML from data/ directory...")
    
    build_about_page()
    build_alphabet_page()
    build_grammar_pages()
    
    print("Build from data/ complete!")

if __name__ == "__main__":
    main()
