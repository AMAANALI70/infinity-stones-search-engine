"""
Advanced Caching System for Infinity Stones Search Engine
Implements LRU (Least Recently Used) caching and performance optimization
"""

import time
import threading
from typing import Dict, Any, Optional, Tuple, List
from collections import OrderedDict
import json
import logging

logger = logging.getLogger(__name__)

class LRUCache:
    """
    Thread-safe LRU (Least Recently Used) Cache implementation
    """
    
    def __init__(self, max_size: int = 1000, ttl: float = 3600):
        """
        Initialize LRU cache
        
        Args:
            max_size: Maximum number of items to store
            ttl: Time to live in seconds (default: 1 hour)
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict = OrderedDict()
        self.access_times: Dict[str, float] = {}
        self.lock = threading.RLock()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        with self.lock:
            if key in self.cache:
                # Check if expired
                if time.time() - self.access_times[key] > self.ttl:
                    self._remove(key)
                    self.misses += 1
                    return None
                
                # Move to end (most recently used)
                value = self.cache.pop(key)
                self.cache[key] = value
                self.access_times[key] = time.time()
                self.hits += 1
                return value
            else:
                self.misses += 1
                return None
    
    def put(self, key: str, value: Any):
        """Put item in cache"""
        with self.lock:
            current_time = time.time()
            
            if key in self.cache:
                # Update existing item
                self.cache.pop(key)
                self.cache[key] = value
                self.access_times[key] = current_time
            else:
                # Add new item
                if len(self.cache) >= self.max_size:
                    # Remove least recently used item
                    oldest_key = next(iter(self.cache))
                    self._remove(oldest_key)
                    self.evictions += 1
                
                self.cache[key] = value
                self.access_times[key] = current_time
    
    def _remove(self, key: str):
        """Remove item from cache"""
        if key in self.cache:
            del self.cache[key]
            del self.access_times[key]
    
    def clear(self):
        """Clear all cache"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self.cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_ratio = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_ratio': hit_ratio,
            'evictions': self.evictions,
            'ttl': self.ttl
        }
    
    def cleanup_expired(self):
        """Remove expired items"""
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, access_time in self.access_times.items()
                if current_time - access_time > self.ttl
            ]
            
            for key in expired_keys:
                self._remove(key)
            
            return len(expired_keys)

class MultiLevelCache:
    """
    Multi-level cache system for different types of data
    """
    
    def __init__(self):
        self.query_cache = LRUCache(max_size=500, ttl=1800)  # 30 minutes for queries
        self.index_cache = LRUCache(max_size=1000, ttl=7200)  # 2 hours for index data
        self.analytics_cache = LRUCache(max_size=100, ttl=300)  # 5 minutes for analytics
        
    def get_query_cache(self) -> LRUCache:
        """Get query-specific cache"""
        return self.query_cache
    
    def get_index_cache(self) -> LRUCache:
        """Get index-specific cache"""
        return self.index_cache
    
    def get_analytics_cache(self) -> LRUCache:
        """Get analytics-specific cache"""
        return self.analytics_cache
    
    def clear_all(self):
        """Clear all caches"""
        self.query_cache.clear()
        self.index_cache.clear()
        self.analytics_cache.clear()
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get statistics for all cache levels"""
        return {
            'query_cache': self.query_cache.get_stats(),
            'index_cache': self.index_cache.get_stats(),
            'analytics_cache': self.analytics_cache.get_stats(),
            'total_memory_items': (
                self.query_cache.size() + 
                self.index_cache.size() + 
                self.analytics_cache.size()
            )
        }
    
    def cleanup_expired_all(self) -> Dict[str, int]:
        """Cleanup expired items from all caches"""
        return {
            'query_cache_expired': self.query_cache.cleanup_expired(),
            'index_cache_expired': self.index_cache.cleanup_expired(),
            'analytics_cache_expired': self.analytics_cache.cleanup_expired()
        }

class CacheWarmer:
    """
    Cache warming system to pre-populate frequently used data
    """
    
    def __init__(self, cache_system: MultiLevelCache):
        self.cache_system = cache_system
        self.popular_queries = [
            "bluetooth", "wireless", "headphone", "speaker", "charger",
            "case", "camera", "phone", "laptop", "car", "vacuum",
            "beauty", "cream", "home", "furniture", "sports"
        ]
    
    def warm_query_cache(self, search_engine):
        """Pre-populate query cache with popular searches"""
        logger.info("Warming up query cache with popular searches...")
        
        warmed_count = 0
        for query in self.popular_queries:
            try:
                # This would normally trigger actual searches
                # For now, we'll just mark the intent
                cache_key = f"warm_{query}_all"
                self.cache_system.query_cache.put(cache_key, {"warmed": True, "query": query})
                warmed_count += 1
            except Exception as e:
                logger.error(f"Error warming cache for query '{query}': {e}")
        
        logger.info(f"Cache warming completed. Warmed {warmed_count} queries.")
        return warmed_count
    
    def warm_index_cache(self, search_engine):
        """Pre-populate index cache with common data"""
        logger.info("Warming up index cache...")
        
        try:
            # Cache frequently accessed index statistics
            if hasattr(search_engine, 'index_statistics'):
                self.cache_system.index_cache.put("index_stats", search_engine.index_statistics)
            
            # Cache brand and category indexes
            if hasattr(search_engine, 'brand_index'):
                popular_brands = list(search_engine.brand_index.keys())[:50]  # Top 50 brands
                self.cache_system.index_cache.put("popular_brands", popular_brands)
            
            if hasattr(search_engine, 'category_index'):
                popular_categories = list(search_engine.category_index.keys())[:20]  # Top 20 categories
                self.cache_system.index_cache.put("popular_categories", popular_categories)
            
            logger.info("Index cache warming completed")
            return True
            
        except Exception as e:
            logger.error(f"Error warming index cache: {e}")
            return False

class PerformanceMonitor:
    """
    Monitor cache performance and system metrics
    """
    
    def __init__(self, cache_system: MultiLevelCache):
        self.cache_system = cache_system
        self.start_time = time.time()
        self.performance_history = []
    
    def record_performance_snapshot(self):
        """Record current performance metrics"""
        snapshot = {
            'timestamp': time.time(),
            'uptime': time.time() - self.start_time,
            'cache_stats': self.cache_system.get_comprehensive_stats(),
            'system_memory_estimate': self._estimate_memory_usage()
        }
        
        self.performance_history.append(snapshot)
        
        # Keep only last 100 snapshots
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
        
        return snapshot
    
    def _estimate_memory_usage(self) -> int:
        """Estimate memory usage in bytes"""
        # Rough estimation based on cache sizes
        query_cache_size = self.cache_system.query_cache.size() * 1024  # ~1KB per query result
        index_cache_size = self.cache_system.index_cache.size() * 512   # ~512B per index item
        analytics_cache_size = self.cache_system.analytics_cache.size() * 256  # ~256B per analytics item
        
        return query_cache_size + index_cache_size + analytics_cache_size
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        if not self.performance_history:
            return {"error": "No performance data available"}
        
        latest = self.performance_history[-1]
        
        # Calculate trends if we have enough data
        trends = {}
        if len(self.performance_history) >= 2:
            previous = self.performance_history[-2]
            trends = {
                'hit_ratio_trend': latest['cache_stats']['query_cache']['hit_ratio'] - 
                                 previous['cache_stats']['query_cache']['hit_ratio'],
                'memory_trend': latest['system_memory_estimate'] - previous['system_memory_estimate']
            }
        
        return {
            'current_performance': latest,
            'trends': trends,
            'history_length': len(self.performance_history),
            'recommendations': self._generate_recommendations(latest)
        }
    
    def _generate_recommendations(self, current_snapshot: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        query_stats = current_snapshot['cache_stats']['query_cache']
        
        if query_stats['hit_ratio'] < 0.5:
            recommendations.append("Consider increasing query cache size or TTL - low hit ratio detected")
        
        if query_stats['size'] >= query_stats['max_size'] * 0.9:
            recommendations.append("Query cache is near capacity - consider increasing max_size")
        
        if current_snapshot['system_memory_estimate'] > 50 * 1024 * 1024:  # 50MB
            recommendations.append("High memory usage detected - consider implementing cache cleanup")
        
        return recommendations

# Singleton instances for global use
global_cache_system = MultiLevelCache()
global_performance_monitor = PerformanceMonitor(global_cache_system)
global_cache_warmer = CacheWarmer(global_cache_system)
