"""
Comprehensive Test Suite for Infinity Stones Search Engine
Includes unit tests, integration tests, and performance benchmarks
"""

import unittest
import time
import tempfile
import json
import os
from unittest.mock import patch, MagicMock
from typing import List, Dict, Any

# Import modules to test
try:
    from infinity_search_engine import (
        InfinityStonesSearchEngine, StoneType, SearchResult,
        validate_query, safe_get_field, SearchError, ValidationError
    )
    from advanced_caching import LRUCache, MultiLevelCache, CacheWarmer
    from advanced_search_features import FuzzySearchEngine, BooleanSearchEngine, FacetedSearchEngine
    from enhanced_analytics import EnhancedAnalyticsEngine, SearchSession, QueryPerformance
except ImportError as e:
    print(f"Import error: {e}")
    print("Some advanced features may not be available for testing")

class TestValidationFunctions(unittest.TestCase):
    """Test input validation and utility functions"""
    
    def test_validate_query_valid_input(self):
        """Test query validation with valid inputs"""
        self.assertEqual(validate_query("bluetooth"), "bluetooth")
        self.assertEqual(validate_query("  wireless headphones  "), "wireless headphones")
        self.assertEqual(validate_query("car bluetooth adapter"), "car bluetooth adapter")
    
    def test_validate_query_invalid_input(self):
        """Test query validation with invalid inputs"""
        with self.assertRaises(ValidationError):
            validate_query("")
        with self.assertRaises(ValidationError):
            validate_query("   ")
        with self.assertRaises(ValidationError):
            validate_query(None)
        with self.assertRaises(ValidationError):
            validate_query(123)
    
    def test_validate_query_sanitization(self):
        """Test query sanitization"""
        result = validate_query('bluetooth "headphones"')
        self.assertNotIn('"', result)
        
        result = validate_query("bluetooth <script>")
        self.assertNotIn('<', result)
        self.assertNotIn('>', result)
    
    def test_validate_query_length_limit(self):
        """Test query length truncation"""
        long_query = "bluetooth " * 100  # Very long query
        result = validate_query(long_query)
        self.assertLessEqual(len(result), 500)
    
    def test_safe_get_field(self):
        """Test safe field retrieval"""
        data = {"Brand": "Samsung", "Type": "Phone", "Empty": "", "Null": None}
        
        self.assertEqual(safe_get_field(data, "Brand"), "Samsung")
        self.assertEqual(safe_get_field(data, "NonExistent", "default"), "default")
        self.assertEqual(safe_get_field(data, "Empty", "default"), "default")
        self.assertEqual(safe_get_field(data, "Null", "default"), "default")

class TestLRUCache(unittest.TestCase):
    """Test LRU cache implementation"""
    
    def setUp(self):
        """Set up test cache"""
        self.cache = LRUCache(max_size=3, ttl=1.0)
    
    def test_basic_operations(self):
        """Test basic cache operations"""
        # Test put and get
        self.cache.put("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")
        
        # Test miss
        self.assertIsNone(self.cache.get("nonexistent"))
    
    def test_capacity_limit(self):
        """Test cache capacity limiting"""
        # Fill cache beyond capacity
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        self.cache.put("key4", "value4")  # Should evict key1
        
        self.assertIsNone(self.cache.get("key1"))  # Evicted
        self.assertEqual(self.cache.get("key4"), "value4")  # New item
    
    def test_lru_behavior(self):
        """Test LRU eviction behavior"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        
        # Access key1 to make it recently used
        self.cache.get("key1")
        
        # Add new item, should evict key2 (least recently used)
        self.cache.put("key4", "value4")
        
        self.assertEqual(self.cache.get("key1"), "value1")  # Still there
        self.assertIsNone(self.cache.get("key2"))  # Evicted
        self.assertEqual(self.cache.get("key3"), "value3")  # Still there
    
    def test_ttl_expiration(self):
        """Test TTL-based expiration"""
        self.cache.put("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")
        
        # Wait for expiration
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("key1"))
    
    def test_cache_statistics(self):
        """Test cache statistics tracking"""
        self.cache.put("key1", "value1")
        self.cache.get("key1")  # Hit
        self.cache.get("key2")  # Miss
        
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 1)
        self.assertEqual(stats['hit_ratio'], 0.5)

class TestFuzzySearch(unittest.TestCase):
    """Test fuzzy search functionality"""
    
    def setUp(self):
        """Set up fuzzy search engine"""
        self.fuzzy_engine = FuzzySearchEngine(similarity_threshold=0.7)
    
    def test_fuzzy_matching(self):
        """Test fuzzy string matching"""
        corpus = ["bluetooth", "wireless", "headphones", "speakers"]
        
        # Test close match
        matches = self.fuzzy_engine.find_fuzzy_matches("bluetoth", corpus, max_results=3)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0].matched_term, "bluetooth")
        self.assertGreater(matches[0].similarity, 0.7)
    
    def test_similarity_calculations(self):
        """Test similarity calculation methods"""
        # Test Jaro similarity
        jaro_sim = self.fuzzy_engine._jaro_similarity("bluetooth", "bluetoth")
        self.assertGreater(jaro_sim, 0.8)
        
        # Test Levenshtein similarity
        lev_sim = self.fuzzy_engine._levenshtein_similarity("bluetooth", "bluetoth")
        self.assertGreater(lev_sim, 0.8)
    
    def test_threshold_filtering(self):
        """Test similarity threshold filtering"""
        corpus = ["bluetooth", "car", "house"]
        
        # Very different word should not match
        matches = self.fuzzy_engine.find_fuzzy_matches("bluetoth", corpus)
        
        # Should only match bluetooth, not car or house
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].matched_term, "bluetooth")

class TestBooleanSearch(unittest.TestCase):
    """Test boolean search functionality"""
    
    def setUp(self):
        """Set up boolean search engine"""
        self.boolean_engine = BooleanSearchEngine()
    
    def test_simple_boolean_queries(self):
        """Test simple boolean query parsing"""
        # Test AND
        parsed = self.boolean_engine.parse_boolean_query("bluetooth AND wireless")
        self.assertTrue(parsed['success'])
        self.assertEqual(parsed['expression']['type'], 'and')
        
        # Test OR
        parsed = self.boolean_engine.parse_boolean_query("phone OR tablet")
        self.assertTrue(parsed['success'])
        self.assertEqual(parsed['expression']['type'], 'or')
        
        # Test NOT
        parsed = self.boolean_engine.parse_boolean_query("NOT expensive")
        self.assertTrue(parsed['success'])
        self.assertEqual(parsed['expression']['type'], 'not')
    
    def test_complex_boolean_queries(self):
        """Test complex boolean queries with parentheses"""
        query = "bluetooth AND (headphone OR speaker)"
        parsed = self.boolean_engine.parse_boolean_query(query)
        
        self.assertTrue(parsed['success'])
        self.assertEqual(parsed['expression']['type'], 'and')
        self.assertEqual(parsed['expression']['right']['type'], 'or')
    
    def test_boolean_evaluation(self):
        """Test boolean expression evaluation"""
        # Create test product matches
        product_matches = {
            'bluetooth': {'product1', 'product2'},
            'wireless': {'product2', 'product3'},
            'expensive': {'product1'}
        }
        
        # Test AND operation
        and_expr = {'type': 'and', 'left': {'type': 'term', 'value': 'bluetooth'}, 
                   'right': {'type': 'term', 'value': 'wireless'}}
        result = self.boolean_engine.evaluate_boolean_expression(and_expr, product_matches)
        self.assertEqual(result, {'product2'})  # Only product2 has both
        
        # Test OR operation
        or_expr = {'type': 'or', 'left': {'type': 'term', 'value': 'bluetooth'}, 
                  'right': {'type': 'term', 'value': 'wireless'}}
        result = self.boolean_engine.evaluate_boolean_expression(or_expr, product_matches)
        self.assertEqual(result, {'product1', 'product2', 'product3'})

class TestFacetedSearch(unittest.TestCase):
    """Test faceted search functionality"""
    
    def setUp(self):
        """Set up test products for faceted search"""
        self.test_products = [
            {"id": "1", "Brand": "Samsung", "Type": "Phone", "Sales Package": "Advanced smartphone with 128GB storage"},
            {"id": "2", "Brand": "Apple", "Type": "Phone", "Sales Package": "Premium iPhone with camera"},
            {"id": "3", "Brand": "Sony", "Type": "Headphone", "Sales Package": "Wireless bluetooth headphones"},
            {"id": "4", "Brand": "Samsung", "Type": "TV", "Sales Package": "55 inch smart TV"},
        ]
        self.faceted_engine = FacetedSearchEngine(self.test_products)
    
    def test_facet_building(self):
        """Test facet index building"""
        facets = self.faceted_engine.get_facets()
        
        # Check brand facets
        self.assertIn('Samsung', facets['brand'])
        self.assertIn('Apple', facets['brand'])
        self.assertEqual(facets['brand']['Samsung'], 2)  # 2 Samsung products
        
        # Check category inference
        self.assertIn('Mobile & Tablets', facets['category'])
        self.assertIn('Audio', facets['category'])
    
    def test_facet_filtering(self):
        """Test filtering by facets"""
        all_product_ids = {'1', '2', '3', '4'}
        
        # Filter by brand
        samsung_filter = {'brand': ['Samsung']}
        filtered = self.faceted_engine.filter_by_facets(all_product_ids, samsung_filter)
        self.assertEqual(filtered, {'1', '4'})  # Samsung products
        
        # Filter by category
        mobile_filter = {'category': ['Mobile & Tablets']}
        filtered = self.faceted_engine.filter_by_facets(all_product_ids, mobile_filter)
        self.assertEqual(len(filtered), 2)  # Phone products
    
    def test_multiple_facet_filtering(self):
        """Test filtering with multiple facets"""
        all_product_ids = {'1', '2', '3', '4'}
        
        # Filter by brand AND category
        filters = {'brand': ['Samsung'], 'category': ['Mobile & Tablets']}
        filtered = self.faceted_engine.filter_by_facets(all_product_ids, filters)
        self.assertEqual(filtered, {'1'})  # Only Samsung phone

class TestSearchEngine(unittest.TestCase):
    """Test main search engine functionality"""
    
    def setUp(self):
        """Set up test search engine with sample data"""
        # Create temporary test data file
        self.test_data = [
            {"id": "1", "Name": "Bluetooth Speaker", "Brand": "JBL", "Type": "Speaker", 
             "Sales Package": "Portable wireless bluetooth speaker with bass"},
            {"id": "2", "Name": "Wireless Headphones", "Brand": "Sony", "Type": "Headphone", 
             "Sales Package": "Premium over-ear wireless headphones"},
            {"id": "3", "Name": "Car Adapter", "Brand": "Samsung", "Type": "Car Accessory", 
             "Sales Package": "Bluetooth car adapter for music streaming"},
        ]
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        
        # Initialize search engine
        self.engine = InfinityStonesSearchEngine(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary files"""
        os.unlink(self.temp_file.name)
    
    def test_data_loading(self):
        """Test data loading and initialization"""
        self.assertEqual(len(self.engine.products), 3)
        self.assertGreater(len(self.engine.index), 0)
    
    def test_basic_search(self):
        """Test basic search functionality"""
        results = self.engine.search("bluetooth")
        self.assertGreater(len(results), 0)
        
        # Check result structure
        result = results[0]
        self.assertIsInstance(result, SearchResult)
        self.assertIn('id', result.product_data)
        self.assertGreater(result.relevance_score, 0)
    
    def test_stone_specific_search(self):
        """Test searching with specific stones"""
        # Test Space Stone
        space_results = self.engine.search("bluetooth", stone_preference=StoneType.SPACE)
        self.assertGreater(len(space_results), 0)
        
        # Test Mind Stone
        mind_results = self.engine.search("bluetooth", stone_preference=StoneType.MIND)
        self.assertGreater(len(mind_results), 0)
        
        # Test Power Stone
        power_results = self.engine.search("bluetooth", stone_preference=StoneType.POWER)
        self.assertGreater(len(power_results), 0)
    
    def test_empty_query_handling(self):
        """Test handling of empty or invalid queries"""
        empty_results = self.engine.search("")
        self.assertEqual(len(empty_results), 0)
        
        whitespace_results = self.engine.search("   ")
        self.assertEqual(len(whitespace_results), 0)
    
    def test_no_results_query(self):
        """Test queries that return no results"""
        no_results = self.engine.search("nonexistentproduct12345")
        self.assertEqual(len(no_results), 0)
    
    def test_search_caching(self):
        """Test search result caching"""
        query = "bluetooth speaker"
        
        # First search
        start_time = time.time()
        results1 = self.engine.search(query)
        first_search_time = time.time() - start_time
        
        # Second search (should be cached)
        start_time = time.time()
        results2 = self.engine.search(query)
        second_search_time = time.time() - start_time
        
        # Results should be identical
        self.assertEqual(len(results1), len(results2))
        
        # Second search should be faster (cached)
        self.assertLess(second_search_time, first_search_time)
    
    def test_analytics_tracking(self):
        """Test analytics data collection"""
        initial_analytics = self.engine.get_analytics()
        initial_searches = initial_analytics['search_analytics']['total_searches']
        
        # Perform a search
        self.engine.search("bluetooth")
        
        # Check analytics updated
        updated_analytics = self.engine.get_analytics()
        updated_searches = updated_analytics['search_analytics']['total_searches']
        
        self.assertEqual(updated_searches, initial_searches + 1)

class TestEnhancedAnalytics(unittest.TestCase):
    """Test enhanced analytics functionality"""
    
    def setUp(self):
        """Set up analytics engine"""
        self.analytics = EnhancedAnalyticsEngine(export_path=tempfile.mkdtemp())
    
    def test_session_tracking(self):
        """Test user session tracking"""
        session_id = "test_session_1"
        
        # Start session
        session = self.analytics.start_search_session(session_id)
        self.assertIsNotNone(session)
        self.assertIn(session_id, self.analytics.active_sessions)
        
        # Track actions
        self.analytics.track_user_action(session_id, 'search', {'query': 'bluetooth'})
        
        # End session
        self.analytics.end_search_session(session_id)
        self.assertNotIn(session_id, self.analytics.active_sessions)
        self.assertEqual(len(self.analytics.completed_sessions), 1)
    
    def test_performance_tracking(self):
        """Test query performance tracking"""
        initial_count = len(self.analytics.query_performance_history)
        
        self.analytics.track_query_performance(
            query="bluetooth",
            total_time=0.5,
            stone_times={"Space": 0.1, "Mind": 0.2},
            cache_hit=False,
            results_count=10,
            relevance_scores=[0.9, 0.8, 0.7]
        )
        
        self.assertEqual(len(self.analytics.query_performance_history), initial_count + 1)
    
    def test_real_time_metrics(self):
        """Test real-time metrics calculation"""
        # Add some test data
        self.analytics.track_query_performance(
            query="test",
            total_time=0.3,
            stone_times={"Space": 0.1},
            cache_hit=True,
            results_count=5,
            relevance_scores=[0.8]
        )
        
        metrics = self.analytics.get_real_time_metrics()
        self.assertIn('status', metrics)
        self.assertIn('timestamp', metrics)

class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests"""
    
    def setUp(self):
        """Set up performance test data"""
        # Create larger test dataset
        self.large_test_data = []
        for i in range(1000):  # 1000 products
            self.large_test_data.append({
                "id": str(i),
                "Name": f"Product {i}",
                "Brand": f"Brand{i % 10}",
                "Type": f"Type{i % 5}",
                "Sales Package": f"Description for product {i} with features and specifications"
            })
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.large_test_data, self.temp_file)
        self.temp_file.close()
        
        self.engine = InfinityStonesSearchEngine(self.temp_file.name)
    
    def tearDown(self):
        """Clean up"""
        os.unlink(self.temp_file.name)
    
    def test_search_performance(self):
        """Test search performance with larger dataset"""
        queries = ["Product", "Brand1", "Type2", "Description", "features"]
        
        total_time = 0
        for query in queries:
            start_time = time.time()
            results = self.engine.search(query)
            search_time = time.time() - start_time
            total_time += search_time
            
            # Performance assertions
            self.assertLess(search_time, 2.0)  # Should complete within 2 seconds
            self.assertGreater(len(results), 0)  # Should find results
        
        avg_time = total_time / len(queries)
        self.assertLess(avg_time, 1.0)  # Average should be under 1 second
        
        print(f"Average search time: {avg_time:.3f} seconds")
    
    def test_indexing_performance(self):
        """Test indexing performance"""
        start_time = time.time()
        
        # Re-initialize to test indexing time
        test_engine = InfinityStonesSearchEngine(self.temp_file.name)
        
        indexing_time = time.time() - start_time
        
        # Indexing should complete reasonably quickly
        self.assertLess(indexing_time, 10.0)  # Should index within 10 seconds
        self.assertGreater(len(test_engine.index), 0)
        
        print(f"Indexing time for 1000 products: {indexing_time:.3f} seconds")
    
    def test_memory_usage_estimation(self):
        """Test memory usage remains reasonable"""
        # This is a rough estimation test
        index_size = len(self.engine.index)
        product_count = len(self.engine.products)
        
        # Basic sanity checks
        self.assertGreater(index_size, 0)
        self.assertEqual(product_count, 1000)
        
        # Index should not be excessively large compared to product count
        self.assertLess(index_size, product_count * 100)  # Reasonable upper bound
        
        print(f"Index size: {index_size} terms for {product_count} products")

def run_all_tests():
    """Run all test suites"""
    print("🔮 Running Infinity Stones Search Engine Test Suite 🔮")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestValidationFunctions,
        TestLRUCache,
        TestFuzzySearch,
        TestBooleanSearch,
        TestFacetedSearch,
        TestSearchEngine,
        TestEnhancedAnalytics,
        TestPerformanceBenchmarks
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"🎯 Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("\n✅ All tests passed! The Infinity Stones are working perfectly! ✨")
    
    return result

if __name__ == "__main__":
    run_all_tests()
