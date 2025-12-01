document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('rtd-search-form');
    const searchInput = searchForm.querySelector('input[name="q"]');

    // Create results container
    const resultsContainer = document.createElement('div');
    resultsContainer.id = 'modern-search-results';
    resultsContainer.style.display = 'none';
    searchForm.appendChild(resultsContainer);

    let searchIndex = [];
    let isIndexLoaded = false;

    // Check for highlight param and scroll/highlight
    const urlParams = new URLSearchParams(window.location.search);
    const highlightParam = urlParams.get('highlight');
    if (highlightParam) {
        highlightPageContent(highlightParam);
    }

    // Load index
    async function loadIndex() {
        if (isIndexLoaded) return;
        try {
            const contentRoot = document.documentElement.dataset.content_root || './';
            const response = await fetch(contentRoot + 'search_index.json');
            searchIndex = await response.json();
            isIndexLoaded = true;
            console.log('Search index loaded:', searchIndex.length, 'pages');
        } catch (error) {
            console.error('Failed to load search index:', error);
        }
    }

    // Search function
    function performSearch(query) {
        if (!query || query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }

        const lowerQuery = query.toLowerCase();
        const results = searchIndex.filter(page => {
            return page.title.toLowerCase().includes(lowerQuery) ||
                page.content.toLowerCase().includes(lowerQuery);
        });

        displayResults(results, query);
    }

    // Display results
    function displayResults(results, query) {
        resultsContainer.innerHTML = '';

        if (results.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'search-result-item no-results';
            noResults.textContent = 'Ничего не найдено';
            resultsContainer.appendChild(noResults);
        } else {
            // Sort results by lesson number
            results.sort((a, b) => {
                const getNum = (str) => {
                    const match = str.match(/^(\d+)\./);
                    return match ? parseInt(match[1], 10) : 9999;
                };
                return getNum(a.title) - getNum(b.title);
            });

            // Helper to highlight text in dropdown
            const highlightText = (text, term) => {
                if (!term) return text;
                const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
                return text.replace(regex, '<span class="search-highlight">$1</span>');
            };

            results.slice(0, 10).forEach(page => {
                const item = document.createElement('a');
                item.className = 'search-result-item';
                // Add highlight param to URL
                const separator = page.link.includes('?') ? '&' : '?';
                const contentRoot = document.documentElement.dataset.content_root || './';
                const relativeLink = page.link.startsWith('/') ? page.link.substring(1) : page.link;
                item.href = `${contentRoot}${relativeLink}${separator}highlight=${encodeURIComponent(query)}`;

                const title = document.createElement('div');
                title.className = 'search-result-title';
                title.innerHTML = highlightText(page.title, query);

                const snippet = document.createElement('div');
                snippet.className = 'search-result-snippet';

                // Create a simple snippet
                const contentLower = page.content.toLowerCase();
                const queryIndex = contentLower.indexOf(query.toLowerCase());
                let snippetText = page.content.substring(0, 100) + '...';

                if (queryIndex > -1) {
                    const start = Math.max(0, queryIndex - 40);
                    const end = Math.min(page.content.length, queryIndex + 60);
                    snippetText = (start > 0 ? '...' : '') +
                        page.content.substring(start, end) +
                        (end < page.content.length ? '...' : '');
                }
                snippet.innerHTML = highlightText(snippetText, query);

                item.appendChild(title);
                item.appendChild(snippet);
                resultsContainer.appendChild(item);
            });
        }

        resultsContainer.style.display = 'block';
    }

    // Highlight content on page
    function highlightPageContent(term) {
        if (!term) return;

        // We want to highlight in the main content area
        const contentArea = document.querySelector('div[itemprop="articleBody"]') || document.body;

        // Simple recursive find and replace text nodes
        // Note: This is a basic implementation. For complex HTML it might need a library like Mark.js
        // But for this static site it should be sufficient.

        const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');

        function traverse(node) {
            if (node.nodeType === 3) { // Text node
                const match = node.data.match(regex);
                if (match) {
                    const span = document.createElement('span');
                    span.innerHTML = node.data.replace(regex, '<span class="search-highlight" id="search-match-first">$1</span>');
                    // We add an ID to the first match to scroll to it
                    // But we need to be careful not to add ID to all.
                    // Let's just use class and scroll to first element with class.
                    node.parentNode.replaceChild(span, node);
                }
            } else if (node.nodeType === 1 && node.nodeName !== 'SCRIPT' && node.nodeName !== 'STYLE') {
                for (let i = 0; i < node.childNodes.length; i++) {
                    traverse(node.childNodes[i]);
                }
            }
        }

        traverse(contentArea);

        // Scroll to first match
        const firstMatch = document.querySelector('.search-highlight');
        if (firstMatch) {
            firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    // Event listeners
    searchInput.addEventListener('focus', loadIndex);

    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value);
    });

    // Close results ONLY on Esc
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            resultsContainer.style.display = 'none';
            searchInput.blur();
        }
    });

    // Prevent default form submission
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
    });
});
