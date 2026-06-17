// Search functionality for vocabulary

class VocabularySearch {
    constructor() {
        this.vocabulary = [];
        this.filteredVocabulary = [];
        this.searchInput = null;
        this.suggestionsContainer = null;
        this.resultsContainer = null;
        this.selectedIndex = -1;
        this.init();
    }

    async init() {
        // Setup DOM elements first
        this.searchInput = document.getElementById('search-input');
        this.suggestionsContainer = document.getElementById('search-suggestions');
        this.resultsContainer = document.getElementById('vocabulary-results');
        
        // Show loading state
        if (this.resultsContainer) {
            this.resultsContainer.innerHTML = `
                <div class="loading">
                    <p>Loading vocabulary...</p>
                </div>
            `;
        }
        
        // Load vocabulary data
        // Сначала проверяем, есть ли встроенные данные (для standalone версии)
        if (window.EMBEDDED_VOCABULARY && Array.isArray(window.EMBEDDED_VOCABULARY)) {
            console.log('Using embedded vocabulary data');
            this.vocabulary = window.EMBEDDED_VOCABULARY;
            this.filteredVocabulary = [...this.vocabulary];
            console.log(`Loaded ${this.vocabulary.length} vocabulary entries (embedded)`);
            this.onDataLoaded();
            return;
        }
        
        // Иначе загружаем через fetch
        try {
            const dataPath = 'data/vocabulary.json';
            console.log('Loading vocabulary from:', dataPath);
            const response = await fetch(dataPath);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.vocabulary = await response.json();
            this.filteredVocabulary = [...this.vocabulary];
            console.log(`Loaded ${this.vocabulary.length} vocabulary entries`);
            
            // Вызываем отрисовку после загрузки данных
            this.onDataLoaded();
        } catch (error) {
            console.error('Error loading vocabulary:', error);
            console.error('Error details:', {
                message: error.message,
                protocol: window.location.protocol,
                pathname: window.location.pathname
            });
            
            if (this.resultsContainer) {
                const isFileProtocol = window.location.protocol === 'file:';
                const errorMsg = isFileProtocol 
                    ? `<div class="empty-state">
                        <p><strong>Error loading vocabulary data.</strong></p>
                        <p>This happens when opening HTML files directly (file:// protocol).</p>
                        <p><strong>Solution 1:</strong> Use a local web server:</p>
                        <pre style="background: #f0f0f0; padding: 1rem; margin: 1rem 0; border-radius: 4px; text-align: left; display: inline-block;">
cd html
python3 -m http.server 8000
</pre>
                        <p>Then open <a href="http://localhost:8000">http://localhost:8000</a></p>
                        <p><strong>Solution 2:</strong> Use <a href="index_standalone.html">index_standalone.html</a> which has embedded data.</p>
                        <p><strong>Error:</strong> ${error.message}</p>
                    </div>`
                    : `<div class="empty-state">
                        <p>Error loading vocabulary data.</p>
                        <p><strong>Error:</strong> ${error.message}</p>
                        <p>Please check that data/vocabulary.json exists and is accessible.</p>
                    </div>`;
                
                this.resultsContainer.innerHTML = errorMsg;
            }
            return;
        }

        // Setup search input handlers
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

        // Initial render - вызываем после загрузки данных
        // renderResults будет вызван после успешной загрузки в init()
    }
    
    // Метод для вызова после загрузки данных
    onDataLoaded() {
        if (this.vocabulary.length > 0) {
            this.filteredVocabulary = [...this.vocabulary];
            this.renderResults();
        }
    }

    handleSearch(query) {
        const searchTerm = query.toLowerCase().trim();
        
        if (searchTerm.length === 0) {
            this.filteredVocabulary = [...this.vocabulary];
            this.hideSuggestions();
        } else {
            // Filter vocabulary
            this.filteredVocabulary = this.vocabulary.filter(item => {
                const english = (item.english || '').toLowerCase();
                const avar = (item.avar || '').toLowerCase();
                const arabic = (item.arabic || '').toLowerCase();
                const type = (item.type || '').toLowerCase();
                
                return english.includes(searchTerm) ||
                       avar.includes(searchTerm) ||
                       arabic.includes(searchTerm) ||
                       type.includes(searchTerm);
            });

            // Show suggestions
            this.showSuggestions();
        }

        this.renderResults();
    }

    showSuggestions() {
        if (!this.suggestionsContainer || this.filteredVocabulary.length === 0) {
            this.hideSuggestions();
            return;
        }

        const query = this.searchInput.value.toLowerCase().trim();
        if (query.length === 0) {
            this.hideSuggestions();
            return;
        }

        // Get top 10 suggestions
        const suggestions = this.filteredVocabulary.slice(0, 10);
        
        this.suggestionsContainer.innerHTML = suggestions.map((item, index) => {
            const english = this.highlight(item.english, query);
            const avar = item.avar ? ` - ${item.avar}` : '';
            return `
                <div class="suggestion-item" data-index="${index}" onclick="vocabSearch.selectSuggestion(${index})">
                    <strong>${english}</strong>${avar}
                </div>
            `;
        }).join('');

        this.suggestionsContainer.classList.add('show');
        this.selectedIndex = -1;
    }

    hideSuggestions() {
        if (this.suggestionsContainer) {
            this.suggestionsContainer.classList.remove('show');
        }
        this.selectedIndex = -1;
    }

    highlight(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    handleKeyDown(e) {
        if (!this.suggestionsContainer.classList.contains('show')) {
            return;
        }

        const suggestions = this.suggestionsContainer.querySelectorAll('.suggestion-item');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            this.selectedIndex = Math.min(this.selectedIndex + 1, suggestions.length - 1);
            this.updateSelection(suggestions);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
            this.updateSelection(suggestions);
        } else if (e.key === 'Enter' && this.selectedIndex >= 0) {
            e.preventDefault();
            this.selectSuggestion(this.selectedIndex);
        } else if (e.key === 'Escape') {
            this.hideSuggestions();
        }
    }

    updateSelection(suggestions) {
        suggestions.forEach((item, index) => {
            if (index === this.selectedIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('selected');
            }
        });
    }

    selectSuggestion(index) {
        const item = this.filteredVocabulary[index];
        if (item) {
            this.searchInput.value = item.english;
            this.handleSearch(item.english);
            this.hideSuggestions();
            // Scroll to the result
            const resultElement = document.querySelector(`[data-vocab-id="${index}"]`);
            if (resultElement) {
                resultElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }

    renderResults() {
        if (!this.resultsContainer) return;

        // Если словарь еще не загружен
        if (this.vocabulary.length === 0) {
            this.resultsContainer.innerHTML = `
                <div class="loading">
                    <p>Loading vocabulary...</p>
                </div>
            `;
            return;
        }

        if (this.filteredVocabulary.length === 0) {
            this.resultsContainer.innerHTML = `
                <div class="empty-state">
                    <p>No results found. Try a different search term.</p>
                </div>
            `;
            return;
        }

        this.resultsContainer.innerHTML = this.filteredVocabulary.map((item, index) => {
            const type = item.type ? `<span class="vocab-type">${item.type}</span>` : '';
            const avar = item.avar ? `<div class="vocab-avar">${item.avar}</div>` : '';
            const arabic = item.arabic ? `<div class="vocab-arabic">${item.arabic}</div>` : '';
            
            return `
                <div class="vocabulary-item" data-vocab-id="${index}">
                    <div class="vocab-english">${item.english}${type}</div>
                    ${avar}
                    ${arabic}
                </div>
            `;
        }).join('');
    }
}

// Initialize search when DOM is ready
let vocabSearch;
document.addEventListener('DOMContentLoaded', () => {
    vocabSearch = new VocabularySearch();
});
