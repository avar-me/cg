#!/usr/bin/env python3
"""
Создание заглушек для разделов Grammar
"""

from pathlib import Path

GRAMMAR_SECTIONS = [
    ('numerals.html', '4A. The Numerals', 'The Numerals'),
    ('substantive.html', '4B. The Substantive', 'The Substantive'),
    ('plural.html', '4C. The Formation of the Plural', 'The Formation of the Plural'),
    ('declension.html', '4D. Declension of the Substantive', 'Declension of the Substantive'),
    ('declension-tables.html', '4E. Tables of the Declensions of the Substantive', 'Tables of the Declensions of the Substantive'),
    ('adjective.html', '4F. The Adjective', 'The Adjective'),
    ('pronouns.html', '4G. Pronouns', 'Pronouns'),
    ('verbs.html', '4H. The Verbs', 'The Verbs'),
    ('prepositions.html', '4I1. Prepositions', 'Prepositions'),
    ('conjunctions.html', '4I2. Conjunctions', 'Conjunctions'),
    ('interjections.html', '4I3. Interjections', 'Interjections'),
    ('end.html', '5. The End', 'The End'),
]

def create_grammar_page(filename, title, heading):
    """Создает HTML страницу для раздела Grammar"""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - The Avâr Language</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>The Avâr Language</h1>
            <p>Vocabulary compiled by Cyril Graham, Royal Asiatic Society, 1881</p>
        </div>
    </header>

    <nav>
        <div class="container">
            <ul>
                <li><a href="../index.html">Vocabulary</a></li>
                <li><a href="../about.html">About</a></li>
                <li><a href="../alphabet.html">Alphabet</a></li>
                <li><a href="index.html">Grammar</a></li>
            </ul>
        </div>
    </nav>

    <main>
        <div class="container">
            <div class="content-section">
                <h2>{heading}</h2>
                
                <p>
                    This section will contain the content for <strong>{title}</strong>. 
                    The content will be populated after parsing the PDF document.
                </p>
                
                <p>
                    <a href="index.html">← Back to Grammar Index</a>
                </p>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2026 The Avar Me Project | <a href="mailto:admin@avar.me">admin@avar.me</a></p>
        </div>
    </footer>
</body>
</html>'''
    return html

def main():
    project_root = Path(__file__).parent.parent
    grammar_dir = project_root / "docs" / "grammar"
    grammar_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, title, heading in GRAMMAR_SECTIONS:
        filepath = grammar_dir / filename
        html = create_grammar_page(filename, title, heading)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Создан файл {filepath}")

if __name__ == "__main__":
    main()
