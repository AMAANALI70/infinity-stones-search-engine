"""
Infinity Stones Search Engine - Demonstration Script
This script demonstrates the capabilities of the search engine with various test queries
"""

from infinity_search_engine import InfinityStonesSearchEngine, StoneType
import time

def demonstrate_search_engine():
    """Demonstrate the Infinity Stones Search Engine with various test cases"""
    
    print("🔮 INFINITY STONES SEARCH ENGINE DEMONSTRATION 🔮")
    print("=" * 60)
    print("Demonstrating the power of each Infinity Stone...")
    print()
    
    # Initialize the search engine
    print("Initializing the cosmic search engine...")
    engine = InfinityStonesSearchEngine('data-set.json')
    print("✨ Search engine ready!")
    print()
    
    # Test queries for different scenarios
    test_queries = [
        ("bluetooth speaker", "Electronics search"),
        ("car vacuum", "Automotive search"),
        ("beauty cream", "Beauty products search"),
        ("home furniture", "Home goods search"),
        ("sports equipment", "Sports search"),
        ("wireless headphones", "Tech accessories search")
    ]
    
    # Demonstrate each stone individually
    stones_to_demo = [
        (StoneType.SPACE, "🔵 Space Stone - Data Exploration"),
        (StoneType.MIND, "🟡 Mind Stone - Visualization"),
        (StoneType.REALITY, "🔴 Reality Stone - Domain Knowledge"),
        (StoneType.POWER, "🟣 Power Stone - Computational Power"),
        (StoneType.TIME, "🟢 Time Stone - Performance Optimization"),
        (StoneType.SOUL, "🟠 Soul Stone - Business Intelligence")
    ]
    
    for stone_type, stone_name in stones_to_demo:
        print(f"\n{stone_name}")
        print("-" * 50)
        
        # Test with a sample query
        query = "bluetooth"
        print(f"Searching for: '{query}' using {stone_name}")
        
        start_time = time.time()
        results = engine.search(query, stone_preference=stone_type)
        search_time = time.time() - start_time
        
        print(f"Found {len(results)} results in {search_time:.3f} seconds")
        
        # Show top 3 results
        for i, result in enumerate(results[:3], 1):
            product = result.product_data
            print(f"\n  {i}. Product ID: {result.product_id}")
            print(f"     Relevance: {result.relevance_score:.3f}")
            
            # Show key information
            if 'Brand' in product and product['Brand']:
                print(f"     Brand: {product['Brand']}")
            if 'Type' in product and product['Type']:
                print(f"     Type: {product['Type']}")
            
            # Show stone power
            stone_power = result.stone_powers.get(stone_type, 0)
            print(f"     {stone_name} Power: {stone_power:.3f}")
    
    # Demonstrate combined search
    print(f"\n✨ ALL STONES COMBINED - ULTIMATE POWER ✨")
    print("-" * 50)
    
    query = "wireless bluetooth"
    print(f"Searching for: '{query}' using ALL INFINITY STONES")
    
    start_time = time.time()
    results = engine.search(query)  # No stone preference = all stones
    search_time = time.time() - start_time
    
    print(f"Found {len(results)} results in {search_time:.3f} seconds")
    print("\nTop 5 Results:")
    
    for i, result in enumerate(results[:5], 1):
        product = result.product_data
        print(f"\n  {i}. Product ID: {result.product_id}")
        print(f"     Combined Relevance: {result.relevance_score:.3f}")
        
        if 'Brand' in product and product['Brand']:
            print(f"     Brand: {product['Brand']}")
        if 'Type' in product and product['Type']:
            print(f"     Type: {product['Type']}")
        if 'Model Number' in product and product['Model Number']:
            print(f"     Model: {product['Model Number']}")
        
        # Show all stone powers
        print(f"     Stone Powers:")
        for stone, power in result.stone_powers.items():
            print(f"       {stone.value}: {power:.3f}")
    
    # Show analytics
    print(f"\n📊 ANALYTICS DASHBOARD 📊")
    print("-" * 50)
    
    analytics = engine.get_analytics()
    print(f"Total Products in Database: {analytics['total_products']}")
    print(f"Total Searches Performed: {analytics['search_analytics']['total_searches']}")
    
    if analytics['search_analytics']['search_times']:
        avg_time = sum(analytics['search_analytics']['search_times']) / len(analytics['search_analytics']['search_times'])
        print(f"Average Search Time: {avg_time:.3f} seconds")
    
    print(f"\nStone Usage Statistics:")
    for stone, count in analytics['search_analytics']['stone_usage'].items():
        print(f"  {stone.value}: {count} uses")
    
    print(f"\nMost Popular Search Queries:")
    for query, count in analytics['search_analytics']['popular_queries'].most_common(3):
        print(f"  '{query}': {count} searches")
    
    print(f"\n🎯 DEMONSTRATION COMPLETE! 🎯")
    print("The Infinity Stones Search Engine successfully demonstrates:")
    print("• Data exploration and indexing (Space Stone)")
    print("• User-friendly result presentation (Mind Stone)")
    print("• Domain-specific product categorization (Reality Stone)")
    print("• Advanced search algorithms and ranking (Power Stone)")
    print("• Performance optimization and caching (Time Stone)")
    print("• Business intelligence and analytics (Soul Stone)")
    print("• Combined power of all stones working together")

def run_performance_test():
    """Run performance tests on the search engine"""
    print("\n🚀 PERFORMANCE TESTING 🚀")
    print("=" * 40)
    
    engine = InfinityStonesSearchEngine('data-set.json')
    
    test_queries = [
        "bluetooth",
        "car",
        "home",
        "beauty",
        "sports",
        "electronic",
        "wireless",
        "vacuum",
        "speaker",
        "headphone"
    ]
    
    print("Testing search performance with 10 different queries...")
    
    total_time = 0
    for i, query in enumerate(test_queries, 1):
        start_time = time.time()
        results = engine.search(query)
        search_time = time.time() - start_time
        total_time += search_time
        
        print(f"  {i:2d}. '{query}': {len(results)} results in {search_time:.3f}s")
    
    avg_time = total_time / len(test_queries)
    print(f"\nAverage search time: {avg_time:.3f} seconds")
    print(f"Total test time: {total_time:.3f} seconds")
    
    # Test caching performance
    print(f"\nTesting Time Stone caching...")
    start_time = time.time()
    for query in test_queries:
        engine.search(query)  # Should use cache
    cached_time = time.time() - start_time
    print(f"Cached searches completed in: {cached_time:.3f} seconds")
    print(f"Cache speedup: {total_time/cached_time:.1f}x faster")

if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_search_engine()
    
    # Run performance tests
    run_performance_test()
    
    print(f"\n🔮 Thank you for exploring the Infinity Stones Search Engine! 🔮")
    print("May the power of the stones guide your search endeavors!")
