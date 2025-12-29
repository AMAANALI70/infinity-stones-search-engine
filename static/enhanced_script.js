// Enhanced Infinity Stones Search Engine - Advanced JavaScript

class EnhancedInfinitySearchApp {
    constructor() {
        this.selectedStones = new Set(); // Track multiple selected stones
        this.searchResults = [];
        this.currentPage = 1;
        this.resultsPerPage = 25;
        this.paginationInfo = null; // Store backend pagination info
        this.currentQuery = ''; // Store current search query for pagination
        this.analytics = {
            totalSearches: 0,
            searchTimes: [],
            stoneUsage: {},
            popularQueries: {}
        };
        
        this.particleSystem = null;
        this.gsapTimeline = null;
        this.isSearching = false;
        
        this.init();
    }

    init() {
        console.log('🔮 Initializing Enhanced Infinity Search App...');
        this.setupEventListeners();
        this.loadAnalytics();
        this.initializeAnimations();
        this.setupParticleSystem();
        this.setupSearchSuggestions();
        this.startCosmicEffects();
        
        // Debug: Check if stone cards exist
        setTimeout(() => {
            const stoneCards = document.querySelectorAll('.stone-card.enhanced');
            console.log(`Found ${stoneCards.length} stone cards`);
            stoneCards.forEach((card, index) => {
                console.log(`Stone ${index + 1}:`, card.dataset.stone, card.style.display);
            });
            
            // Initialize power bars to 0%
            this.updateIndividualStonePowerBars();
        }, 1000);
    }

    initializeAnimations() {
        // Initialize GSAP timeline for entrance animations
        this.gsapTimeline = gsap.timeline();
        
        // Animate header elements
        this.gsapTimeline
            .from('.title', { duration: 1, y: -50, opacity: 0, ease: "power3.out" })
            .from('.subtitle', { duration: 0.8, y: 30, opacity: 0, ease: "power2.out" }, "-=0.5")
            .from('.power-indicator', { duration: 0.6, scale: 0, opacity: 0, ease: "back.out(1.7)" }, "-=0.3")
            .from('.stone-card', { duration: 0.5, y: 50, opacity: 0, stagger: 0.1, ease: "power2.out" }, "-=0.2")
            .from('.search-interface', { duration: 0.8, y: 50, opacity: 0, ease: "power2.out" }, "-=0.4");
    }

    setupParticleSystem() {
        const container = document.getElementById('particlesContainer');
        if (!container) return;

        // Create particle system using Three.js
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0);
        container.appendChild(renderer.domElement);

        // Create particles
        const particleCount = 200;
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 2000;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 2000;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 2000;

            // Random colors for different stone types
            const colorChoice = Math.random();
            if (colorChoice < 0.16) {
                colors[i * 3] = 0.29; colors[i * 3 + 1] = 0.56; colors[i * 3 + 2] = 0.89; // Space blue
            } else if (colorChoice < 0.32) {
                colors[i * 3] = 0.96; colors[i * 3 + 1] = 0.65; colors[i * 3 + 2] = 0.14; // Mind yellow
            } else if (colorChoice < 0.48) {
                colors[i * 3] = 0.82; colors[i * 3 + 1] = 0.01; colors[i * 3 + 2] = 0.11; // Reality red
            } else if (colorChoice < 0.64) {
                colors[i * 3] = 0.56; colors[i * 3 + 1] = 0.08; colors[i * 3 + 2] = 1.0; // Power purple
            } else if (colorChoice < 0.80) {
                colors[i * 3] = 0.49; colors[i * 3 + 1] = 0.83; colors[i * 3 + 2] = 0.13; // Time green
            } else {
                colors[i * 3] = 0.97; colors[i * 3 + 1] = 0.91; colors[i * 3 + 2] = 0.11; // Soul orange
            }
        }

        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particles.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 2,
            vertexColors: true,
            transparent: true,
            opacity: 0.6
        });

        this.particleSystem = new THREE.Points(particles, material);
        scene.add(this.particleSystem);

        camera.position.z = 1000;

        // Animation loop
        const animate = () => {
            requestAnimationFrame(animate);
            
            this.particleSystem.rotation.x += 0.001;
            this.particleSystem.rotation.y += 0.002;
            
            renderer.render(scene, camera);
        };
        
        animate();

        // Handle window resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }


    startCosmicEffects() {
        // Animate power indicator
        this.animatePowerIndicator();
        
        // Start floating animations
        this.startFloatingAnimations();
        
        // Initialize typing effects
        this.setupTypingEffects();
    }

    animatePowerIndicator() {
        // Power indicator is now handled by updatePowerLevel() method
        // This method is kept for compatibility but does nothing
    }

    startFloatingAnimations() {
        // Animate infinity symbols
        const infinitySymbols = document.querySelectorAll('.infinity-symbol');
        infinitySymbols.forEach((symbol, index) => {
            gsap.to(symbol, {
                duration: 3,
                y: "+=10",
                rotation: "+=5",
                ease: "sine.inOut",
                yoyo: true,
                repeat: -1,
                delay: index * 0.5
            });
        });

        // Animate search stats
        const statItems = document.querySelectorAll('.stat-item');
        statItems.forEach((item, index) => {
            gsap.to(item, {
                duration: 2,
                y: "+=5",
                ease: "sine.inOut",
                yoyo: true,
                repeat: -1,
                delay: index * 0.3
            });
        });
    }

    setupTypingEffects() {
        const searchInput = document.getElementById('searchInput');
        const typingIndicator = document.getElementById('typingIndicator');
        
        if (!searchInput || !typingIndicator) return;

        let typingTimeout;
        
        searchInput.addEventListener('input', () => {
            typingIndicator.classList.add('active');
            
            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(() => {
                typingIndicator.classList.remove('active');
            }, 1000);
        });
    }

    setupEventListeners() {
        // Stone selection
        document.querySelectorAll('.stone-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.selectStone(e.currentTarget.dataset.stone);
                this.animateStoneSelection(e.currentTarget);
            });
        });

        // All stones button
        document.getElementById('allStonesBtn').addEventListener('click', () => {
            this.selectStone('all');
            this.animateAllStonesSelection();
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
        const stoneDescriptions = {
            'space': '🔍 Space Stone: Fast text search using distributed indexes',
            'mind': '🧠 Mind Stone: Smart search with AI understanding and synonyms', 
            'reality': '🎯 Reality Stone: Advanced ranking with TF-IDF and personalization',
            'power': '⚡ Power Stone: Distributed computing with weighted result combination',
            'time': '⏱️ Time Stone: Ultra-fast search with advanced caching',
            'soul': '📊 Soul Stone: Analytics engine tracking search patterns',
            'all': '∞ All Stones: Ultimate search power combining all six algorithms'
        };

        if (stoneType === 'all') {
            // Select all stones
            this.selectedStones.clear();
            document.querySelectorAll('.stone-card').forEach(card => {
                const stone = card.dataset.stone;
                this.selectedStones.add(stone);
                card.classList.add('active');
            });
            document.getElementById('allStonesBtn').classList.add('active');
            this.showNotification(stoneDescriptions['all'], 'info');
        } else {
            // Toggle individual stone selection
            const stoneCard = document.querySelector(`[data-stone="${stoneType}"]`);
            if (this.selectedStones.has(stoneType)) {
                // Deselect stone
                this.selectedStones.delete(stoneType);
                stoneCard.classList.remove('active');
                this.showNotification(`${stoneDescriptions[stoneType]} - DEACTIVATED`, 'warning');
            } else {
                // Select stone
                this.selectedStones.add(stoneType);
                stoneCard.classList.add('active');
                this.showNotification(`${stoneDescriptions[stoneType]} - ACTIVATED`, 'success');
            }
            document.getElementById('allStonesBtn').classList.remove('active');
        }

        // Animate stone selection
        this.animateStoneSelection(stoneType);
        
        // Update power immediately
        this.updatePowerLevel();
        
        // Update stone selection info
        this.updateStoneSelectionInfo();
    }

    updatePowerLevel() {
        const panelPowerFill = document.getElementById('panelPowerFill');
        const panelPowerLevel = document.getElementById('panelPowerLevel');
        
        if (!panelPowerFill || !panelPowerLevel) return;

        const stoneCount = this.selectedStones.size;
        const power = stoneCount * 16.67; // Each stone = 16.67% (100% / 6 stones)
        const allStonesPower = Math.min(power, 100); // Cap at 100%
        
        gsap.to(panelPowerFill, { 
            duration: 0.8, 
            width: `${allStonesPower}%`,
            ease: "power2.out"
        });
        
        gsap.to(panelPowerLevel, { 
            duration: 0.8, 
            textContent: `${Math.round(allStonesPower)}%`,
            ease: "power2.out"
        });

        // Update individual stone power bars
        this.updateIndividualStonePowerBars();
    }

    updateIndividualStonePowerBars() {
        document.querySelectorAll('.stone-card').forEach(card => {
            const stoneType = card.dataset.stone;
            const powerFill = card.querySelector('.power-fill');
            const powerValue = card.querySelector('.power-value');
            
            if (powerFill && powerValue) {
                if (this.selectedStones.has(stoneType)) {
                    // Stone is selected - show 100% power
                    gsap.to(powerFill, {
                        duration: 0.5,
                        width: "100%",
                        ease: "power2.out"
                    });
                    gsap.to(powerValue, {
                        duration: 0.5,
                        textContent: "100%",
                        ease: "power2.out"
                    });
                } else {
                    // Stone is not selected - show 0% power
                    gsap.to(powerFill, {
                        duration: 0.5,
                        width: "0%",
                        ease: "power2.out"
                    });
                    gsap.to(powerValue, {
                        duration: 0.5,
                        textContent: "0%",
                        ease: "power2.out"
                    });
                }
            }
        });
    }

    updateStoneSelectionInfo() {
        const selectedStoneNames = {
            'space': 'Space Stone (Fast Search)',
            'mind': 'Mind Stone (Smart AI)', 
            'reality': 'Reality Stone (Advanced Ranking)',
            'power': 'Power Stone (Distributed Computing)',
            'time': 'Time Stone (Ultra-Fast Cache)',
            'soul': 'Soul Stone (Analytics)'
        };
        
        if (this.selectedStones.size === 0) {
            console.log('ℹ️ No stones selected - searches will use basic algorithms');
        } else if (this.selectedStones.size === 6) {
            console.log('🌟 All stones active - maximum search power!');
        } else {
            const activeStones = Array.from(this.selectedStones).map(stone => selectedStoneNames[stone]);
            console.log(`✨ Active stones: ${activeStones.join(', ')}`);
        }
    }

    animateStoneSelection(element) {
        if (typeof element === 'string') {
            element = document.querySelector(`[data-stone="${element}"]`);
        }
        
        if (!element) return;

        // Create selection effect
        gsap.fromTo(element, 
            { scale: 1 },
            { 
                scale: 1.05, 
                duration: 0.3, 
                ease: "power2.out",
                yoyo: true,
                repeat: 1
            }
        );

        // Add glow effect
        const glowEffect = element.querySelector('.stone-glow-effect');
        if (glowEffect) {
            gsap.to(glowEffect, {
                duration: 0.5,
                opacity: 0.6,
                ease: "power2.out"
            });
        }

        // Power bar animation is now handled by updateIndividualStonePowerBars()
        // This ensures consistency with the actual selection state

        // Create ripple effect
        const rippleEffect = element.querySelector('.ripple-effect');
        if (rippleEffect) {
            gsap.fromTo(rippleEffect, 
                { scale: 0, opacity: 0 },
                { 
                    scale: 1.5, 
                    opacity: 0.6, 
                    duration: 0.6, 
                    ease: "power2.out",
                    onComplete: () => {
                        gsap.to(rippleEffect, {
                            duration: 0.3,
                            opacity: 0,
                            ease: "power2.out"
                        });
                    }
                }
            );
        }
    }

    animateAllStonesSelection() {
        const allStonesBtn = document.getElementById('allStonesBtn');
        
        gsap.fromTo(allStonesBtn, 
            { scale: 1 },
            { 
                scale: 1.05, 
                duration: 0.3, 
                ease: "power2.out",
                yoyo: true,
                repeat: 2
            }
        );

        // Animate all stone cards
        document.querySelectorAll('.stone-card').forEach((card, index) => {
            gsap.to(card, {
                duration: 0.3,
                scale: 1.05,
                ease: "power2.out",
                delay: index * 0.1,
                yoyo: true,
                repeat: 1
            });
        });
    }

    async performSearch() {
        const query = document.getElementById('searchInput').value.trim();
        if (!query) {
            this.showNotification('Please enter a search query', 'warning');
            return;
        }

        if (this.isSearching) return;
        this.isSearching = true;
        
        // Store current query for pagination
        this.currentQuery = query;

        console.log('Starting search for:', query);
        this.showLoading();
        this.animateSearchButton();
        
        const startTime = performance.now();

        try {
            // Call the real Flask backend API
            const searchData = await this.performRealSearch(query);
            const endTime = performance.now();
            const searchTime = (endTime - startTime) / 1000;

            // Handle paginated response
            if (searchData.results) {
                this.searchResults = searchData.results;
                this.paginationInfo = searchData.pagination;
                console.log('About to display results:', searchData.results);
                console.log('Pagination info:', searchData.pagination);
                this.displayResults(searchData.results, true);
            } else {
                // Fallback for non-paginated response
                this.searchResults = searchData;
                console.log('About to display results:', searchData);
                this.displayResults(searchData, true);
            }
            
            this.updateSearchStats(query, searchTime);
            this.hideLoading();

            // Show results section with animation
            const resultsSection = document.getElementById('resultsSection');
            console.log('Results section found:', resultsSection);
            if (resultsSection) {
                resultsSection.style.display = 'block';
                console.log('Results section displayed');
                
                try {
                    gsap.fromTo(resultsSection, 
                        { y: 50, opacity: 0 },
                        { y: 0, opacity: 1, duration: 0.8, ease: "power2.out" }
                    );
                    
                    setTimeout(() => {
                        resultsSection.scrollIntoView({ behavior: 'smooth' });
                    }, 100);
                } catch (error) {
                    console.warn('Results section animation error:', error);
                    resultsSection.style.opacity = '1';
                    resultsSection.scrollIntoView({ behavior: 'smooth' });
                }
            } else {
                console.error('Could not find results section element!');
            }

        } catch (error) {
            console.error('Search error:', error);
            this.showNotification('Search failed. Please try again.', 'error');
            this.hideLoading();
        } finally {
            this.isSearching = false;
        }
    }

    animateSearchButton() {
        const searchBtn = document.getElementById('searchBtn');
        
        gsap.to(searchBtn, {
            duration: 0.1,
            scale: 0.95,
            ease: "power2.out",
            yoyo: true,
            repeat: -1
        });
    }

    async performRealSearch(query, page = 1, perPage = 25) {
        // Call the actual Flask backend API
        // Handle stone selection - default to 'all' if none selected
        let stoneSelection = 'all'; // Default to all stones
        if (this.selectedStones.size > 0 && this.selectedStones.size < 6) {
            stoneSelection = Array.from(this.selectedStones).join(',');
        }
        
        const requestData = {
            query: query,
            stone: stoneSelection,
            page: page,
            per_page: perPage
        };

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Search failed');
            }

            console.log(`🎆 Search successful! Found ${data.results ? data.results.length : 0} results on page ${data.pagination ? data.pagination.page : 1}`);
            return {
                results: data.results,
                pagination: data.pagination
            };
        } catch (error) {
            console.error('API call failed:', error);
            console.log('Falling back to mock data');
            // Fallback to mock data if API fails
            return this.simulateSearch(query);
        }
    }

    async simulateSearch(query) {
        // Enhanced mock data for demonstration
        const mockResults = [
            {
                product_id: '1',
                product_data: {
                    'Brand': 'Sony',
                    'Type': 'Bluetooth Speaker',
                    'Model Number': 'SRS-XB23',
                    'Features': 'Waterproof, Extra Bass, LED Lights',
                    'Battery Life': '12 hours',
                    'Connectivity': 'Bluetooth 5.0, USB-C',
                    'Weight': '580g',
                    'Dimensions': '18.4 x 6.8 x 6.8 cm'
                },
                relevance_score: 0.95,
                stone_powers: {
                    'Space Stone': 0.8,
                    'Mind Stone': 0.7,
                    'Reality Stone': 0.9,
                    'Power Stone': 0.85,
                    'Time Stone': 0.6,
                    'Soul Stone': 0.75
                },
                matched_fields: ['brand', 'type', 'features']
            },
            {
                product_id: '2',
                product_data: {
                    'Brand': 'JBL',
                    'Type': 'Wireless Headphones',
                    'Model Number': 'TUNE 750BTNC',
                    'Features': 'Noise Cancelling, 30h Battery, Quick Charge',
                    'Connectivity': 'Bluetooth 5.0, 3.5mm, USB-C',
                    'Weight': '220g',
                    'Frequency Response': '20Hz - 20kHz'
                },
                relevance_score: 0.88,
                stone_powers: {
                    'Space Stone': 0.75,
                    'Mind Stone': 0.8,
                    'Reality Stone': 0.85,
                    'Power Stone': 0.9,
                    'Time Stone': 0.7,
                    'Soul Stone': 0.65
                },
                matched_fields: ['type', 'features', 'connectivity']
            },
            {
                product_id: '3',
                product_data: {
                    'Brand': 'Bose',
                    'Type': 'Smart Speaker',
                    'Model Number': 'Home Speaker 500',
                    'Features': 'Voice Control, Wi-Fi, Multi-room',
                    'Connectivity': 'Wi-Fi, Bluetooth, Ethernet',
                    'Weight': '1.1kg',
                    'Audio': '360-degree sound'
                },
                relevance_score: 0.82,
                stone_powers: {
                    'Space Stone': 0.7,
                    'Mind Stone': 0.9,
                    'Reality Stone': 0.8,
                    'Power Stone': 0.75,
                    'Time Stone': 0.8,
                    'Soul Stone': 0.85
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
        await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));

        return filteredResults;
    }

    displayResults(results, resetPagination = true) {
        console.log('Displaying results:', results ? results.length : 0);
        const resultsGrid = document.getElementById('resultsGrid');
        const resultsCount = document.getElementById('resultsCount');
        const searchTime = document.getElementById('searchTime');
        
        console.log('Results grid element:', resultsGrid);
        console.log('Results count element:', resultsCount);
        console.log('Search time element:', searchTime);

        // Use backend pagination if available
        let totalResults, totalPages, currentPageResults, startIndex, endIndex;
        
        if (this.paginationInfo) {
            // Backend pagination
            totalResults = this.paginationInfo.total_results;
            totalPages = this.paginationInfo.total_pages;
            currentPageResults = results; // Results are already paginated by backend
            this.currentPage = this.paginationInfo.page;
            // Calculate display indices for backend pagination
            startIndex = (this.paginationInfo.page - 1) * this.paginationInfo.per_page;
            endIndex = startIndex + this.paginationInfo.per_page;
        } else {
            // Fallback to frontend pagination for mock/legacy data
            if (resetPagination) {
                this.currentPage = 1;
                this.allResults = [...results];
            }
            const sortedResults = [...this.allResults].sort((a, b) => b.relevance_score - a.relevance_score);
            totalResults = sortedResults.length;
            totalPages = Math.ceil(totalResults / this.resultsPerPage);
            startIndex = (this.currentPage - 1) * this.resultsPerPage;
            endIndex = startIndex + this.resultsPerPage;
            currentPageResults = sortedResults.slice(startIndex, endIndex);
        }
        
        // Update results count to show pagination info
        if (resultsCount) {
            resultsCount.textContent = `${totalResults} results (Page ${this.currentPage} of ${totalPages})`;
        }
        if (searchTime) searchTime.textContent = (performance.now() / 1000).toFixed(3);

        if (totalResults === 0) {
            console.log('No results found, showing no-results message');
            if (resultsGrid) {
                resultsGrid.innerHTML = `
                    <div class="no-results">
                        <h3>No results found</h3>
                        <p>Try adjusting your search terms or using a different stone power.</p>
                    </div>
                `;
            }
            this.updatePagination(0, 0);
            return;
        }

        console.log(`Displaying page ${this.currentPage}: results ${startIndex + 1}-${Math.min(endIndex, totalResults)} of ${totalResults}`);
        console.log('Current page results:', currentPageResults);
        console.log('Results grid element check:', resultsGrid);

        if (!resultsGrid) {
            console.error('Results grid element not found!');
            return;
        }

        if (!currentPageResults || !Array.isArray(currentPageResults)) {
            console.error('Invalid current page results:', currentPageResults);
            resultsGrid.innerHTML = `<div class="error-message">Error: Invalid results data</div>`;
            return;
        }

        // Display current page results
        try {
            resultsGrid.innerHTML = currentPageResults.map((result, index) => {
            const product = result.product_data;
            const stonePowers = result.stone_powers;
            const globalIndex = startIndex + index + 1; // Global ranking number
            
                if (!result || !result.product_data) {
                    console.warn('Invalid result item:', result);
                    return '<div class="error-result">Invalid result data</div>';
                }
                
                return `
                    <div class="result-card fade-in" style="animation-delay: ${index * 0.1}s" onclick="app.showProductDetails('${result.product_id}')">
                        <div class="result-header">
                            <span class="result-rank">#${globalIndex}</span>
                            <span class="result-id">ID: ${result.product_id}</span>
                            <span class="relevance-score">${(result.relevance_score * 100).toFixed(1)}%</span>
                        </div>
                        <div class="result-content">
                            <div class="result-brand">${product.Brand || 'Unknown Brand'}</div>
                            <div class="result-type">${product.Type || 'Unknown Type'}</div>
                            <div class="result-model">${product['Model Number'] || 'No Model'}</div>
                        </div>
                        <div class="stone-powers">
                            ${Object.entries(stonePowers || {}).map(([stone, power]) => 
                                `<span class="stone-power-badge ${stone.toLowerCase().replace(' stone', '')}" title="${stone} stone power">${stone.replace(' Stone', '')}: ${(power * 100).toFixed(0)}%</span>`
                            ).join('')}
                        </div>
                    </div>
                `;
            }).join('');
            
            console.log('Results HTML generated successfully');
            
        } catch (error) {
            console.error('Error generating results HTML:', error);
            resultsGrid.innerHTML = `<div class="error-message">Error displaying results: ${error.message}</div>`;
            return;
        }

        // Animate result cards with smooth transition
        try {
            gsap.fromTo('.result-card', 
                { y: 30, opacity: 0 },
                { 
                    y: 0, 
                    opacity: 1, 
                    duration: 0.5, 
                    stagger: 0.08, 
                    ease: "power2.out" 
                }
            );
        } catch (error) {
            console.warn('GSAP animation error:', error);
        }

        // Update pagination controls
        try {
            this.updatePagination(totalPages, totalResults);
            this.updateStonePowers(currentPageResults);
        } catch (error) {
            console.warn('Pagination update error:', error);
        }
        
        // Ensure results section is visible and scroll to it
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.style.display = 'block';
            console.log('Results section made visible');
            
            if (!resetPagination) {
                try {
                    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } catch (error) {
                    console.warn('Scroll error:', error);
                    // Fallback to immediate scroll
                    resultsSection.scrollIntoView();
                }
            }
        } else {
            console.error('Results section element not found!');
        }
    }

    updateStonePowers(results) {
        // Update stone power indicators based on search results
        const stoneCards = document.querySelectorAll('.stone-card');
        
        stoneCards.forEach(card => {
            const stoneType = card.dataset.stone;
            const powerBar = card.querySelector('.stone-power');
            
            // Calculate average power for this stone across all results
            const avgPower = results.reduce((sum, result) => {
                const stoneName = stoneType.charAt(0).toUpperCase() + stoneType.slice(1) + ' Stone';
                return sum + (result.stone_powers[stoneName] || 0);
            }, 0) / results.length;
            
            // Animate power bar
            gsap.to(powerBar.querySelector('::after'), {
                duration: 1,
                width: `${avgPower * 100}%`,
                ease: "power2.out"
            });
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
                        <span class="stone-name">${stone}</span>
                        <div class="power-bar">
                            <div class="power-fill ${stone.toLowerCase().replace(' stone', '')}" style="width: ${power * 100}%"></div>
                        </div>
                        <span class="power-value">${(power * 100).toFixed(1)}%</span>
                    </div>`
                ).join('')}
            </div>
        `;

        modal.style.display = 'flex';
        
        // Animate modal entrance
        gsap.fromTo(modal, 
            { opacity: 0, scale: 0.8 },
            { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.7)" }
        );
    }

    closeModal() {
        const modal = document.getElementById('productModal');
        
        gsap.to(modal, {
            duration: 0.3,
            opacity: 0,
            scale: 0.8,
            ease: "power2.in",
            onComplete: () => {
                modal.style.display = 'none';
            }
        });
    }

    sortResults() {
        const sortBy = document.getElementById('sortBy').value;
        if (!this.allResults || this.allResults.length === 0) return;
        
        let sortedResults = [...this.allResults];

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

        // Store sorted results and reset to page 1
        this.allResults = sortedResults;
        this.currentPage = 1;
        this.displayResults(this.allResults, false);
    }

    filterResults() {
        const category = document.getElementById('categoryFilter').value;
        if (!category) {
            // Reset to original search results
            if (this.searchResults && this.searchResults.length > 0) {
                this.allResults = [...this.searchResults];
                this.currentPage = 1;
                this.displayResults(this.allResults, false);
            }
            return;
        }

        if (!this.searchResults || this.searchResults.length === 0) return;

        const filteredResults = this.searchResults.filter(result => {
            const productType = (result.product_data.Type || '').toLowerCase();
            const productBrand = (result.product_data.Brand || '').toLowerCase();
            const productFeatures = (result.product_data.Features || '').toLowerCase();
            const allProductText = `${productType} ${productBrand} ${productFeatures}`.toLowerCase();
            
            // Create category mapping for better filtering
            switch(category) {
                case 'automotive':
                    return productType.includes('car') || 
                           productType.includes('bike') || 
                           productType.includes('vehicle') ||
                           productType.includes('tyre') ||
                           productType.includes('vacuum') ||
                           productType.includes('bluetooth converter') ||
                           allProductText.includes('car') ||
                           allProductText.includes('automotive') ||
                           allProductText.includes('vehicle');
                
                case 'electronics':
                    return productType.includes('bluetooth') ||
                           productType.includes('speaker') ||
                           productType.includes('headphone') ||
                           productType.includes('converter') ||
                           productType.includes('led') ||
                           productType.includes('light') ||
                           allProductText.includes('bluetooth') ||
                           allProductText.includes('electronic') ||
                           allProductText.includes('digital');
                
                case 'beauty':
                    return allProductText.includes('beauty') ||
                           allProductText.includes('cream') ||
                           allProductText.includes('cosmetic') ||
                           allProductText.includes('skin') ||
                           allProductText.includes('hair');
                
                case 'home':
                    return productType.includes('mattress') ||
                           productType.includes('pillow') ||
                           productType.includes('furniture') ||
                           productType.includes('table') ||
                           productType.includes('chair') ||
                           productType.includes('bed') ||
                           allProductText.includes('home') ||
                           allProductText.includes('furniture') ||
                           allProductText.includes('household');
                
                case 'sports':
                    return productType.includes('gym') ||
                           productType.includes('fitness') ||
                           productType.includes('exercise') ||
                           productType.includes('sports') ||
                           productType.includes('yoga') ||
                           productType.includes('workout') ||
                           allProductText.includes('gym') ||
                           allProductText.includes('fitness') ||
                           allProductText.includes('sports') ||
                           allProductText.includes('exercise');
                
                default:
                    return productType.includes(category);
            }
        });

        // Store filtered results and reset to page 1
        this.allResults = filteredResults;
        this.currentPage = 1;
        this.displayResults(this.allResults, false);
    }

    updatePagination(totalPages, totalResults) {
        const pagination = document.getElementById('pagination');
        if (!pagination || totalPages <= 1) {
            if (pagination) pagination.innerHTML = '';
            return;
        }

        let paginationHTML = '<div class="pagination-container">';
        
        // Previous button
        if (this.currentPage > 1) {
            paginationHTML += `<button class="pagination-btn prev-btn" onclick="app.goToPage(${this.currentPage - 1})">
                <i class="fas fa-chevron-left"></i> Previous
            </button>`;
        }
        
        // Page numbers
        paginationHTML += '<div class="page-numbers">';
        
        // Calculate page range to show
        let startPage = Math.max(1, this.currentPage - 2);
        let endPage = Math.min(totalPages, this.currentPage + 2);
        
        // Show first page if not in range
        if (startPage > 1) {
            paginationHTML += `<button class="pagination-btn page-btn" onclick="app.goToPage(1)">1</button>`;
            if (startPage > 2) {
                paginationHTML += '<span class="pagination-dots">...</span>';
            }
        }
        
        // Show page numbers in range
        for (let i = startPage; i <= endPage; i++) {
            const isActive = i === this.currentPage ? 'active' : '';
            paginationHTML += `<button class="pagination-btn page-btn ${isActive}" onclick="app.goToPage(${i})">${i}</button>`;
        }
        
        // Show last page if not in range
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                paginationHTML += '<span class="pagination-dots">...</span>';
            }
            paginationHTML += `<button class="pagination-btn page-btn" onclick="app.goToPage(${totalPages})">${totalPages}</button>`;
        }
        
        paginationHTML += '</div>';
        
        // Next button
        if (this.currentPage < totalPages) {
            paginationHTML += `<button class="pagination-btn next-btn" onclick="app.goToPage(${this.currentPage + 1})">
                Next <i class="fas fa-chevron-right"></i>
            </button>`;
        }
        
        // Results info
        const startResult = (this.currentPage - 1) * this.resultsPerPage + 1;
        const endResult = Math.min(this.currentPage * this.resultsPerPage, totalResults);
        paginationHTML += `</div><div class="pagination-info">
            Showing ${startResult}-${endResult} of ${totalResults} results
        </div>`;
        
        pagination.innerHTML = paginationHTML;
        
        // Animate pagination
        gsap.fromTo('.pagination-container', 
            { y: 20, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }
        );
    }

    goToPage(page) {
        if (page < 1 || !this.allResults) return;
        
        const totalPages = Math.ceil(this.allResults.length / this.resultsPerPage);
        if (page > totalPages) return;
        
        this.currentPage = page;
        this.displayResults(this.allResults, false); // Don't reset pagination
    }

    switchSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Show/hide sections with animations
        const sections = {
            'search': document.getElementById('resultsSection'),
            'analytics': document.getElementById('analyticsDashboard'),
            'about': document.getElementById('aboutSection')
        };

        Object.entries(sections).forEach(([key, element]) => {
            if (key === section) {
                element.style.display = 'block';
                gsap.fromTo(element, 
                    { y: 30, opacity: 0 },
                    { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }
                );
            } else {
                gsap.to(element, {
                    duration: 0.3,
                    y: -30,
                    opacity: 0,
                    ease: "power2.in",
                    onComplete: () => {
                        element.style.display = 'none';
                    }
                });
            }
        });

        if (section === 'analytics') {
            this.updateAnalyticsDashboard();
        }
    }

    async updateAnalyticsDashboard() {
        try {
            // Fetch real analytics from the backend
            const response = await fetch('/api/analytics');
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.analytics = data.analytics;
                }
            }
        } catch (error) {
            console.error('Failed to fetch analytics:', error);
        }

        document.getElementById('totalSearches').textContent = this.analytics.search_analytics?.total_searches || 0;
        
        const searchTimes = this.analytics.search_analytics?.search_times || [];
        const avgTime = searchTimes.length > 0 
            ? searchTimes.reduce((a, b) => a + b, 0) / searchTimes.length 
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
        const stones = ['Space Stone', 'Mind Stone', 'Reality Stone', 'Power Stone', 'Time Stone', 'Soul Stone'];
        
        chart.innerHTML = stones.map(stone => {
            const usage = this.analytics.search_analytics?.stone_usage?.[stone] || 0;
            const totalSearches = this.analytics.search_analytics?.total_searches || 1;
            const percentage = (usage / totalSearches) * 100;
            const stoneKey = stone.toLowerCase().replace(' stone', '');
            
            return `
                <div class="stone-usage-item">
                    <span class="stone-name">${stone}</span>
                    <div class="usage-bar">
                        <div class="usage-fill ${stoneKey}" style="width: ${percentage}%"></div>
                    </div>
                    <span class="usage-value">${usage}</span>
                </div>
            `;
        }).join('');
    }

    updatePopularQueries() {
        const container = document.getElementById('popularQueries');
        const popularQueries = this.analytics.search_analytics?.popular_queries || {};
        const queries = Object.entries(popularQueries)
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
        
        if (this.selectedStones.size === 6) {
            this.analytics.stoneUsage['all'] = (this.analytics.stoneUsage['all'] || 0) + 1;
        } else {
            this.selectedStones.forEach(stone => {
                this.analytics.stoneUsage[stone] = (this.analytics.stoneUsage[stone] || 0) + 1;
            });
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
                
                // Animate suggestions
                gsap.fromTo('.suggestion-item', 
                    { y: -10, opacity: 0 },
                    { y: 0, opacity: 1, duration: 0.3, stagger: 0.1, ease: "power2.out" }
                );
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
        
        // Animate loading overlay
        gsap.fromTo('#loadingOverlay', 
            { opacity: 0 },
            { opacity: 1, duration: 0.3, ease: "power2.out" }
        );
    }

    hideLoading() {
        gsap.to('#loadingOverlay', {
            duration: 0.3,
            opacity: 0,
            ease: "power2.in",
            onComplete: () => {
                document.getElementById('loadingOverlay').style.display = 'none';
            }
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 2rem',
            borderRadius: '15px',
            color: 'white',
            fontWeight: '600',
            zIndex: '1001',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)'
        });

        // Set background color based on type
        const colors = {
            info: 'linear-gradient(135deg, #4A90E2, #357ABD)',
            success: 'linear-gradient(135deg, #7ED321, #6BC20A)',
            warning: 'linear-gradient(135deg, #F5A623, #E89611)',
            error: 'linear-gradient(135deg, #D0021B, #B8011A)'
        };
        notification.style.background = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Animate in
        gsap.to(notification, {
            duration: 0.4,
            x: 0,
            ease: "back.out(1.7)"
        });

        // Remove after 4 seconds
        setTimeout(() => {
            gsap.to(notification, {
                duration: 0.3,
                x: '100%',
                ease: "power2.in",
                onComplete: () => {
                    document.body.removeChild(notification);
                }
            });
        }, 4000);
    }

    getNotificationIcon(type) {
        const icons = {
            info: 'info-circle',
            success: 'check-circle',
            warning: 'exclamation-triangle',
            error: 'times-circle'
        };
        return icons[type] || 'info-circle';
    }

    async goToPage(page) {
        if (!this.currentQuery) return;
        
        if (this.paginationInfo) {
            // Backend pagination - perform new search with page parameter
            try {
                const searchData = await this.performRealSearch(this.currentQuery, page, this.resultsPerPage);
                if (searchData.results) {
                    this.searchResults = searchData.results;
                    this.paginationInfo = searchData.pagination;
                    this.displayResults(searchData.results, false);
                } else {
                    this.searchResults = searchData;
                    this.displayResults(searchData, false);
                }
            } catch (error) {
                console.error('Pagination error:', error);
                this.showNotification('Failed to load page', 'error');
            }
        } else {
            // Frontend pagination fallback
            this.currentPage = page;
            this.displayResults(this.allResults, false);
        }
    }

    nextPage() {
        if (this.paginationInfo && this.paginationInfo.has_next) {
            this.goToPage(this.paginationInfo.next_page);
        } else if (!this.paginationInfo) {
            const totalPages = Math.ceil(this.allResults.length / this.resultsPerPage);
            if (this.currentPage < totalPages) {
                this.goToPage(this.currentPage + 1);
            }
        }
    }

    prevPage() {
        if (this.paginationInfo && this.paginationInfo.has_prev) {
            this.goToPage(this.paginationInfo.prev_page);
        } else if (!this.paginationInfo) {
            if (this.currentPage > 1) {
                this.goToPage(this.currentPage - 1);
            }
        }
    }

    updatePagination(totalPages, totalResults) {
        const paginationContainer = document.getElementById('paginationContainer');
        if (!paginationContainer) {
            // Create pagination container if it doesn't exist
            const resultsSection = document.getElementById('resultsSection');
            if (resultsSection) {
                const paginationHTML = `
                    <div id="paginationContainer" class="pagination-container">
                        <div class="pagination-info"></div>
                        <div class="pagination-controls">
                            <button id="prevPageBtn" class="pagination-btn">← Previous</button>
                            <span id="pageInfo" class="page-info"></span>
                            <button id="nextPageBtn" class="pagination-btn">Next →</button>
                        </div>
                    </div>
                `;
                resultsSection.insertAdjacentHTML('beforeend', paginationHTML);
                
                // Add event listeners for pagination buttons
                document.getElementById('prevPageBtn').addEventListener('click', () => this.prevPage());
                document.getElementById('nextPageBtn').addEventListener('click', () => this.nextPage());
            }
        }
        
        // Update pagination controls
        const prevBtn = document.getElementById('prevPageBtn');
        const nextBtn = document.getElementById('nextPageBtn');
        const pageInfo = document.getElementById('pageInfo');
        const paginationInfo = document.querySelector('.pagination-info');
        
        if (this.paginationInfo) {
            // Backend pagination
            const { page, total_pages, has_prev, has_next, total_results } = this.paginationInfo;
            
            if (prevBtn) prevBtn.disabled = !has_prev;
            if (nextBtn) nextBtn.disabled = !has_next;
            if (pageInfo) pageInfo.textContent = `Page ${page} of ${total_pages}`;
            if (paginationInfo) paginationInfo.textContent = `Showing ${this.searchResults.length} results out of ${total_results} total`;
        } else {
            // Frontend pagination fallback
            if (prevBtn) prevBtn.disabled = this.currentPage <= 1;
            if (nextBtn) nextBtn.disabled = this.currentPage >= totalPages;
            if (pageInfo) pageInfo.textContent = `Page ${this.currentPage} of ${totalPages}`;
            if (paginationInfo) paginationInfo.textContent = `Showing ${this.resultsPerPage} results per page`;
        }
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
    
    // Debug helper function
    debugSearch(query = 'mobile') {
        console.log('🔍 Debug: Testing search functionality...');
        console.log('Selected stones:', this.selectedStones);
        console.log('Search input element:', document.getElementById('searchInput'));
        console.log('Results section element:', document.getElementById('resultsSection'));
        console.log('Results grid element:', document.getElementById('resultsGrid'));
        
        // Set the query and perform search
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = query;
            this.performSearch();
        } else {
            console.error('Search input not found!');
        }
    }
}

// Initialize the enhanced app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new EnhancedInfinitySearchApp();
    
    // Save analytics periodically
    setInterval(() => {
        if (window.app) {
            window.app.saveAnalytics();
        }
    }, 30000); // Save every 30 seconds
});

// Add enhanced CSS for dynamic elements
const enhancedStyles = `
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .notification-content i {
        font-size: 1.2rem;
    }
    
    .stone-ripple {
        position: absolute;
        border: 2px solid currentColor;
        border-radius: 50%;
        pointer-events: none;
        opacity: 0.8;
    }
    
    .suggestion-item {
        padding: 0.8rem 1.2rem;
        cursor: pointer;
        border-bottom: 1px solid rgba(74, 144, 226, 0.2);
        transition: all 0.2s ease;
        background: rgba(26, 26, 46, 0.9);
    }
    
    .suggestion-item:hover {
        background: rgba(74, 144, 226, 0.1);
        transform: translateX(5px);
    }
    
    .search-suggestions {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: rgba(26, 26, 46, 0.95);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 0 0 20px 20px;
        backdrop-filter: blur(15px);
        z-index: 100;
        max-height: 250px;
        overflow-y: auto;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .stone-usage-item, .query-item, .category-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid rgba(74, 144, 226, 0.1);
        transition: all 0.2s ease;
    }
    
    .stone-usage-item:hover, .query-item:hover, .category-item:hover {
        background: rgba(74, 144, 226, 0.05);
        transform: translateX(5px);
    }
    
    .pagination-container {
        margin-top: 2rem;
        padding: 1.5rem;
        background: rgba(26, 26, 46, 0.9);
        border-radius: 20px;
        border: 1px solid rgba(74, 144, 226, 0.3);
        backdrop-filter: blur(15px);
        text-align: center;
    }
    
    .pagination-info {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    
    .pagination-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .pagination-btn {
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.8), rgba(53, 122, 189, 0.8));
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .pagination-btn:hover:not(:disabled) {
        background: linear-gradient(135deg, rgba(74, 144, 226, 1), rgba(53, 122, 189, 1));
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4);
    }
    
    .pagination-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }
    
    .page-info {
        color: white;
        font-weight: 600;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .usage-bar, .power-bar {
        flex: 1;
        height: 10px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        margin: 0 1rem;
        overflow: hidden;
        position: relative;
    }
    
    .usage-fill, .power-fill {
        height: 100%;
        border-radius: 5px;
        transition: width 0.5s ease;
        position: relative;
    }
    
    .usage-fill::after, .power-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmer 2s ease-in-out infinite;
    }
    
    .usage-fill.space, .power-fill.space { background: var(--gradient-space); }
    .usage-fill.mind, .power-fill.mind { background: var(--gradient-mind); }
    .usage-fill.reality, .power-fill.reality { background: var(--gradient-reality); }
    .usage-fill.power, .power-fill.power { background: var(--gradient-power); }
    .usage-fill.time, .power-fill.time { background: var(--gradient-time); }
    .usage-fill.soul, .power-fill.soul { background: var(--gradient-soul); }
    
    .detail-grid {
        display: grid;
        gap: 0.8rem;
    }
    
    .detail-item {
        display: flex;
        justify-content: space-between;
        padding: 0.8rem 0;
        border-bottom: 1px solid rgba(74, 144, 226, 0.1);
        transition: all 0.2s ease;
    }
    
    .detail-item:hover {
        background: rgba(74, 144, 226, 0.05);
        transform: translateX(5px);
    }
    
    .detail-label {
        font-weight: 700;
        color: var(--text-secondary);
        min-width: 120px;
    }
    
    .detail-value {
        color: var(--text-primary);
        text-align: right;
        flex: 1;
    }
    
    .stone-powers-grid {
        display: grid;
        gap: 1.5rem;
    }
    
    .stone-power-item {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .stone-name {
        min-width: 120px;
        font-weight: 700;
        color: var(--text-secondary);
    }
    
    .power-value {
        min-width: 60px;
        text-align: right;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .no-results {
        grid-column: 1 / -1;
        text-align: center;
        padding: 4rem;
        color: var(--text-secondary);
    }
    
    .no-results h3 {
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .no-results p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
`;

// Inject enhanced styles
const styleSheet = document.createElement('style');
styleSheet.textContent = enhancedStyles;
document.head.appendChild(styleSheet);
