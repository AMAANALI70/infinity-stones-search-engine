// Infinity Stones Search Engine - JavaScript

class InfinitySearchApp {
    constructor() {
        this.selectedStone = null;
        this.searchResults = [];
        this.currentPage = 1;
        this.resultsPerPage = 12;
        this.analytics = {
            totalSearches: 0,
            searchTimes: [],
            stoneUsage: {},
            popularQueries: {}
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadAnalytics();
        this.animateStones();
        this.setupSearchSuggestions();
    }

    setupEventListeners() {
        // Stone selection
        document.querySelectorAll('.stone-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.selectStone(e.currentTarget.dataset.stone);
            });
        });

        // All stones button
        document.getElementById('allStonesBtn').addEventListener('click', () => {
            this.selectStone('all');
        });

        // Search functionality
        document.getElementById('searchBtn').addEventListener('click', () => {
            this.performSearch();
        });

        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });

        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchSection(e.currentTarget.dataset.section);
            });
        });

        // Modal
        document.getElementById('closeModal').addEventListener('click', () => {
            this.closeModal();
        });

        // Filters
        document.getElementById('sortBy').addEventListener('change', () => {
            this.sortResults();
        });

        document.getElementById('categoryFilter').addEventListener('change', () => {
            this.filterResults();
        });

        // Close modal on outside click
        document.getElementById('productModal').addEventListener('click', (e) => {
            if (e.target.id === 'productModal') {
                this.closeModal();
            }
        });
    }

    selectStone(stoneType) {
        // Remove active class from all stones
        document.querySelectorAll('.stone-card').forEach(card => {
            card.classList.remove('active');
        });

        // Add active class to selected stone or all stones button
        if (stoneType === 'all') {
            document.getElementById('allStonesBtn').classList.add('active');
            this.selectedStone = null;
        } else {
            document.querySelector(`[data-stone="${stoneType}"]`).classList.add('active');
            this.selectedStone = stoneType;
        }

        // Animate stone selection
        this.animateStoneSelection(stoneType);
    }

    animateStoneSelection(stoneType) {
        const stones = document.querySelectorAll('.stone-card');
        stones.forEach((stone, index) => {
            if (stoneType === 'all' || stone.dataset.stone === stoneType) {
                setTimeout(() => {
                    stone.style.transform = 'scale(1.1)';
                    stone.style.boxShadow = '0 0 30px rgba(74, 144, 226, 0.5)';
                    
                    setTimeout(() => {
                        stone.style.transform = 'scale(1)';
                        stone.style.boxShadow = '';
                    }, 300);
                }, index * 100);
            }
        });
    }

    animateStones() {
        const stones = document.querySelectorAll('.stone-card');
        stones.forEach((stone, index) => {
            setTimeout(() => {
                stone.classList.add('fade-in');
            }, index * 200);
        });
    }

    async performSearch() {
        const query = document.getElementById('searchInput').value.trim();
        if (!query) {
            this.showNotification('Please enter a search query', 'warning');
            return;
        }

        this.showLoading();
        const startTime = performance.now();

        try {
            // Simulate API call (replace with actual backend call)
            const results = await this.simulateSearch(query);
            const endTime = performance.now();
            const searchTime = (endTime - startTime) / 1000;

            this.searchResults = results;
            this.displayResults(results);
            this.updateSearchStats(query, searchTime);
            this.hideLoading();

            // Show results section
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Search error:', error);
            this.showNotification('Search failed. Please try again.', 'error');
            this.hideLoading();
        }
    }

    async simulateSearch(query) {
        // This simulates the search engine results
        // In a real implementation, this would call your Python backend
        
        const mockResults = [
            {
                product_id: '1',
                product_data: {
                    'Brand': 'Sony',
                    'Type': 'Bluetooth Speaker',
                    'Model Number': 'SRS-XB23',
                    'Features': 'Waterproof, Extra Bass',
                    'Battery Life': '12 hours',
                    'Connectivity': 'Bluetooth 5.0'
                },
                relevance_score: 0.95,
                stone_powers: {
                    'space': 0.8,
                    'mind': 0.7,
                    'reality': 0.9,
                    'power': 0.85,
                    'time': 0.6,
                    'soul': 0.75
                },
                matched_fields: ['brand', 'type', 'features']
            },
            {
                product_id: '2',
                product_data: {
                    'Brand': 'JBL',
                    'Type': 'Wireless Headphones',
                    'Model Number': 'TUNE 750BTNC',
                    'Features': 'Noise Cancelling, 30h Battery',
                    'Connectivity': 'Bluetooth 5.0, 3.5mm'
                },
                relevance_score: 0.88,
                stone_powers: {
                    'space': 0.75,
                    'mind': 0.8,
                    'reality': 0.85,
                    'power': 0.9,
                    'time': 0.7,
                    'soul': 0.65
                },
                matched_fields: ['type', 'features', 'connectivity']
            },
            {
                product_id: '3',
                product_data: {
                    'Brand': 'Bose',
                    'Type': 'Smart Speaker',
                    'Model Number': 'Home Speaker 500',
                    'Features': 'Voice Control, Wi-Fi',
                    'Connectivity': 'Wi-Fi, Bluetooth, Ethernet'
                },
                relevance_score: 0.82,
                stone_powers: {
                    'space': 0.7,
                    'mind': 0.9,
                    'reality': 0.8,
                    'power': 0.75,
                    'time': 0.8,
                    'soul': 0.85
                },
                matched_fields: ['type', 'features', 'brand']
            }
        ];

        // Filter results based on query
        const filteredResults = mockResults.filter(result => {
            const searchText = query.toLowerCase();
            const productText = JSON.stringify(result.product_data).toLowerCase();
            return productText.includes(searchText);
        });

        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

        return filteredResults;
    }

    displayResults(results) {
        const resultsGrid = document.getElementById('resultsGrid');
        const resultsCount = document.getElementById('resultsCount');
        const searchTime = document.getElementById('searchTime');

        resultsCount.textContent = results.length;
        searchTime.textContent = (performance.now() / 1000).toFixed(3);

        if (results.length === 0) {
            resultsGrid.innerHTML = `
                <div class="no-results">
                    <h3>No results found</h3>
                    <p>Try adjusting your search terms or using a different stone power.</p>
                </div>
            `;
            return;
        }

        resultsGrid.innerHTML = results.map((result, index) => {
            const product = result.product_data;
            const stonePowers = result.stone_powers;
            
            return `
                <div class="result-card fade-in" style="animation-delay: ${index * 0.1}s" onclick="app.showProductDetails('${result.product_id}')">
                    <div class="result-header">
                        <span class="result-id">ID: ${result.product_id}</span>
                        <span class="relevance-score">${(result.relevance_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="result-content">
                        <div class="result-brand">${product.Brand || 'Unknown Brand'}</div>
                        <div class="result-type">${product.Type || 'Unknown Type'}</div>
                        <div class="result-model">${product['Model Number'] || 'No Model'}</div>
                    </div>
                    <div class="stone-powers">
                        ${Object.entries(stonePowers).map(([stone, power]) => 
                            `<span class="stone-power-badge ${stone}" title="${stone} stone power">${stone}: ${(power * 100).toFixed(0)}%</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }).join('');

        this.updateStonePowers(results);
    }

    updateStonePowers(results) {
        // Update stone power indicators based on search results
        const stoneCards = document.querySelectorAll('.stone-card');
        
        stoneCards.forEach(card => {
            const stoneType = card.dataset.stone;
            const powerBar = card.querySelector('.stone-power');
            
            // Calculate average power for this stone across all results
            const avgPower = results.reduce((sum, result) => {
                return sum + (result.stone_powers[stoneType] || 0);
            }, 0) / results.length;
            
            // Update power bar
            powerBar.style.setProperty('--power', `${avgPower * 100}%`);
            powerBar.querySelector('::after').style.width = `${avgPower * 100}%`;
        });
    }

    showProductDetails(productId) {
        const result = this.searchResults.find(r => r.product_id === productId);
        if (!result) return;

        const product = result.product_data;
        const modal = document.getElementById('productModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        const stonePowersDisplay = document.getElementById('stonePowersDisplay');

        modalTitle.textContent = `${product.Brand || 'Unknown'} - ${product.Type || 'Product'}`;
        
        modalBody.innerHTML = `
            <div class="product-details">
                <div class="detail-group">
                    <h4>Product Information</h4>
                    <div class="detail-grid">
                        ${Object.entries(product).map(([key, value]) => 
                            `<div class="detail-item">
                                <span class="detail-label">${key}:</span>
                                <span class="detail-value">${value || 'N/A'}</span>
                            </div>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;

        stonePowersDisplay.innerHTML = `
            <h4>Infinity Stone Powers</h4>
            <div class="stone-powers-grid">
                ${Object.entries(result.stone_powers).map(([stone, power]) => 
                    `<div class="stone-power-item">
                        <span class="stone-name">${stone.charAt(0).toUpperCase() + stone.slice(1)} Stone</span>
                        <div class="power-bar">
                            <div class="power-fill ${stone}" style="width: ${power * 100}%"></div>
                        </div>
                        <span class="power-value">${(power * 100).toFixed(1)}%</span>
                    </div>`
                ).join('')}
            </div>
        `;

        modal.style.display = 'flex';
        modal.classList.add('fade-in');
    }

    closeModal() {
        const modal = document.getElementById('productModal');
        modal.style.display = 'none';
        modal.classList.remove('fade-in');
    }

    sortResults() {
        const sortBy = document.getElementById('sortBy').value;
        let sortedResults = [...this.searchResults];

        switch (sortBy) {
            case 'relevance':
                sortedResults.sort((a, b) => b.relevance_score - a.relevance_score);
                break;
            case 'brand':
                sortedResults.sort((a, b) => (a.product_data.Brand || '').localeCompare(b.product_data.Brand || ''));
                break;
            case 'type':
                sortedResults.sort((a, b) => (a.product_data.Type || '').localeCompare(b.product_data.Type || ''));
                break;
        }

        this.displayResults(sortedResults);
    }

    filterResults() {
        const category = document.getElementById('categoryFilter').value;
        if (!category) {
            this.displayResults(this.searchResults);
            return;
        }

        const filteredResults = this.searchResults.filter(result => {
            const productType = (result.product_data.Type || '').toLowerCase();
            return productType.includes(category);
        });

        this.displayResults(filteredResults);
    }

    switchSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Show/hide sections
        document.getElementById('resultsSection').style.display = section === 'search' ? 'block' : 'none';
        document.getElementById('analyticsDashboard').style.display = section === 'analytics' ? 'block' : 'none';
        document.getElementById('aboutSection').style.display = section === 'about' ? 'block' : 'none';

        if (section === 'analytics') {
            this.updateAnalyticsDashboard();
        }
    }

    updateAnalyticsDashboard() {
        document.getElementById('totalSearches').textContent = this.analytics.totalSearches;
        
        const avgTime = this.analytics.searchTimes.length > 0 
            ? this.analytics.searchTimes.reduce((a, b) => a + b, 0) / this.analytics.searchTimes.length 
            : 0;
        document.getElementById('avgSearchTime').textContent = `${avgTime.toFixed(3)}s`;

        // Update stone usage chart
        this.updateStoneUsageChart();
        
        // Update popular queries
        this.updatePopularQueries();
        
        // Update category chart
        this.updateCategoryChart();
    }

    updateStoneUsageChart() {
        const chart = document.getElementById('stoneUsageChart');
        const stones = ['space', 'mind', 'reality', 'power', 'time', 'soul'];
        
        chart.innerHTML = stones.map(stone => {
            const usage = this.analytics.stoneUsage[stone] || 0;
            const percentage = this.analytics.totalSearches > 0 ? (usage / this.analytics.totalSearches) * 100 : 0;
            
            return `
                <div class="stone-usage-item">
                    <span class="stone-name">${stone.charAt(0).toUpperCase() + stone.slice(1)}</span>
                    <div class="usage-bar">
                        <div class="usage-fill ${stone}" style="width: ${percentage}%"></div>
                    </div>
                    <span class="usage-value">${usage}</span>
                </div>
            `;
        }).join('');
    }

    updatePopularQueries() {
        const container = document.getElementById('popularQueries');
        const queries = Object.entries(this.analytics.popularQueries)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5);
        
        container.innerHTML = queries.map(([query, count]) => 
            `<div class="query-item">
                <span class="query-text">"${query}"</span>
                <span class="query-count">${count} searches</span>
            </div>`
        ).join('');
    }

    updateCategoryChart() {
        const container = document.getElementById('categoryChart');
        const categories = {};
        
        this.searchResults.forEach(result => {
            const type = result.product_data.Type || 'Unknown';
            categories[type] = (categories[type] || 0) + 1;
        });
        
        const categoryEntries = Object.entries(categories)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5);
        
        container.innerHTML = categoryEntries.map(([category, count]) => 
            `<div class="category-item">
                <span class="category-name">${category}</span>
                <span class="category-count">${count}</span>
            </div>`
        ).join('');
    }

    updateSearchStats(query, searchTime) {
        this.analytics.totalSearches++;
        this.analytics.searchTimes.push(searchTime);
        this.analytics.popularQueries[query] = (this.analytics.popularQueries[query] || 0) + 1;
        
        if (this.selectedStone) {
            this.analytics.stoneUsage[this.selectedStone] = (this.analytics.stoneUsage[this.selectedStone] || 0) + 1;
        } else {
            this.analytics.stoneUsage['all'] = (this.analytics.stoneUsage['all'] || 0) + 1;
        }
    }

    setupSearchSuggestions() {
        const input = document.getElementById('searchInput');
        const suggestions = document.getElementById('searchSuggestions');
        
        const popularQueries = [
            'bluetooth speaker',
            'wireless headphones',
            'car vacuum',
            'beauty cream',
            'home furniture',
            'sports equipment',
            'smart watch',
            'laptop bag',
            'phone case',
            'gaming mouse'
        ];

        input.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            if (query.length < 2) {
                suggestions.style.display = 'none';
                return;
            }

            const matches = popularQueries.filter(q => q.includes(query));
            if (matches.length > 0) {
                suggestions.innerHTML = matches.map(match => 
                    `<div class="suggestion-item" onclick="app.selectSuggestion('${match}')">${match}</div>`
                ).join('');
                suggestions.style.display = 'block';
            } else {
                suggestions.style.display = 'none';
            }
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !suggestions.contains(e.target)) {
                suggestions.style.display = 'none';
            }
        });
    }

    selectSuggestion(suggestion) {
        document.getElementById('searchInput').value = suggestion;
        document.getElementById('searchSuggestions').style.display = 'none';
        this.performSearch();
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 2rem',
            borderRadius: '10px',
            color: 'white',
            fontWeight: '600',
            zIndex: '1001',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });

        // Set background color based on type
        const colors = {
            info: '#4A90E2',
            success: '#7ED321',
            warning: '#F5A623',
            error: '#D0021B'
        };
        notification.style.background = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    loadAnalytics() {
        // Load analytics from localStorage if available
        const saved = localStorage.getItem('infinitySearchAnalytics');
        if (saved) {
            this.analytics = { ...this.analytics, ...JSON.parse(saved) };
        }
    }

    saveAnalytics() {
        // Save analytics to localStorage
        localStorage.setItem('infinitySearchAnalytics', JSON.stringify(this.analytics));
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new InfinitySearchApp();
    
    // Save analytics periodically
    setInterval(() => {
        if (window.app) {
            window.app.saveAnalytics();
        }
    }, 30000); // Save every 30 seconds
});

// Add some additional CSS for dynamic elements
const additionalStyles = `
    .suggestion-item {
        padding: 0.5rem 1rem;
        cursor: pointer;
        border-bottom: 1px solid rgba(74, 144, 226, 0.2);
        transition: background-color 0.2s ease;
    }
    
    .suggestion-item:hover {
        background-color: rgba(74, 144, 226, 0.1);
    }
    
    .search-suggestions {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: rgba(26, 26, 46, 0.95);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 0 0 15px 15px;
        backdrop-filter: blur(10px);
        z-index: 100;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .stone-usage-item, .query-item, .category-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(74, 144, 226, 0.1);
    }
    
    .usage-bar, .power-bar {
        flex: 1;
        height: 8px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
        margin: 0 1rem;
        overflow: hidden;
    }
    
    .usage-fill, .power-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .usage-fill.space, .power-fill.space { background: var(--space-blue); }
    .usage-fill.mind, .power-fill.mind { background: var(--mind-yellow); }
    .usage-fill.reality, .power-fill.reality { background: var(--reality-red); }
    .usage-fill.power, .power-fill.power { background: var(--power-purple); }
    .usage-fill.time, .power-fill.time { background: var(--time-green); }
    .usage-fill.soul, .power-fill.soul { background: var(--soul-orange); }
    
    .detail-grid {
        display: grid;
        gap: 0.5rem;
    }
    
    .detail-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(74, 144, 226, 0.1);
    }
    
    .detail-label {
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .detail-value {
        color: var(--text-primary);
    }
    
    .stone-powers-grid {
        display: grid;
        gap: 1rem;
    }
    
    .stone-power-item {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .stone-name {
        min-width: 100px;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .power-value {
        min-width: 50px;
        text-align: right;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .no-results {
        grid-column: 1 / -1;
        text-align: center;
        padding: 3rem;
        color: var(--text-secondary);
    }
    
    .no-results h3 {
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);
