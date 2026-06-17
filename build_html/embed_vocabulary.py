#!/usr/bin/env python3
"""
Создает версию index.html с встроенными данными словаря
Это обходит проблему CORS при открытии через file://
"""

import json
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent
    
    # Читаем vocabulary.json
    vocab_path = project_root / "docs" / "data" / "vocabulary.json"
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)
    
    # Читаем index.html
    index_path = project_root / "docs" / "index.html"
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Встраиваем данные в JavaScript
    vocab_json = json.dumps(vocabulary, ensure_ascii=False)
    
    # Находим место для вставки (перед закрывающим тегом body или перед script search.js)
    script_tag = '<script src="js/search.js"></script>'
    
    # Создаем встроенный скрипт с данными
    embedded_data_script = f'''<script>
        // Embedded vocabulary data to avoid CORS issues
        window.EMBEDDED_VOCABULARY = {vocab_json};
    </script>'''
    
    override_script = '''<script>
        // Override VocabularySearch to use embedded data
        document.addEventListener('DOMContentLoaded', function() {
            if (window.EMBEDDED_VOCABULARY && typeof VocabularySearch !== 'undefined') {
                const originalInit = VocabularySearch.prototype.init;
                VocabularySearch.prototype.init = async function() {
                    // Setup DOM elements first
                    this.searchInput = document.getElementById('search-input');
                    this.suggestionsContainer = document.getElementById('search-suggestions');
                    this.resultsContainer = document.getElementById('vocabulary-results');
                    
                    // Show loading state
                    if (this.resultsContainer) {
                        this.resultsContainer.innerHTML = '<div class="loading"><p>Loading vocabulary...</p></div>';
                    }
                    
                    // Use embedded data instead of fetch
                    this.vocabulary = window.EMBEDDED_VOCABULARY;
                    this.filteredVocabulary = [...this.vocabulary];
                    console.log('Loaded ' + this.vocabulary.length + ' vocabulary entries (embedded)');
                    
                    // Setup event handlers
                    if (this.searchInput) {
                        this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
                        this.searchInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
                        this.searchInput.addEventListener('focus', () => {
                            if (this.searchInput.value) {
                                this.showSuggestions();
                            }
                        });
                    }
                    
                    // Hide suggestions when clicking outside
                    document.addEventListener('click', (e) => {
                        if (this.searchInput && this.suggestionsContainer &&
                            !this.searchInput.contains(e.target) && 
                            !this.suggestionsContainer.contains(e.target)) {
                            this.hideSuggestions();
                        }
                    });
                    
                    // Render results
                    this.onDataLoaded();
                };
            }
        });
    </script>'''
    
    embedded_script = embedded_data_script + '\n    ' + script_tag + '\n    ' + override_script
    
    # Заменяем script tag
    new_html = html_content.replace(script_tag, embedded_script)
    
    # Сохраняем как index_standalone.html
    standalone_path = project_root / "docs" / "index_standalone.html"
    with open(standalone_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Создан файл {standalone_path}")
    print("Этот файл можно открывать напрямую в браузере без веб-сервера")
    print(f"Размер: {len(vocab_json)} символов данных")

if __name__ == "__main__":
    main()
