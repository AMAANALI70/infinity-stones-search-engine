"""
Infinity Stones Search Engine
Inspired by the Marvel Cinematic Universe Infinity Stones concept
Each stone represents a different aspect of search functionality

Author: Amaan Ali D Doddamani
Task 05: Search Engine Implementation
"""

import json
import re
import math
from typing import Dict, List, Any, Tuple, Optional, Set
from collections import defaultdict, Counter
import time
import logging
from dataclasses import dataclass
from enum import Enum
from functools import wraps
try:
    from advanced_caching import global_cache_system, global_performance_monitor, global_cache_warmer
    ADVANCED_CACHING_AVAILABLE = True
except ImportError:
    ADVANCED_CACHING_AVAILABLE = False
    logger.warning("Advanced caching not available - using basic caching")

try:
    from advanced_search_features import global_fuzzy_engine, global_boolean_engine, FacetedSearchEngine
    ADVANCED_SEARCH_AVAILABLE = True
except ImportError:
    ADVANCED_SEARCH_AVAILABLE = False
    logger.warning("Advanced search features not available - using basic search")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchEngineError(Exception):
    """Base exception class for search engine errors"""
    pass

class DataLoadError(SearchEngineError):
    """Raised when data loading fails"""
    pass

class SearchError(SearchEngineError):
    """Raised when search operation fails"""
    pass

class ValidationError(SearchEngineError):
    """Raised when input validation fails"""
    pass

def handle_errors(func):
    """Decorator for graceful error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            if isinstance(e, SearchEngineError):
                raise
            raise SearchError(f"Unexpected error in {func.__name__}: {str(e)}") from e
    return wrapper

def validate_query(query: str) -> str:
    """Validate and sanitize search query"""
    if not query or not isinstance(query, str):
        raise ValidationError("Query must be a non-empty string")
    
    # Clean and sanitize query
    cleaned_query = query.strip()
    if len(cleaned_query) == 0:
        raise ValidationError("Query cannot be empty or whitespace only")
    
    if len(cleaned_query) > 500:
        logger.warning(f"Query truncated from {len(cleaned_query)} to 500 characters")
        cleaned_query = cleaned_query[:500]
    
    # Remove potentially dangerous characters
    cleaned_query = re.sub(r'[<>"\']', '', cleaned_query)
    
    return cleaned_query

def safe_get_field(data: Dict[str, Any], field: str, default: Any = None) -> Any:
    """Safely get field from data with fallback"""
    try:
        value = data.get(field, default)
        if value is None or (isinstance(value, str) and value.strip() == ''):
            return default
        return value
    except Exception:
        return default

class StoneType(Enum):
    SPACE = "Space Stone"      # EDA - Data exploration and indexing
    MIND = "Mind Stone"        # Visualization - Search interface and results
    REALITY = "Reality Stone"  # Domain Knowledge - Product categorization
    POWER = "Power Stone"      # Compute Resources - Search algorithms
    TIME = "Time Stone"        # Algorithm Selection - Search optimization
    SOUL = "Soul Stone"        # Business Intelligence - Analytics

@dataclass
class SearchResult:
    product_id: str
    product_data: Dict[str, Any]
    relevance_score: float
    stone_powers: Dict[StoneType, float]
    matched_fields: List[str]

class InfinityStonesSearchEngine:
    """
    A search engine powered by the six Infinity Stones, each representing
    a different aspect of search functionality based on computer science principles.
    
    Implements the fundamental search engine principles:
    1. Crawling - Data discovery and collection
    2. Indexing - Content organization and cataloging  
    3. Ranking - Relevance scoring and result ordering
    """
    
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.products = []
        
        # Core Search Engine Components
        self.index = defaultdict(list)  # Inverted index for fast text search
        self.category_index = defaultdict(list)  # Category-based indexing
        self.brand_index = defaultdict(list)  # Brand-based indexing
        self.feature_index = defaultdict(list)  # Feature-based indexing
        self.authority_scores = {}  # Page authority (like PageRank)
        self.freshness_scores = {}  # Content freshness scores
        self.user_experience_scores = {}  # UX quality scores
        
        # Search Engine Fundamentals
        if ADVANCED_CACHING_AVAILABLE:
            self.search_cache = global_cache_system.get_query_cache()
            self.index_cache = global_cache_system.get_index_cache()
            self.analytics_cache = global_cache_system.get_analytics_cache()
            self.performance_monitor = global_performance_monitor
            self.cache_warmer = global_cache_warmer
            print("🚀 Advanced caching system initialized")
        else:
            self.search_cache = {}  # Fallback to basic caching
            
        self.crawl_history = []  # Track data discovery
        self.index_statistics = {}  # Index quality metrics
        
        self.analytics = {
            'total_searches': 0,
            'popular_queries': Counter(),
            'search_times': [],
            'stone_usage': Counter()
        }
        
        # Initialize the stones
        self.stones = {
            StoneType.SPACE: SpaceStone(self),
            StoneType.MIND: MindStone(self),
            StoneType.REALITY: RealityStone(self),
            StoneType.POWER: PowerStone(self),
            StoneType.TIME: TimeStone(self),
            StoneType.SOUL: SoulStone(self)
        }
        
        self._load_data()
        self._build_indexes()
        
        # Initialize advanced search features
        if ADVANCED_SEARCH_AVAILABLE:
            self.faceted_engine = FacetedSearchEngine(self.products)
            self.fuzzy_engine = global_fuzzy_engine
            self.boolean_engine = global_boolean_engine
            print("🎆 Advanced search features initialized (fuzzy, boolean, faceted)")
        else:
            self.faceted_engine = None
    
    @handle_errors
    def _load_data(self):
        """Load the e-commerce dataset (Crawling Phase)"""
        print("🔮 Loading dataset with the Power of the Space Stone...")
        print("🌐 Phase 1: CRAWLING - Discovering and collecting data...")
        
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validate loaded data
            if not isinstance(data, list):
                raise DataLoadError(f"Expected list of products, got {type(data)}")
            
            if len(data) == 0:
                raise DataLoadError("Dataset is empty")
            
            # Filter and validate products
            valid_products = []
            for i, product in enumerate(data):
                if not isinstance(product, dict):
                    logger.warning(f"Skipping invalid product at index {i}: not a dictionary")
                    continue
                
                # Ensure product has minimum required fields
                if not product.get('id'):
                    product['id'] = f"product_{i}"  # Generate ID if missing
                
                valid_products.append(product)
            
            self.products = valid_products
            
            if len(valid_products) < len(data):
                logger.warning(f"Filtered out {len(data) - len(valid_products)} invalid products")
            
            print(f"✨ Crawled {len(self.products)} products into the cosmic database")
            
            # Record crawling activity
            self.crawl_history.append({
                'timestamp': time.time(),
                'source': self.dataset_path,
                'products_discovered': len(self.products),
                'crawl_type': 'initial_dataset_load',
                'validation_errors': len(data) - len(valid_products)
            })
            
        except FileNotFoundError:
            raise DataLoadError(f"Dataset file not found: {self.dataset_path}")
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Invalid JSON format in dataset: {str(e)}")
        except PermissionError:
            raise DataLoadError(f"Permission denied accessing dataset: {self.dataset_path}")
    
    def _build_indexes(self):
        """Build various indexes for efficient searching (Indexing Phase)"""
        print("🌌 Phase 2: INDEXING - Creating catalog and organizing data...")
        
        index_stats = {
            'total_terms': 0,
            'unique_terms': 0,
            'categories_found': 0,
            'brands_found': 0,
            'features_found': 0
        }
        
        for product in self.products:
            product_id = product.get('id', '')
            
            # Calculate authority scores (like PageRank)
            self.authority_scores[product_id] = self._calculate_authority_score(product)
            
            # Calculate freshness scores
            self.freshness_scores[product_id] = self._calculate_freshness_score(product)
            
            # Calculate UX scores
            self.user_experience_scores[product_id] = self._calculate_ux_score(product)
            
            # Build inverted text index (core search engine component)
            for key, value in product.items():
                if isinstance(value, str):
                    words = re.findall(r'\b\w+\b', value.lower())
                    for word in words:
                        self.index[word].append(product_id)
                        index_stats['total_terms'] += 1
            
            # Build category index
            if 'Type' in product:
                category = product['Type'].lower()
                self.category_index[category].append(product_id)
                index_stats['categories_found'] += 1
            
            # Build brand index
            if 'Brand' in product:
                brand = product['Brand'].lower()
                self.brand_index[brand].append(product_id)
                index_stats['brands_found'] += 1
            
            # Build feature index
            for key, value in product.items():
                if key not in ['id'] and isinstance(value, str):
                    self.feature_index[key.lower()].append(product_id)
                    index_stats['features_found'] += 1
        
        # Calculate index statistics
        index_stats['unique_terms'] = len(self.index)
        self.index_statistics = index_stats
        
        print(f"📊 Index Statistics:")
        print(f"   • Unique terms indexed: {index_stats['unique_terms']:,}")
        print(f"   • Total term occurrences: {index_stats['total_terms']:,}")
        print(f"   • Categories found: {index_stats['categories_found']}")
        print(f"   • Brands found: {index_stats['brands_found']}")
        print(f"   • Features found: {index_stats['features_found']}")
        print("✨ Search engine ready!")
    
    def _calculate_authority_score(self, product: Dict[str, Any]) -> float:
        """Calculate authority score (like PageRank) based on product quality indicators"""
        score = 0.0
        
        # Brand authority (well-known brands get higher scores)
        if 'Brand' in product and product['Brand']:
            brand = product['Brand'].lower()
            # Popular brands get higher authority
            if brand in ['samsung', 'apple', 'sony', 'lg', 'xiaomi', 'oneplus']:
                score += 0.4
            elif brand in ['realme', 'vivo', 'oppo', 'huawei', 'motorola']:
                score += 0.3
            else:
                score += 0.2
        
        # Product completeness (more complete product info = higher authority)
        required_fields = ['Name', 'Type', 'Brand', 'Sales Package']
        completeness = sum(1 for field in required_fields if field in product and product[field])
        score += (completeness / len(required_fields)) * 0.3
        
        # Product description quality
        if 'Sales Package' in product and product['Sales Package']:
            description_length = len(product['Sales Package'])
            if description_length > 100:
                score += 0.2
            elif description_length > 50:
                score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_freshness_score(self, product: Dict[str, Any]) -> float:
        """Calculate freshness score based on product recency indicators"""
        # For e-commerce, we'll use product ID patterns or other indicators
        # In a real system, this would be based on actual timestamps
        
        score = 0.5  # Base freshness score
        
        # Newer product IDs might indicate fresher products
        if 'id' in product:
            product_id = product['id']
            # Simple heuristic: longer IDs might indicate newer products
            if len(product_id) > 10:
                score += 0.2
            elif len(product_id) > 5:
                score += 0.1
        
        # Products with more detailed information might be more recently updated
        if 'Sales Package' in product and product['Sales Package']:
            if len(product['Sales Package']) > 200:
                score += 0.2
            elif len(product['Sales Package']) > 100:
                score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_ux_score(self, product: Dict[str, Any]) -> float:
        """Calculate user experience score based on product information quality"""
        score = 0.0
        
        # Information completeness
        if 'Name' in product and product['Name']:
            score += 0.2
        if 'Type' in product and product['Type']:
            score += 0.2
        if 'Brand' in product and product['Brand']:
            score += 0.2
        if 'Sales Package' in product and product['Sales Package']:
            score += 0.2
        
        # Information quality
        if 'Sales Package' in product and product['Sales Package']:
            description = product['Sales Package']
            # Check for detailed descriptions
            if len(description) > 50:
                score += 0.1
            # Check for technical specifications
            if any(keyword in description.lower() for keyword in ['gb', 'inch', 'mp', 'mah', 'hz']):
                score += 0.1
        
        return min(score, 1.0)
    
    def _apply_ranking_algorithms(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        """
        Apply advanced ranking algorithms based on search engine fundamentals:
        - Keyword Relevance
        - Content Quality
        - User Experience
        - Authority and Backlinks (product authority)
        - Freshness
        """
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        
        for result in results:
            product = result.product_data
            product_id = result.product_id
            
            # 1. Keyword Relevance (TF-IDF based)
            keyword_score = self._calculate_keyword_relevance(query_words, product)
            
            # 2. Content Quality Score
            content_quality = self._calculate_content_quality(product)
            
            # 3. User Experience Score
            ux_score = self.user_experience_scores.get(product_id, 0.5)
            
            # 4. Authority Score (like PageRank)
            authority_score = self.authority_scores.get(product_id, 0.5)
            
            # 5. Freshness Score
            freshness_score = self.freshness_scores.get(product_id, 0.5)
            
            # Combine all ranking factors
            final_score = (
                keyword_score * 0.4 +      # 40% - Keyword relevance
                content_quality * 0.2 +    # 20% - Content quality
                ux_score * 0.15 +          # 15% - User experience
                authority_score * 0.15 +   # 15% - Authority
                freshness_score * 0.1      # 10% - Freshness
            )
            
            # Update the result with the new score
            result.relevance_score = final_score
        
        # Sort results by final relevance score
        ranked_results = sorted(results, key=lambda x: x.relevance_score, reverse=True)
        
        print(f"📊 Ranking applied to {len(ranked_results)} results")
        if ranked_results:
            print(f"   • Top result score: {ranked_results[0].relevance_score:.3f}")
            top_10 = ranked_results[:10]
            if top_10:
                print(f"   • Average score: {sum(r.relevance_score for r in top_10)/len(top_10):.3f}")
        
        return ranked_results
    
    def _calculate_keyword_relevance(self, query_words: set, product: Dict[str, Any]) -> float:
        """Calculate keyword relevance using TF-IDF principles"""
        score = 0.0
        total_words = 0
        
        for key, value in product.items():
            if isinstance(value, str):
                words = re.findall(r'\b\w+\b', value.lower())
                total_words += len(words)
                
                # Count query word matches
                for word in words:
                    if word in query_words:
                        # Different fields have different weights
                        if key == 'Name':
                            score += 3.0  # Product name matches are most important
                        elif key == 'Type':
                            score += 2.0  # Category matches are important
                        elif key == 'Brand':
                            score += 2.0  # Brand matches are important
                        else:
                            score += 1.0  # Other field matches
        
        # Normalize by total words (TF component)
        if total_words > 0:
            score = score / total_words
        
        return min(score, 1.0)
    
    def _calculate_content_quality(self, product: Dict[str, Any]) -> float:
        """Calculate content quality score"""
        score = 0.0
        
        # Information completeness
        required_fields = ['Name', 'Type', 'Brand', 'Sales Package']
        completeness = sum(1 for field in required_fields if field in product and product[field])
        score += (completeness / len(required_fields)) * 0.4
        
        # Description quality
        if 'Sales Package' in product and product['Sales Package']:
            description = product['Sales Package']
            # Length indicates detail
            if len(description) > 200:
                score += 0.3
            elif len(description) > 100:
                score += 0.2
            elif len(description) > 50:
                score += 0.1
            
            # Technical specifications indicate quality
            tech_indicators = ['gb', 'inch', 'mp', 'mah', 'hz', 'ram', 'storage', 'camera']
            tech_count = sum(1 for indicator in tech_indicators if indicator in description.lower())
            score += min(tech_count * 0.05, 0.3)
        
        return min(score, 1.0)
    
    @handle_errors
    def search(self, query: str, stone_preference: StoneType = None) -> List[SearchResult]:
        """
        Perform a search using the combined power of all Infinity Stones
        Implements the three fundamental phases: Crawling, Indexing, and Ranking
        """
        start_time = time.time()
        
        # Validate query
        try:
            cleaned_query = validate_query(query)
        except ValidationError as e:
            logger.error(f"Query validation failed: {e}")
            return []  # Return empty results for invalid queries
        
        # Check if search engine is properly initialized
        if not self.products:
            logger.error("Search engine not initialized - no products loaded")
            raise SearchError("Search engine not initialized properly")
        
        self.analytics['total_searches'] += 1
        self.analytics['popular_queries'][cleaned_query.lower()] += 1
        
        # Use Time Stone for caching
        cache_key = f"{cleaned_query}_{stone_preference}"
        
        # Try advanced cache first
        if ADVANCED_CACHING_AVAILABLE:
            cached_results = self.search_cache.get(cache_key)
            if cached_results is not None:
                print("⏰ Time Stone: Retrieving from advanced LRU cache...")
                search_time = time.time() - start_time
                self.analytics['search_times'].append(search_time)
                return cached_results
        else:
            # Fallback to basic cache
            if cache_key in self.search_cache:
                print("⏰ Time Stone: Retrieving from basic cache...")
                cached_results = self.search_cache[cache_key]
                search_time = time.time() - start_time
                self.analytics['search_times'].append(search_time)
                return cached_results
        
        print(f"🔍 Searching for '{cleaned_query}' with the power of the Infinity Stones...")
        print("🎯 Phase 3: RANKING - Applying relevance algorithms...")
        
        # Get results from each stone with error handling
        stone_results = {}
        search_errors = []
        
        for stone_type, stone in self.stones.items():
            if stone_preference is None or stone_type == stone_preference:
                try:
                    results = stone.search(cleaned_query)
                    stone_results[stone_type] = results if results else []
                    self.analytics['stone_usage'][stone_type] += 1
                except Exception as e:
                    logger.error(f"Error in {stone_type.value}: {str(e)}")
                    search_errors.append((stone_type, str(e)))
                    stone_results[stone_type] = []  # Continue with empty results
        
        # Check if we have any results
        total_results = sum(len(results) for results in stone_results.values())
        if total_results == 0:
            logger.warning(f"No results found for query: '{cleaned_query}'")
            if search_errors:
                logger.error(f"Search errors encountered: {search_errors}")
            return []
        
        # Combine results using the Power Stone
        combined_results = self.stones[StoneType.POWER].combine_results(stone_results)
        
        # Apply advanced ranking algorithms
        ranked_results = self._apply_ranking_algorithms(query, combined_results)
        
        # Apply Soul Stone analytics
        self.stones[StoneType.SOUL].analyze_search(query, ranked_results)
        
        search_time = time.time() - start_time
        self.analytics['search_times'].append(search_time)
        
        # Cache results with Time Stone
        if ADVANCED_CACHING_AVAILABLE:
            self.search_cache.put(cache_key, ranked_results)
            # Record performance snapshot
            self.performance_monitor.record_performance_snapshot()
        else:
            self.search_cache[cache_key] = ranked_results
        
        print(f"✨ Search completed in {search_time:.3f} seconds")
        return ranked_results
    
    def search_boolean(self, boolean_query: str, stone_preference: StoneType = None) -> List[SearchResult]:
        """
        Perform boolean search with AND/OR/NOT operators
        """
        if not ADVANCED_SEARCH_AVAILABLE:
            logger.warning("Boolean search not available - falling back to regular search")
            return self.search(boolean_query, stone_preference)
        
        try:
            # Parse boolean query
            parsed_query = self.boolean_engine.parse_boolean_query(boolean_query)
            
            if not parsed_query['success']:
                logger.warning(f"Boolean parsing failed: {parsed_query.get('error', 'Unknown error')}")
                # Fallback to regular search with individual terms
                fallback_terms = parsed_query.get('fallback_terms', [boolean_query])
                return self.search(' '.join(fallback_terms), stone_preference)
            
            print(f"🧠 Boolean Search: Parsed '{boolean_query}' successfully")
            
            # Build product matches for each term
            product_matches = {}
            all_terms = self._extract_terms_from_expression(parsed_query['expression'])
            
            for term in all_terms:
                matching_products = set()
                for product in self.products:
                    product_text = ' '.join(str(v) for v in product.values() if isinstance(v, str)).lower()
                    if term.lower() in product_text:
                        matching_products.add(product.get('id', ''))
                product_matches[term] = matching_products
            
            # Evaluate boolean expression
            matching_product_ids = self.boolean_engine.evaluate_boolean_expression(
                parsed_query['expression'], product_matches
            )
            
            # Convert to SearchResult objects
            results = []
            for product in self.products:
                if product.get('id', '') in matching_product_ids:
                    result = SearchResult(
                        product_id=product.get('id', ''),
                        product_data=product,
                        relevance_score=1.0,  # Base score for boolean matches
                        stone_powers={StoneType.MIND: 1.0},
                        matched_fields=['boolean_search']
                    )
                    results.append(result)
            
            print(f"🎯 Boolean Search: Found {len(results)} products matching expression")
            return results  # Return all results
            
        except Exception as e:
            logger.error(f"Boolean search failed: {e}")
            return self.search(boolean_query, stone_preference)
    
    def _extract_terms_from_expression(self, expression: Dict[str, Any]) -> Set[str]:
        """Extract all search terms from a boolean expression"""
        terms = set()
        
        if expression['type'] == 'term':
            terms.add(expression['value'])
        elif expression['type'] in ['and', 'or']:
            terms.update(self._extract_terms_from_expression(expression['left']))
            terms.update(self._extract_terms_from_expression(expression['right']))
        elif expression['type'] == 'not':
            terms.update(self._extract_terms_from_expression(expression['operand']))
        
        return terms
    
    def get_facets(self) -> Dict[str, Any]:
        """
        Get available facets for filtering
        """
        if not ADVANCED_SEARCH_AVAILABLE or not self.faceted_engine:
            return {'error': 'Faceted search not available'}
        
        return {
            'success': True,
            'facets': self.faceted_engine.get_facets(),
            'total_products': len(self.products)
        }
    
    def search_with_facets(self, query: str, facet_filters: Dict[str, List[str]] = None, stone_preference: StoneType = None) -> Dict[str, Any]:
        """
        Perform search with faceted filtering
        
        Args:
            query: Search query
            facet_filters: Dict of facet filters, e.g., {'brand': ['Samsung'], 'category': ['Mobile']}
            stone_preference: Preferred stone for search
        
        Returns:
            Dict with results and facet information
        """
        # Perform regular search first
        search_results = self.search(query, stone_preference)
        
        if not ADVANCED_SEARCH_AVAILABLE or not self.faceted_engine:
            return {
                'success': True,
                'results': search_results,
                'facets': {},
                'total_results': len(search_results),
                'filtered_results': len(search_results)
            }
        
        # Extract product IDs from search results
        result_product_ids = {result.product_id for result in search_results}
        
        # Apply facet filters if provided
        if facet_filters:
            filtered_product_ids = self.faceted_engine.filter_by_facets(result_product_ids, facet_filters)
            
            # Filter search results to only include filtered products
            filtered_results = [
                result for result in search_results 
                if result.product_id in filtered_product_ids
            ]
            
            print(f"🎯 Faceted Search: Filtered from {len(search_results)} to {len(filtered_results)} results")
        else:
            filtered_results = search_results
        
        return {
            'success': True,
            'results': filtered_results,
            'facets': self.faceted_engine.get_facets(),
            'total_results': len(search_results),
            'filtered_results': len(filtered_results),
            'applied_filters': facet_filters or {}
        }
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get search analytics from the Soul Stone"""
        return self.stones[StoneType.SOUL].get_analytics()

class SpaceStone:
    """
    Space Stone - Data & Indexing
    Controls where things exist, just like data placement and indexing.
    
    Search engine aspects:
    - Efficient inverted index (where words live)
    - Partitioning/sharding across servers
    - Metadata storage (space to organize filters)
    - Without it → chaos, no structure, search can't find "where" info is
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.shard_metadata = {}  # Simulate sharding metadata
        self.index_statistics = {
            'total_documents': 0,
            'unique_terms': 0,
            'index_size_mb': 0,
            'shard_count': 1
        }
        self._initialize_sharding()
    
    def _initialize_sharding(self):
        """Initialize data sharding for scalability"""
        # Simulate sharding by product ID ranges
        total_products = len(self.engine.products)
        shard_size = max(1000, total_products // 10)  # 10 shards max
        
        for i, product in enumerate(self.engine.products):
            shard_id = i // shard_size
            if shard_id not in self.shard_metadata:
                self.shard_metadata[shard_id] = {
                    'start_id': i,
                    'end_id': min(i + shard_size - 1, total_products - 1),
                    'product_count': 0,
                    'terms_count': 0
                }
            self.shard_metadata[shard_id]['product_count'] += 1
        
        self.index_statistics['shard_count'] = len(self.shard_metadata)
        self.index_statistics['total_documents'] = total_products
    
    def search(self, query: str) -> List[SearchResult]:
        """Explore the data space using efficient inverted index"""
        print("🌌 Space Stone: Accessing distributed index...")
        
        query_words = re.findall(r'\b\w+\b', query.lower())
        product_scores = defaultdict(float)
        matched_fields = defaultdict(set)
        shard_hits = defaultdict(int)
        
        # Search across all shards (simulated distributed search)
        for word in query_words:
            if word in self.engine.index:
                # Simulate shard-based search
                for product_id in self.engine.index[word]:
                    shard_id = self._get_shard_for_product(product_id)
                    shard_hits[shard_id] += 1
                    
                    product_scores[product_id] += 1
                    matched_fields[product_id].add(f"inverted_index_{word}")
        
        # Add sharding metadata to results
        results = []
        for product_id, score in product_scores.items():
            product = next((p for p in self.engine.products if p.get('id') == product_id), None)
            if product:
                shard_id = self._get_shard_for_product(product_id)
                result = SearchResult(
                    product_id=product_id,
                    product_data=product,
                    relevance_score=score,
                    stone_powers={StoneType.SPACE: score},
                    matched_fields=list(matched_fields[product_id])
                )
                # Add shard metadata
                result.product_data['_shard_id'] = shard_id
                result.product_data['_shard_hits'] = shard_hits[shard_id]
                results.append(result)
        
        # Sort and limit for performance
        sorted_results = sorted(results, key=lambda x: x.relevance_score, reverse=True)
        limited_results = sorted_results[:500]  # Limit Space Stone results for better performance
        print(f"📈 Space Stone: Searched {len(self.shard_metadata)} shards, found {len(limited_results)} results (limited from {len(results)})")
        return limited_results
    
    def _get_shard_for_product(self, product_id: str) -> int:
        """Determine which shard a product belongs to"""
        # Simple hash-based sharding
        if len(self.shard_metadata) == 0:
            return 0
        return hash(product_id) % len(self.shard_metadata)
    
    def get_index_statistics(self) -> Dict[str, Any]:
        """Get comprehensive index statistics"""
        return {
            'index_statistics': self.index_statistics,
            'shard_metadata': self.shard_metadata,
            'index_health': {
                'shard_balance': self._calculate_shard_balance(),
                'index_efficiency': self._calculate_index_efficiency(),
                'storage_utilization': self._calculate_storage_utilization()
            }
        }
    
    def _calculate_shard_balance(self) -> float:
        """Calculate how balanced the shards are"""
        if not self.shard_metadata:
            return 1.0
        
        counts = [shard['product_count'] for shard in self.shard_metadata.values()]
        return 1.0 - (max(counts) - min(counts)) / max(counts) if max(counts) > 0 else 1.0
    
    def _calculate_index_efficiency(self) -> float:
        """Calculate index efficiency metrics"""
        total_terms = sum(len(self.engine.index[term]) for term in self.engine.index)
        unique_terms = len(self.engine.index)
        return unique_terms / total_terms if total_terms > 0 else 0.0
    
    def _calculate_storage_utilization(self) -> float:
        """Calculate storage utilization"""
        # Simulate storage calculation
        return min(1.0, len(self.engine.products) / 50000)  # Assume 50k is max capacity

class MindStone:
    """
    Mind Stone - Query Understanding & User Experience
    Powers perception & influence, like how the system interprets user intent.
    
    Search engine aspects:
    - Natural Language Processing (NLP) for intent
    - Synonym handling, spell correction, query expansion
    - Autocomplete, query suggestions
    - UX features: highlighting, snippets, faceted filters
    - Without it → the engine is "mindless," only doing raw string matching
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.synonyms = {
            'phone': ['mobile', 'cellphone', 'smartphone', 'device'],
            'laptop': ['notebook', 'computer', 'pc'],
            'headphone': ['earphone', 'earbud', 'headset'],
            'charger': ['adapter', 'power', 'cable'],
            'case': ['cover', 'protector', 'shell'],
            'bluetooth': ['wireless', 'bt'],
            'camera': ['photo', 'picture', 'image'],
            'battery': ['power', 'charge'],
            'screen': ['display', 'monitor'],
            'memory': ['storage', 'ram', 'gb']
        }
        self.spell_corrections = {
            'phne': 'phone',
            'lptop': 'laptop',
            'hedphone': 'headphone',
            'blutooth': 'bluetooth',
            'camra': 'camera',
            'batry': 'battery',
            'scrn': 'screen',
            'memry': 'memory'
        }
        self.query_intent_patterns = {
            'comparison': ['vs', 'versus', 'compare', 'better', 'best'],
            'specification': ['specs', 'specifications', 'features', 'details'],
            'price': ['price', 'cost', 'cheap', 'expensive', 'budget'],
            'brand': ['brand', 'make', 'manufacturer'],
            'category': ['type', 'kind', 'category']
        }
    
    def search(self, query: str) -> List[SearchResult]:
        """Understand user intent and present results with enhanced UX"""
        print("🧠 Mind Stone: Analyzing user intent and enhancing UX...")
        
        # 1. Query Understanding & NLP
        processed_query = self._process_query(query)
        intent = self._detect_intent(query)
        
        # 2. Get base results from Space Stone
        space_results = self.engine.stones[StoneType.SPACE].search(processed_query)
        
        # 3. Enhance with UX features
        enhanced_results = self._enhance_ux_features(space_results, query, intent)
        
        print(f"🎯 Mind Stone: Detected intent: {intent['type']}, confidence: {intent['confidence']:.2f}")
        return enhanced_results
    
    def _process_query(self, query: str) -> str:
        """Process query with NLP techniques including fuzzy search"""
        processed = query.lower().strip()
        
        # 1. Spell correction
        words = processed.split()
        corrected_words = []
        fuzzy_corrections = []
        
        for word in words:
            if word in self.spell_corrections:
                corrected_words.append(self.spell_corrections[word])
                print(f"🔧 Mind Stone: Corrected '{word}' → '{self.spell_corrections[word]}'")
            else:
                # Simple fuzzy matching - only for obvious typos
                if ADVANCED_SEARCH_AVAILABLE and hasattr(self.engine, 'fuzzy_engine') and len(word) > 4:
                    try:
                        # Very conservative fuzzy matching
                        common_terms = ['mobile', 'phone', 'laptop', 'computer', 'headphone', 'camera', 'battery']
                        fuzzy_matches = self.engine.fuzzy_engine.find_fuzzy_matches(word, common_terms, max_results=1)
                        
                        if fuzzy_matches and fuzzy_matches[0].similarity > 0.9:
                            best_match = fuzzy_matches[0]
                            corrected_words.append(best_match.matched_term)
                            print(f"🎯 Mind Stone: Fuzzy matched '{word}' → '{best_match.matched_term}' (similarity: {best_match.similarity:.2f})")
                        else:
                            corrected_words.append(word)
                    except Exception:
                        corrected_words.append(word)
                else:
                    corrected_words.append(word)
        
        # 2. Query expansion with synonyms - conservative expansion
        expanded_words = []
        
        for word in corrected_words:
            expanded_words.append(word)
            # Expand synonyms for short queries only
            if word in self.synonyms and len(corrected_words) <= 3:
                # Add 1-2 synonyms based on query length
                synonym_count = 1 if len(corrected_words) > 1 else 2
                expanded_words.extend(self.synonyms[word][:synonym_count])
        
        processed_query = ' '.join(expanded_words)
        
        # Store fuzzy corrections for analytics
        if fuzzy_corrections:
            if not hasattr(self, 'fuzzy_correction_stats'):
                self.fuzzy_correction_stats = []
            self.fuzzy_correction_stats.extend(fuzzy_corrections)
        
        return processed_query
    
    def _detect_intent(self, query: str) -> Dict[str, Any]:
        """Detect user intent using pattern matching"""
        query_lower = query.lower()
        intent_scores = {}
        
        for intent_type, patterns in self.query_intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            if score > 0:
                intent_scores[intent_type] = score / len(patterns)
        
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return {
                'type': best_intent[0],
                'confidence': best_intent[1],
                'all_scores': intent_scores
            }
        else:
            return {
                'type': 'general_search',
                'confidence': 0.5,
                'all_scores': {}
            }
    
    def _enhance_ux_features(self, results: List[SearchResult], original_query: str, intent: Dict[str, Any]) -> List[SearchResult]:
        """Enhance results with UX features"""
        enhanced_results = []
        query_words = set(re.findall(r'\b\w+\b', original_query.lower()))
        
        # Limit processing to improve performance
        for result in results[:200]:  # Process top 200 results only
            # Add highlighting information
            highlighted_fields = self._add_highlighting(result.product_data, query_words)
            result.product_data['_highlighted'] = highlighted_fields
            
            # Add snippet generation
            snippet = self._generate_snippet(result.product_data, query_words)
            result.product_data['_snippet'] = snippet
            
            # Add faceted filter information
            facets = self._extract_facets(result.product_data)
            result.product_data['_facets'] = facets
            
            # Add intent-based scoring boost
            intent_boost = self._calculate_intent_boost(result, intent)
            result.relevance_score += intent_boost
            
            enhanced_results.append(result)
        
        # Add the remaining results without enhancement for performance
        enhanced_results.extend(results[200:])
        
        return enhanced_results
    
    def _add_highlighting(self, product: Dict[str, Any], query_words: set) -> Dict[str, str]:
        """Add highlighting to matched text"""
        highlighted = {}
        
        for key, value in product.items():
            if isinstance(value, str):
                highlighted_text = value
                for word in query_words:
                    if word in value.lower():
                        # Simple highlighting with <mark> tags
                        highlighted_text = re.sub(
                            f'\\b{re.escape(word)}\\b',
                            f'<mark>{word}</mark>',
                            highlighted_text,
                            flags=re.IGNORECASE
                        )
                highlighted[key] = highlighted_text
        
        return highlighted
    
    def _generate_snippet(self, product: Dict[str, Any], query_words: set) -> str:
        """Generate a relevant snippet for the product"""
        # Use Sales Package or Name for snippet
        snippet_source = product.get('Sales Package', product.get('Name', ''))
        
        if not snippet_source:
            return "No description available"
        
        # Find the best sentence containing query words
        sentences = snippet_source.split('.')
        best_sentence = ""
        max_matches = 0
        
        for sentence in sentences:
            matches = sum(1 for word in query_words if word in sentence.lower())
            if matches > max_matches:
                max_matches = matches
                best_sentence = sentence.strip()
        
        # If no sentence has query words, use first sentence
        if not best_sentence:
            best_sentence = sentences[0].strip() if sentences else snippet_source
        
        # Truncate if too long
        if len(best_sentence) > 150:
            best_sentence = best_sentence[:147] + "..."
        
        return best_sentence
    
    def _extract_facets(self, product: Dict[str, Any]) -> Dict[str, str]:
        """Extract faceted filter information"""
        facets = {}
        
        if 'Type' in product:
            facets['category'] = product['Type']
        if 'Brand' in product:
            facets['brand'] = product['Brand']
        
        # Extract price range if available
        if 'Sales Package' in product:
            package = product['Sales Package']
            # Look for price indicators
            if 'rupee' in package.lower() or 'rs' in package.lower():
                facets['has_price'] = 'true'
        
        return facets
    
    def _calculate_intent_boost(self, result: SearchResult, intent: Dict[str, Any]) -> float:
        """Calculate intent-based relevance boost"""
        boost = 0.0
        
        if intent['type'] == 'comparison':
            # Boost products with detailed specifications
            if 'Sales Package' in result.product_data:
                package = result.product_data['Sales Package']
                if len(package) > 100:  # Detailed descriptions
                    boost += 0.1
        
        elif intent['type'] == 'specification':
            # Boost products with technical details
            if 'Sales Package' in result.product_data:
                package = result.product_data['Sales Package']
                tech_terms = ['gb', 'inch', 'mp', 'mah', 'hz', 'ram', 'storage']
                tech_count = sum(1 for term in tech_terms if term in package.lower())
                boost += min(tech_count * 0.02, 0.1)
        
        elif intent['type'] == 'brand':
            # Boost products with clear brand information
            if 'Brand' in result.product_data and result.product_data['Brand']:
                boost += 0.05
        
        return boost
    
    def _calculate_presentation_score(self, result: SearchResult) -> float:
        """Calculate how well the result can be presented"""
        score = 0.0
        product = result.product_data
        
        # Prefer products with more complete information
        if 'Brand' in product:
            score += 0.2
        if 'Type' in product:
            score += 0.2
        if 'Model Number' in product:
            score += 0.1
        
        return min(score, 1.0)

class RealityStone:
    """
    Reality Stone - Relevance & Adaptability
    Warps reality → a good search engine "warps" raw matches into useful reality for the user.
    
    Search engine aspects:
    - Ranking models (TF-IDF, BM25, embeddings)
    - Personalization & context-aware relevance
    - Business logic: promotions, sponsored results
    - Freshness & diversity (balancing multiple realities)
    - Without it → results don't reflect user's actual needs
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.category_keywords = {
            'electronics': ['electronic', 'digital', 'smart', 'wireless', 'bluetooth', 'usb'],
            'automotive': ['car', 'vehicle', 'automotive', 'auto', 'tire', 'brake'],
            'home': ['home', 'house', 'kitchen', 'bedroom', 'living', 'furniture'],
            'beauty': ['beauty', 'cosmetic', 'makeup', 'skincare', 'hair', 'fragrance'],
            'sports': ['sport', 'fitness', 'exercise', 'gym', 'outdoor', 'athletic']
        }
        self.user_preferences = {}  # Simulate user personalization
        self.business_rules = {
            'promoted_brands': ['samsung', 'apple', 'sony'],
            'sponsored_categories': ['electronics'],
            'freshness_boost': 0.1
        }
        self.diversity_factors = {
            'brand_diversity': True,
            'category_diversity': True,
            'price_diversity': True
        }
    
    def search(self, query: str) -> List[SearchResult]:
        """Warp raw matches into useful reality for the user"""
        print("🔴 Reality Stone: Applying relevance algorithms and personalization...")
        
        # 1. Get base results from Space Stone
        space_results = self.engine.stones[StoneType.SPACE].search(query)
        
        # 2. Apply advanced ranking models
        ranked_results = self._apply_ranking_models(query, space_results)
        
        # 3. Apply personalization
        personalized_results = self._apply_personalization(ranked_results, query)
        
        # 4. Apply business logic
        business_enhanced_results = self._apply_business_logic(personalized_results)
        
        # 5. Ensure diversity
        diverse_results = self._ensure_diversity(business_enhanced_results)
        
        # Limit final results for performance
        final_limited_results = diverse_results[:200]  # Reasonable limit for Reality Stone
        print(f"🎯 Reality Stone: Applied {len(final_limited_results)} reality-warping algorithms")
        return final_limited_results
    
    def _apply_ranking_models(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        """Apply advanced ranking models (TF-IDF, BM25, embeddings)"""
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        
        for result in results:
            # TF-IDF scoring
            tfidf_score = self._calculate_tfidf_score(query_words, result.product_data)
            
            # BM25-like scoring
            bm25_score = self._calculate_bm25_score(query_words, result.product_data)
            
            # Embedding similarity (simulated)
            embedding_score = self._calculate_embedding_similarity(query, result.product_data)
            
            # Combine ranking models
            combined_score = (
                tfidf_score * 0.4 +
                bm25_score * 0.4 +
                embedding_score * 0.2
            )
            
            result.relevance_score = combined_score
            result.stone_powers[StoneType.REALITY] = combined_score
            result.matched_fields.append("reality_ranked")
        
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
    
    def _calculate_tfidf_score(self, query_words: set, product: Dict[str, Any]) -> float:
        """Calculate TF-IDF score for the product"""
        score = 0.0
        total_words = 0
        
        for key, value in product.items():
            if isinstance(value, str):
                words = re.findall(r'\b\w+\b', value.lower())
                total_words += len(words)
                
                for word in words:
                    if word in query_words:
                        # Term frequency
                        tf = words.count(word) / len(words)
                        # Inverse document frequency (simplified)
                        idf = math.log(len(self.engine.products) / (len(self.engine.index.get(word, [])) + 1))
                        score += tf * idf
        
        return score / total_words if total_words > 0 else 0.0
    
    def _calculate_bm25_score(self, query_words: set, product: Dict[str, Any]) -> float:
        """Calculate BM25 score (simplified version)"""
        k1, b = 1.2, 0.75  # BM25 parameters
        avg_doc_length = 50  # Average document length
        
        score = 0.0
        doc_length = sum(len(str(value)) for value in product.values() if isinstance(value, str))
        
        for word in query_words:
            if word in self.engine.index:
                # Document frequency
                df = len(self.engine.index[word])
                # Term frequency in document
                tf = sum(str(value).lower().count(word) for value in product.values() if isinstance(value, str))
                
                if tf > 0:
                    # BM25 formula
                    idf = math.log((len(self.engine.products) - df + 0.5) / (df + 0.5))
                    bm25_term = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avg_doc_length)))
                    score += bm25_term
        
        return score
    
    def _calculate_embedding_similarity(self, query: str, product: Dict[str, Any]) -> float:
        """Simulate embedding similarity calculation"""
        # In a real system, this would use actual embeddings
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        product_text = ' '.join(str(value) for value in product.values() if isinstance(value, str))
        product_words = set(re.findall(r'\b\w+\b', product_text.lower()))
        
        # Jaccard similarity as a proxy for embedding similarity
        intersection = len(query_words.intersection(product_words))
        union = len(query_words.union(product_words))
        
        return intersection / union if union > 0 else 0.0
    
    def _apply_personalization(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """Apply personalization based on user preferences"""
        # Simulate user preferences
        user_id = "default_user"  # In real system, this would be actual user ID
        
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'preferred_brands': ['samsung', 'apple'],
                'preferred_categories': ['electronics'],
                'price_sensitivity': 'medium'
            }
        
        preferences = self.user_preferences[user_id]
        
        for result in results:
            personalization_boost = 0.0
            
            # Brand preference boost
            if 'Brand' in result.product_data:
                brand = result.product_data['Brand'].lower()
                if brand in preferences['preferred_brands']:
                    personalization_boost += 0.1
            
            # Category preference boost
            if 'Type' in result.product_data:
                category = result.product_data['Type'].lower()
                if any(pref_cat in category for pref_cat in preferences['preferred_categories']):
                    personalization_boost += 0.05
            
            result.relevance_score += personalization_boost
            result.matched_fields.append("personalized")
        
        return results
    
    def _apply_business_logic(self, results: List[SearchResult]) -> List[SearchResult]:
        """Apply business logic like promotions and sponsored results"""
        for result in results:
            business_boost = 0.0
            
            # Promoted brand boost
            if 'Brand' in result.product_data:
                brand = result.product_data['Brand'].lower()
                if brand in self.business_rules['promoted_brands']:
                    business_boost += 0.15
            
            # Sponsored category boost
            if 'Type' in result.product_data:
                category = result.product_data['Type'].lower()
                if any(sponsored_cat in category for sponsored_cat in self.business_rules['sponsored_categories']):
                    business_boost += 0.1
            
            # Freshness boost
            if result.product_data.get('_shard_id', 0) > 5:  # Newer products
                business_boost += self.business_rules['freshness_boost']
            
            result.relevance_score += business_boost
            result.matched_fields.append("business_enhanced")
        
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
    
    def _ensure_diversity(self, results: List[SearchResult]) -> List[SearchResult]:
        """Ensure diversity in results (brand, category, price)"""
        if not self.diversity_factors['brand_diversity']:
            return results
        
        diverse_results = []
        seen_brands = set()
        seen_categories = set()
        
        for result in results:
            brand = result.product_data.get('Brand', '').lower()
            category = result.product_data.get('Type', '').lower()
            
            # Allow some diversity
            if len(seen_brands) < 5 or brand not in seen_brands:
                if len(seen_categories) < 3 or category not in seen_categories:
                    diverse_results.append(result)
                    seen_brands.add(brand)
                    seen_categories.add(category)
            
            if len(diverse_results) >= 15:
                break
        
        return diverse_results

class PowerStone:
    """
    Power Stone - Compute & Scalability
    Raw strength → computational muscle to handle huge queries.
    
    Search engine aspects:
    - Low latency (<200ms results)
    - Large-scale distributed indexing (Elasticsearch, Solr, Lucene)
    - High throughput (millions of queries/sec)
    - Caching, replication, fault tolerance
    - Without it → engine collapses under heavy load
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.performance_metrics = {
            'query_count': 0,
            'total_latency': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'throughput_qps': 0.0
        }
        self.distributed_cache = {}  # Simulate distributed caching
        self.load_balancer = {
            'active_shards': 10,
            'replica_count': 2,
            'fault_tolerance': True
        }
        self.performance_targets = {
            'max_latency_ms': 200,
            'target_qps': 1000,
            'cache_hit_ratio': 0.8
        }
    
    def search(self, query: str) -> List[SearchResult]:
        """Use computational power with performance optimization"""
        start_time = time.time()
        print("💜 Power Stone: Applying computational muscle and performance optimization...")
        
        # 1. Check distributed cache first
        cache_key = f"power_{hash(query)}"
        if cache_key in self.distributed_cache:
            self.performance_metrics['cache_hits'] += 1
            print("⚡ Power Stone: Cache hit - ultra-fast retrieval!")
            return self.distributed_cache[cache_key]
        
        self.performance_metrics['cache_misses'] += 1
        
        # 2. Distributed processing simulation
        results = self._distributed_search(query)
        
        # 3. Performance optimization
        optimized_results = self._optimize_performance(results, query)
        
        # 4. Cache the results
        self.distributed_cache[cache_key] = optimized_results
        
        # 5. Update performance metrics
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds
        self._update_performance_metrics(latency)
        
        print(f"🚀 Power Stone: Processed in {latency:.2f}ms, throughput: {self.performance_metrics['throughput_qps']:.1f} QPS")
        return optimized_results
    
    def _distributed_search(self, query: str) -> List[SearchResult]:
        """Simulate distributed search across multiple shards"""
        query_words = re.findall(r'\b\w+\b', query.lower())
        query_tf = Counter(query_words)
        
        # Simulate parallel processing across shards
        shard_results = []
        shards_per_query = min(3, self.load_balancer['active_shards'])  # Use 3 shards max
        
        for shard_id in range(shards_per_query):
            shard_products = self._get_shard_products(shard_id)
            shard_result = self._process_shard(shard_products, query_tf, query_words, shard_id)
            shard_results.extend(shard_result)
        
        return shard_results
    
    def _get_shard_products(self, shard_id: int) -> List[Dict]:
        """Get products from a specific shard"""
        # Simulate shard distribution
        total_products = len(self.engine.products)
        shard_size = total_products // self.load_balancer['active_shards']
        start_idx = shard_id * shard_size
        end_idx = start_idx + shard_size if shard_id < self.load_balancer['active_shards'] - 1 else total_products
        
        return self.engine.products[start_idx:end_idx]
    
    def _process_shard(self, products: List[Dict], query_tf: Counter, query_words: List[str], shard_id: int) -> List[SearchResult]:
        """Process a single shard with TF-IDF scoring"""
        results = []
        
        for product in products:
            score = self._calculate_optimized_tfidf_score(product, query_tf, query_words)
            if score > 0:
                result = SearchResult(
                    product_id=product.get('id', ''),
                    product_data=product,
                    relevance_score=score,
                    stone_powers={StoneType.POWER: score},
                    matched_fields=["power_optimized", f"shard_{shard_id}"]
                )
                # Add shard metadata
                result.product_data['_shard_id'] = shard_id
                result.product_data['_processing_time'] = time.time()
                results.append(result)
        
        return results
    
    def _calculate_optimized_tfidf_score(self, product: Dict, query_tf: Counter, query_words: List[str]) -> float:
        """Optimized TF-IDF calculation with caching"""
        score = 0.0
        product_text = ' '.join(str(v) for v in product.values() if isinstance(v, str)).lower()
        
        for word in query_words:
            if word in product_text:
                # Term frequency in product
                tf = product_text.count(word)
                # Inverse document frequency (cached)
                idf = self._get_cached_idf(word)
                score += tf * idf * query_tf[word]
        
        return score
    
    def _get_cached_idf(self, word: str) -> float:
        """Get cached IDF value for performance"""
        # In a real system, this would be pre-computed and cached
        if word in self.engine.index:
            return math.log(len(self.engine.products) / (1 + len(self.engine.index[word])))
        return 0.0
    
    def _optimize_performance(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """Apply performance optimizations"""
        # 1. Early termination for high-scoring results
        if len(results) > 2000:  # Increased limit for better pagination
            results = sorted(results, key=lambda x: x.relevance_score, reverse=True)[:2000]
        
        # 2. Parallel sorting simulation
        optimized_results = sorted(results, key=lambda x: x.relevance_score, reverse=True)
        
        # 3. Add performance metadata
        for result in optimized_results:
            result.product_data['_power_optimized'] = True
            result.product_data['_query_processed'] = query
        
        return optimized_results
    
    def _update_performance_metrics(self, latency: float):
        """Update performance metrics"""
        self.performance_metrics['query_count'] += 1
        self.performance_metrics['total_latency'] += latency
        
        # Calculate throughput (queries per second)
        if self.performance_metrics['query_count'] > 0:
            avg_latency = self.performance_metrics['total_latency'] / self.performance_metrics['query_count']
            self.performance_metrics['throughput_qps'] = 1000 / avg_latency if avg_latency > 0 else 0
        
        # Check performance targets
        if latency > self.performance_targets['max_latency_ms']:
            print(f"⚠️ Power Stone: Latency warning - {latency:.2f}ms exceeds target {self.performance_targets['max_latency_ms']}ms")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        cache_hit_ratio = 0.0
        total_cache_requests = self.performance_metrics['cache_hits'] + self.performance_metrics['cache_misses']
        if total_cache_requests > 0:
            cache_hit_ratio = self.performance_metrics['cache_hits'] / total_cache_requests
        
        avg_latency = 0.0
        if self.performance_metrics['query_count'] > 0:
            avg_latency = self.performance_metrics['total_latency'] / self.performance_metrics['query_count']
        
        return {
            'performance_metrics': self.performance_metrics,
            'performance_targets': self.performance_targets,
            'load_balancer': self.load_balancer,
            'performance_health': {
                'avg_latency_ms': avg_latency,
                'cache_hit_ratio': cache_hit_ratio,
                'throughput_qps': self.performance_metrics['throughput_qps'],
                'meets_latency_target': avg_latency <= self.performance_targets['max_latency_ms'],
                'meets_cache_target': cache_hit_ratio >= self.performance_targets['cache_hit_ratio']
            }
        }
    
    def combine_results(self, stone_results: Dict[StoneType, List[SearchResult]]) -> List[SearchResult]:
        """Combine results from all stones using weighted scoring"""
        combined_scores = defaultdict(lambda: {'score': 0.0, 'product': None, 'stone_powers': {}, 'matched_fields': set()})
        
        # Weight for each stone
        stone_weights = {
            StoneType.SPACE: 0.3,
            StoneType.MIND: 0.1,
            StoneType.REALITY: 0.2,
            StoneType.POWER: 0.3,
            StoneType.TIME: 0.05,
            StoneType.SOUL: 0.05
        }
        
        for stone_type, results in stone_results.items():
            weight = stone_weights.get(stone_type, 0.1)
            for result in results:
                product_id = result.product_id
                if product_id not in combined_scores:
                    combined_scores[product_id] = {
                        'score': 0.0,
                        'product': result.product_data,
                        'stone_powers': {},
                        'matched_fields': set()
                    }
                
                combined_scores[product_id]['score'] += result.relevance_score * weight
                combined_scores[product_id]['stone_powers'].update(result.stone_powers)
                combined_scores[product_id]['matched_fields'].update(result.matched_fields)
        
        # Convert to SearchResult objects with performance limit
        final_results = []
        for product_id, data in combined_scores.items():
            final_results.append(SearchResult(
                product_id=product_id,
                product_data=data['product'],
                relevance_score=data['score'],
                stone_powers=data['stone_powers'],
                matched_fields=list(data['matched_fields'])
            ))
        
        # Sort and limit results for performance
        sorted_results = sorted(final_results, key=lambda x: x.relevance_score, reverse=True)
        return sorted_results[:1000]  # Limit to top 1000 results for performance

class TimeStone:
    """
    Time Stone - Algorithm Selection
    Represents the power to optimize search performance and select efficient algorithms
    """
    
    def __init__(self, engine):
        self.engine = engine
    
    def search(self, query: str) -> List[SearchResult]:
        """Optimize search performance"""
        # Use cached results if available
        if ADVANCED_CACHING_AVAILABLE:
            cached_result = self.engine.search_cache.get(query)
            if cached_result is not None:
                return cached_result
        else:
            if query in self.engine.search_cache:
                return self.engine.search_cache[query]
        
        # Otherwise, use a fast approximate search
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        results = []
        
        for product in self.engine.products[:1000]:  # Limit for speed
            product_text = ' '.join(str(v) for v in product.values() if isinstance(v, str)).lower()
            product_words = set(re.findall(r'\b\w+\b', product_text))
            
            # Calculate Jaccard similarity
            intersection = len(query_words.intersection(product_words))
            union = len(query_words.union(product_words))
            
            if union > 0:
                similarity = intersection / union
                if similarity > 0.1:  # Threshold for relevance
                    results.append(SearchResult(
                        product_id=product.get('id', ''),
                        product_data=product,
                        relevance_score=similarity,
                        stone_powers={StoneType.TIME: similarity},
                        matched_fields=["time_optimized"]
                    ))
        
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)[:1000]  # Increased for better pagination

class SoulStone:
    """
    Soul Stone - Business Intelligence
    Represents the power to provide insights, analytics, and business intelligence
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.analytics_data = {
            'search_patterns': Counter(),
            'product_popularity': Counter(),
            'category_trends': Counter(),
            'user_behavior': []
        }
    
    def search(self, query: str) -> List[SearchResult]:
        """Provide business intelligence insights"""
        # Get base results
        base_results = self.engine.stones[StoneType.SPACE].search(query)
        
        # Add business intelligence scoring
        for result in base_results:
            business_score = self._calculate_business_score(result)
            result.stone_powers[StoneType.SOUL] = business_score
            result.matched_fields.append("soul_insight")
        
        return base_results
    
    def _calculate_business_score(self, result: SearchResult) -> float:
        """Calculate business intelligence score"""
        score = 0.0
        product = result.product_data
        
        # Prefer products with business-relevant information
        if 'Brand' in product and product['Brand']:
            score += 0.3
        if 'Type' in product and product['Type']:
            score += 0.2
        if 'Sales Package' in product and product['Sales Package']:
            score += 0.1
        
        return min(score, 1.0)
    
    def analyze_search(self, query: str, results: List[SearchResult]):
        """Analyze search patterns and results"""
        self.analytics_data['search_patterns'][query.lower()] += 1
        
        for result in results:
            product = result.product_data
            if 'Type' in product:
                self.analytics_data['category_trends'][product['Type']] += 1
            if 'Brand' in product:
                self.analytics_data['product_popularity'][product['Brand']] += 1
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get comprehensive analytics"""
        return {
            'total_products': len(self.engine.products),
            'search_analytics': self.engine.analytics,
            'business_insights': self.analytics_data,
            'stone_effectiveness': dict(self.engine.analytics['stone_usage'])
        }

def main():
    """Main function to demonstrate the Infinity Stones Search Engine"""
    print("🔮 Welcome to the Infinity Stones Search Engine! 🔮")
    print("Powered by the six Infinity Stones of the Marvel Cinematic Universe")
    print("=" * 60)
    
    # Initialize the search engine
    engine = InfinityStonesSearchEngine('data-set.json')
    
    # Interactive search loop
    while True:
        print("\nChoose your search approach:")
        print("1. 🔵 Space Stone - Explore data space")
        print("2. 🟡 Mind Stone - Visual presentation")
        print("3. 🔴 Reality Stone - Domain knowledge")
        print("4. 🟣 Power Stone - Computational power")
        print("5. 🟢 Time Stone - Optimized performance")
        print("6. 🟠 Soul Stone - Business intelligence")
        print("7. ✨ All Stones - Combined power")
        print("8. 📊 Analytics Dashboard")
        print("9. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '9':
            print("👋 Thank you for using the Infinity Stones Search Engine!")
            break
        elif choice == '8':
            analytics = engine.get_analytics()
            print("\n📊 Analytics Dashboard:")
            print(f"Total Products: {analytics['total_products']}")
            print(f"Total Searches: {analytics['search_analytics']['total_searches']}")
            print(f"Average Search Time: {sum(analytics['search_analytics']['search_times'])/len(analytics['search_analytics']['search_times']):.3f}s")
            print("\nMost Popular Queries:")
            for query, count in analytics['search_analytics']['popular_queries'].most_common(5):
                print(f"  - '{query}': {count} searches")
            continue
        
        query = input("\nEnter your search query: ").strip()
        if not query:
            continue
        
        # Map choice to stone type
        stone_mapping = {
            '1': StoneType.SPACE,
            '2': StoneType.MIND,
            '3': StoneType.REALITY,
            '4': StoneType.POWER,
            '5': StoneType.TIME,
            '6': StoneType.SOUL,
            '7': None
        }
        
        stone_preference = stone_mapping.get(choice)
        
        # Perform search
        results = engine.search(query, stone_preference)
        
        # Display results
        print(f"\n✨ Found {len(results)} results:")
        print("-" * 60)
        
        for i, result in enumerate(results[:10], 1):
            product = result.product_data
            print(f"\n{i}. Product ID: {result.product_id}")
            print(f"   Relevance Score: {result.relevance_score:.3f}")
            
            # Show key product information
            if 'Brand' in product and product['Brand']:
                print(f"   Brand: {product['Brand']}")
            if 'Type' in product and product['Type']:
                print(f"   Type: {product['Type']}")
            if 'Model Number' in product and product['Model Number']:
                print(f"   Model: {product['Model Number']}")
            
            # Show stone powers
            print(f"   Stone Powers: {', '.join([f'{stone.value}: {power:.2f}' for stone, power in result.stone_powers.items()])}")
            
            # Show matched fields
            print(f"   Matched: {', '.join(result.matched_fields[:3])}")

if __name__ == "__main__":
    main()
