"""
Simple test script for the Infinity Stones Search Engine
"""

from infinity_search_engine import InfinityStonesSearchEngine, StoneType

def test_basic_functionality():
    """Test basic search functionality"""
    print("🧪 Testing Infinity Stones Search Engine...")
    
    try:
        # Initialize engine
        engine = InfinityStonesSearchEngine('data-set.json')
        print("✅ Engine initialized successfully")
        
        # Test basic search
        results = engine.search("bluetooth")
        print(f"✅ Basic search returned {len(results)} results")
        
        # Test stone-specific search
        space_results = engine.search("car", stone_preference=StoneType.SPACE)
        print(f"✅ Space Stone search returned {len(space_results)} results")
        
        # Test analytics
        analytics = engine.get_analytics()
        print(f"✅ Analytics retrieved: {analytics['total_products']} products")
        
        print("🎉 All tests passed! The Infinity Stones are working perfectly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_basic_functionality()
