"""
Flask Backend API for Infinity Stones Search Engine
Connects the web frontend with the Python search engine
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import time
from infinity_search_engine import InfinityStonesSearchEngine, StoneType

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize the search engine
print("🔮 Initializing Infinity Stones Search Engine...")
search_engine = InfinityStonesSearchEngine('data-set.json')
print("✨ Search engine ready!")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint for search functionality"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        stone_preference = data.get('stone', None)
        page = data.get('page', 1)
        per_page = data.get('per_page', 25)  # Default 25 results per page
        
        # Validate pagination parameters
        try:
            page = int(page)
            per_page = int(per_page)
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:  # Limit max per_page to 100
                per_page = 25
        except (ValueError, TypeError):
            page = 1
            per_page = 25
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'success': False
            }), 400
        
        # Convert stone string to StoneType enum
        stone_type = None
        if stone_preference and stone_preference != 'all':
            # Handle multiple stones (comma-separated) or single stone
            if ',' in stone_preference:
                # Multiple stones selected - use all stones
                stone_type = None
            else:
                try:
                    stone_type = StoneType[stone_preference.upper()]
                except KeyError:
                    return jsonify({
                        'error': f'Invalid stone type: {stone_preference}',
                        'success': False
                    }), 400
        
        # Perform search
        start_time = time.time()
        results = search_engine.search(query, stone_type)
        search_time = time.time() - start_time
        
        # Calculate pagination
        total_results = len(results)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = results[start_idx:end_idx]
        total_pages = (total_results + per_page - 1) // per_page  # Ceiling division
        
        # Convert paginated results to JSON-serializable format
        serialized_results = []
        for result in paginated_results:
            serialized_result = {
                'product_id': result.product_id,
                'product_data': result.product_data,
                'relevance_score': result.relevance_score,
                'stone_powers': {stone.value: power for stone, power in result.stone_powers.items()},
                'matched_fields': result.matched_fields
            }
            serialized_results.append(serialized_result)
        
        return jsonify({
            'success': True,
            'query': query,
            'stone_used': stone_preference,
            'results': serialized_results,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_results': total_results,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1,
                'next_page': page + 1 if page < total_pages else None,
                'prev_page': page - 1 if page > 1 else None
            },
            'search_time': search_time,
            'timestamp': time.time()
        })
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'success': False
        }), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """API endpoint for analytics data"""
    try:
        analytics = search_engine.get_analytics()
        
        # Convert analytics to JSON-serializable format
        serialized_analytics = {
            'total_products': analytics['total_products'],
            'search_analytics': {
                'total_searches': analytics['search_analytics']['total_searches'],
                'popular_queries': dict(analytics['search_analytics']['popular_queries']),
                'search_times': analytics['search_analytics']['search_times'],
                'stone_usage': {str(stone): count for stone, count in analytics['search_analytics']['stone_usage'].items()}
            },
            'business_insights': analytics['business_insights'],
            'stone_effectiveness': {str(stone): effectiveness for stone, effectiveness in analytics['stone_effectiveness'].items()}
        }
        
        return jsonify({
            'success': True,
            'analytics': serialized_analytics,
            'timestamp': time.time()
        })
        
    except Exception as e:
        print(f"Analytics error: {e}")
        return jsonify({
            'error': 'Failed to retrieve analytics',
            'success': False
        }), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """API endpoint for search suggestions"""
    try:
        query = request.args.get('q', '').strip().lower()
        
        if len(query) < 2:
            return jsonify({
                'success': True,
                'suggestions': []
            })
        
        # Get popular queries that match the input
        analytics = search_engine.get_analytics()
        popular_queries = analytics['search_analytics']['popular_queries']
        
        # Filter and sort suggestions
        suggestions = []
        for popular_query, count in popular_queries.items():
            if query in popular_query.lower():
                suggestions.append({
                    'query': popular_query,
                    'count': count
                })
        
        # Sort by count (most popular first)
        suggestions.sort(key=lambda x: x['count'], reverse=True)
        
        # Return top 5 suggestions
        suggestions = suggestions[:5]
        
        return jsonify({
            'success': True,
            'suggestions': [s['query'] for s in suggestions],
            'timestamp': time.time()
        })
        
    except Exception as e:
        print(f"Suggestions error: {e}")
        return jsonify({
            'error': 'Failed to get suggestions',
            'success': False
        }), 500

@app.route('/api/stones', methods=['GET'])
def get_stones_info():
    """API endpoint for stone information"""
    try:
        stones_info = {
            'space': {
                'name': 'Space Stone',
                'color': 'blue',
                'emoji': '🔵',
                'description': 'Exploratory Data Analysis - Explores the entire product database space',
                'power': 'Data exploration and indexing'
            },
            'mind': {
                'name': 'Mind Stone',
                'color': 'yellow',
                'emoji': '🟡',
                'description': 'Data Visualization - Presents search results in user-friendly formats',
                'power': 'Search interface and results display'
            },
            'reality': {
                'name': 'Reality Stone',
                'color': 'red',
                'emoji': '🔴',
                'description': 'Domain Knowledge - Understands e-commerce product categories',
                'power': 'Product categorization and filtering'
            },
            'power': {
                'name': 'Power Stone',
                'color': 'purple',
                'emoji': '🟣',
                'description': 'Compute Resources - Provides raw computational force for algorithms',
                'power': 'Search algorithms and ranking'
            },
            'time': {
                'name': 'Time Stone',
                'color': 'green',
                'emoji': '🟢',
                'description': 'Performance Optimization - Optimizes search performance and caching',
                'power': 'Search optimization and caching'
            },
            'soul': {
                'name': 'Soul Stone',
                'color': 'orange',
                'emoji': '🟠',
                'description': 'Business Intelligence - Provides insights and analytics',
                'power': 'Analytics and recommendations'
            }
        }
        
        return jsonify({
            'success': True,
            'stones': stones_info,
            'timestamp': time.time()
        })
        
    except Exception as e:
        print(f"Stones info error: {e}")
        return jsonify({
            'error': 'Failed to get stones information',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Infinity Stones Search Engine is operational',
        'timestamp': time.time(),
        'total_products': len(search_engine.products)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'success': False
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Infinity Stones Search Engine Web Server...")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("🔮 API endpoints available at: http://localhost:5000/api/")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
