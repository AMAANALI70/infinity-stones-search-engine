"""
Enhanced Analytics Dashboard for Infinity Stones Search Engine
Provides detailed performance profiling, user behavior tracking, and exportable reports
"""

import json
import time
import os
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import logging
import csv
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)

@dataclass
class SearchSession:
    """Represents a user search session"""
    session_id: str
    start_time: float
    end_time: Optional[float] = None
    queries: List[str] = None
    results_viewed: List[str] = None
    stones_used: List[str] = None
    total_searches: int = 0
    
    def __post_init__(self):
        if self.queries is None:
            self.queries = []
        if self.results_viewed is None:
            self.results_viewed = []
        if self.stones_used is None:
            self.stones_used = []

@dataclass
class QueryPerformance:
    """Detailed performance metrics for a query"""
    query: str
    timestamp: float
    total_time: float
    stone_times: Dict[str, float]
    cache_hit: bool
    results_count: int
    relevance_scores: List[float]
    error_count: int = 0

@dataclass
class UserBehaviorMetrics:
    """User behavior analytics"""
    query_patterns: Dict[str, int]
    search_frequency: Dict[str, int]  # Time-based frequency
    stone_preferences: Dict[str, int]
    session_duration_avg: float
    bounce_rate: float  # Searches with no follow-up
    refinement_rate: float  # Queries that were refined

class EnhancedAnalyticsEngine:
    """
    Advanced analytics engine with comprehensive tracking and reporting
    """
    
    def __init__(self, export_path: str = "analytics_exports"):
        self.export_path = export_path
        self.ensure_export_directory()
        
        # Performance tracking
        self.query_performance_history: List[QueryPerformance] = []
        self.system_performance_snapshots: List[Dict[str, Any]] = []
        
        # User behavior tracking
        self.active_sessions: Dict[str, SearchSession] = {}
        self.completed_sessions: List[SearchSession] = []
        
        # Advanced metrics
        self.stone_effectiveness_metrics = defaultdict(list)
        self.query_complexity_metrics = {}
        self.error_analytics = defaultdict(list)
        
        # Performance baselines
        self.performance_baselines = {
            'avg_response_time': 1.0,  # seconds
            'cache_hit_ratio': 0.7,
            'error_rate': 0.01
        }
    
    def ensure_export_directory(self):
        """Ensure export directory exists"""
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
    
    def start_search_session(self, session_id: str) -> SearchSession:
        """Start tracking a new search session"""
        session = SearchSession(
            session_id=session_id,
            start_time=time.time()
        )
        self.active_sessions[session_id] = session
        logger.info(f"Started tracking session: {session_id}")
        return session
    
    def end_search_session(self, session_id: str):
        """End a search session and move to completed sessions"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.end_time = time.time()
            self.completed_sessions.append(session)
            del self.active_sessions[session_id]
            logger.info(f"Completed session: {session_id} (duration: {session.end_time - session.start_time:.2f}s)")
    
    def track_query_performance(self, query: str, total_time: float, stone_times: Dict[str, float], 
                              cache_hit: bool, results_count: int, relevance_scores: List[float], 
                              error_count: int = 0):
        """Track detailed performance metrics for a query"""
        performance = QueryPerformance(
            query=query,
            timestamp=time.time(),
            total_time=total_time,
            stone_times=stone_times,
            cache_hit=cache_hit,
            results_count=results_count,
            relevance_scores=relevance_scores,
            error_count=error_count
        )
        
        self.query_performance_history.append(performance)
        
        # Keep only last 1000 queries for memory efficiency
        if len(self.query_performance_history) > 1000:
            self.query_performance_history = self.query_performance_history[-1000:]
        
        # Update stone effectiveness metrics
        for stone, duration in stone_times.items():
            self.stone_effectiveness_metrics[stone].append({
                'duration': duration,
                'results_count': results_count,
                'avg_relevance': statistics.mean(relevance_scores) if relevance_scores else 0.0,
                'timestamp': time.time()
            })
    
    def track_user_action(self, session_id: str, action: str, details: Dict[str, Any]):
        """Track user actions within a session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            
            if action == 'search':
                session.queries.append(details.get('query', ''))
                session.stones_used.append(details.get('stone_used', 'all'))
                session.total_searches += 1
            elif action == 'view_result':
                session.results_viewed.append(details.get('product_id', ''))
    
    def record_system_snapshot(self, snapshot_data: Dict[str, Any]):
        """Record system performance snapshot"""
        snapshot_data['timestamp'] = time.time()
        self.system_performance_snapshots.append(snapshot_data)
        
        # Keep only last 100 snapshots
        if len(self.system_performance_snapshots) > 100:
            self.system_performance_snapshots = self.system_performance_snapshots[-100:]
    
    def get_performance_report(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        cutoff_time = time.time() - (time_range_hours * 3600)
        
        # Filter recent data
        recent_queries = [q for q in self.query_performance_history if q.timestamp > cutoff_time]
        recent_sessions = [s for s in self.completed_sessions if s.start_time > cutoff_time]
        recent_snapshots = [s for s in self.system_performance_snapshots if s['timestamp'] > cutoff_time]
        
        if not recent_queries:
            return {'error': 'No recent data available'}
        
        # Calculate performance metrics
        total_queries = len(recent_queries)
        avg_response_time = statistics.mean([q.total_time for q in recent_queries])
        cache_hit_ratio = sum(1 for q in recent_queries if q.cache_hit) / total_queries
        error_rate = sum(q.error_count for q in recent_queries) / total_queries
        avg_results_count = statistics.mean([q.results_count for q in recent_queries])
        
        # Stone performance analysis
        stone_performance = {}
        for query in recent_queries:
            for stone, duration in query.stone_times.items():
                if stone not in stone_performance:
                    stone_performance[stone] = {'durations': [], 'effectiveness': []}
                stone_performance[stone]['durations'].append(duration)
                stone_performance[stone]['effectiveness'].append(
                    statistics.mean(query.relevance_scores) if query.relevance_scores else 0.0
                )
        
        stone_stats = {}
        for stone, data in stone_performance.items():
            stone_stats[stone] = {
                'avg_duration': statistics.mean(data['durations']),
                'avg_effectiveness': statistics.mean(data['effectiveness']),
                'usage_count': len(data['durations']),
                'consistency': 1.0 - (statistics.stdev(data['durations']) / statistics.mean(data['durations']))
                    if len(data['durations']) > 1 and statistics.mean(data['durations']) > 0 else 1.0
            }
        
        # User behavior analysis
        user_behavior = self._analyze_user_behavior(recent_sessions)
        
        # Performance trends
        trends = self._calculate_trends(recent_queries, recent_snapshots)
        
        # Health assessment
        health_score = self._calculate_health_score(avg_response_time, cache_hit_ratio, error_rate)
        
        return {
            'report_generated': datetime.now().isoformat(),
            'time_range_hours': time_range_hours,
            'summary': {
                'total_queries': total_queries,
                'avg_response_time': avg_response_time,
                'cache_hit_ratio': cache_hit_ratio,
                'error_rate': error_rate,
                'avg_results_count': avg_results_count,
                'health_score': health_score
            },
            'stone_performance': stone_stats,
            'user_behavior': user_behavior,
            'trends': trends,
            'recommendations': self._generate_recommendations(avg_response_time, cache_hit_ratio, error_rate)
        }
    
    def _analyze_user_behavior(self, sessions: List[SearchSession]) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        if not sessions:
            return {}
        
        # Session metrics
        session_durations = [s.end_time - s.start_time for s in sessions if s.end_time]
        avg_session_duration = statistics.mean(session_durations) if session_durations else 0
        
        # Query patterns
        all_queries = []
        all_stones = []
        refinements = 0
        
        for session in sessions:
            all_queries.extend(session.queries)
            all_stones.extend(session.stones_used)
            
            # Check for query refinements (similar queries in same session)
            if len(session.queries) > 1:
                for i in range(len(session.queries) - 1):
                    if self._are_queries_similar(session.queries[i], session.queries[i + 1]):
                        refinements += 1
        
        query_patterns = Counter(all_queries)
        stone_preferences = Counter(all_stones)
        
        # Calculate bounce rate (sessions with only one search)
        single_search_sessions = sum(1 for s in sessions if s.total_searches == 1)
        bounce_rate = single_search_sessions / len(sessions) if sessions else 0
        
        # Refinement rate
        refinement_rate = refinements / len(sessions) if sessions else 0
        
        return {
            'total_sessions': len(sessions),
            'avg_session_duration': avg_session_duration,
            'avg_searches_per_session': statistics.mean([s.total_searches for s in sessions]),
            'bounce_rate': bounce_rate,
            'refinement_rate': refinement_rate,
            'top_queries': dict(query_patterns.most_common(10)),
            'stone_preferences': dict(stone_preferences),
        }
    
    def _are_queries_similar(self, query1: str, query2: str) -> bool:
        """Check if two queries are similar (indicating refinement)"""
        # Simple similarity check based on shared words
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        if not words1 or not words2:
            return False
        
        shared_words = len(words1.intersection(words2))
        total_words = len(words1.union(words2))
        
        return shared_words / total_words > 0.5  # 50% word overlap threshold
    
    def _calculate_trends(self, queries: List[QueryPerformance], snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate performance trends"""
        if len(queries) < 2:
            return {'error': 'Insufficient data for trend analysis'}
        
        # Sort by timestamp
        queries.sort(key=lambda x: x.timestamp)
        snapshots.sort(key=lambda x: x['timestamp'])
        
        # Split into first and second half for trend comparison
        mid_point = len(queries) // 2
        first_half = queries[:mid_point]
        second_half = queries[mid_point:]
        
        first_avg_time = statistics.mean([q.total_time for q in first_half])
        second_avg_time = statistics.mean([q.total_time for q in second_half])
        
        first_cache_ratio = sum(1 for q in first_half if q.cache_hit) / len(first_half)
        second_cache_ratio = sum(1 for q in second_half if q.cache_hit) / len(second_half)
        
        return {
            'response_time_trend': 'improving' if second_avg_time < first_avg_time else 'degrading',
            'response_time_change': ((second_avg_time - first_avg_time) / first_avg_time) * 100,
            'cache_efficiency_trend': 'improving' if second_cache_ratio > first_cache_ratio else 'degrading',
            'cache_efficiency_change': ((second_cache_ratio - first_cache_ratio) / first_cache_ratio) * 100
                if first_cache_ratio > 0 else 0
        }
    
    def _calculate_health_score(self, response_time: float, cache_ratio: float, error_rate: float) -> float:
        """Calculate overall system health score (0-100)"""
        # Performance score (0-40 points)
        performance_score = max(0, 40 - (response_time - self.performance_baselines['avg_response_time']) * 20)
        
        # Cache efficiency score (0-30 points)
        cache_score = (cache_ratio / self.performance_baselines['cache_hit_ratio']) * 30
        cache_score = min(30, max(0, cache_score))
        
        # Reliability score (0-30 points)
        reliability_score = max(0, 30 - (error_rate / self.performance_baselines['error_rate']) * 30)
        
        total_score = performance_score + cache_score + reliability_score
        return min(100, max(0, total_score))
    
    def _generate_recommendations(self, response_time: float, cache_ratio: float, error_rate: float) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if response_time > self.performance_baselines['avg_response_time'] * 1.5:
            recommendations.append("Consider optimizing search algorithms or increasing cache size")
        
        if cache_ratio < self.performance_baselines['cache_hit_ratio']:
            recommendations.append("Improve cache warming strategy or increase cache TTL")
        
        if error_rate > self.performance_baselines['error_rate']:
            recommendations.append("Investigate error patterns and improve error handling")
        
        if not recommendations:
            recommendations.append("System performance is within acceptable parameters")
        
        return recommendations
    
    def export_performance_report(self, report: Dict[str, Any], format: str = 'json') -> str:
        """Export performance report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_report_{timestamp}.{format}"
        filepath = os.path.join(self.export_path, filename)
        
        try:
            if format.lower() == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, default=str)
            
            elif format.lower() == 'csv':
                self._export_to_csv(report, filepath)
            
            logger.info(f"Performance report exported to: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to export report: {e}")
            return ""
    
    def _export_to_csv(self, report: Dict[str, Any], filepath: str):
        """Export report data to CSV format"""
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Summary section
            writer.writerow(['Performance Summary'])
            writer.writerow(['Metric', 'Value'])
            for key, value in report.get('summary', {}).items():
                writer.writerow([key, value])
            
            writer.writerow([])  # Empty row
            
            # Stone performance section
            writer.writerow(['Stone Performance'])
            writer.writerow(['Stone', 'Avg Duration', 'Avg Effectiveness', 'Usage Count', 'Consistency'])
            for stone, stats in report.get('stone_performance', {}).items():
                writer.writerow([
                    stone,
                    stats.get('avg_duration', 0),
                    stats.get('avg_effectiveness', 0),
                    stats.get('usage_count', 0),
                    stats.get('consistency', 0)
                ])
    
    def export_query_history(self, limit: int = 1000) -> str:
        """Export query performance history to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"query_history_{timestamp}.csv"
        filepath = os.path.join(self.export_path, filename)
        
        try:
            recent_queries = self.query_performance_history[-limit:]
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header
                writer.writerow([
                    'Timestamp', 'Query', 'Total Time', 'Cache Hit', 
                    'Results Count', 'Avg Relevance Score', 'Error Count'
                ])
                
                # Data rows
                for query in recent_queries:
                    writer.writerow([
                        datetime.fromtimestamp(query.timestamp).isoformat(),
                        query.query,
                        query.total_time,
                        query.cache_hit,
                        query.results_count,
                        statistics.mean(query.relevance_scores) if query.relevance_scores else 0,
                        query.error_count
                    ])
            
            logger.info(f"Query history exported to: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to export query history: {e}")
            return ""
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time system metrics"""
        current_time = time.time()
        recent_cutoff = current_time - 300  # Last 5 minutes
        
        recent_queries = [q for q in self.query_performance_history if q.timestamp > recent_cutoff]
        
        if not recent_queries:
            return {
                'status': 'no_recent_activity',
                'active_sessions': len(self.active_sessions),
                'timestamp': current_time
            }
        
        return {
            'status': 'active',
            'queries_last_5min': len(recent_queries),
            'avg_response_time_5min': statistics.mean([q.total_time for q in recent_queries]),
            'cache_hit_ratio_5min': sum(1 for q in recent_queries if q.cache_hit) / len(recent_queries),
            'active_sessions': len(self.active_sessions),
            'error_rate_5min': sum(q.error_count for q in recent_queries) / len(recent_queries),
            'timestamp': current_time
        }

# Global analytics engine instance
global_analytics_engine = EnhancedAnalyticsEngine()
