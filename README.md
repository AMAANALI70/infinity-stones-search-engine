# 🔮 Infinity Stones Search Engine

A powerful e-commerce search engine inspired by the Marvel Cinematic Universe's Infinity Stones, where each stone represents a different aspect of search functionality based on computer science principles.

## 🌐 Web Application

This search engine now includes a beautiful, interactive web application with:
- **Cosmic-themed UI** with animated Infinity Stones
- **Real-time search** with instant results
- **Advanced filtering** by category (Electronics, Automotive, Beauty, Home, Sports)
- **Interactive stone selection** to customize search behavior
- **Analytics dashboard** with search insights
- **3D particle effects** and cosmic animations

## 🌌 Overview

This search engine implements the concept from Task 04, where each Infinity Stone corresponds to a specific computer science principle:

| Stone | Color | CS Principle | Function |
|-------|-------|--------------|----------|
| 🔵 Space Stone | Blue | Exploratory Data Analysis (EDA) | Data exploration and indexing |
| 🟡 Mind Stone | Yellow | Data Visualization & Communication | Search interface and results display |
| 🔴 Reality Stone | Red | Domain Knowledge | Product categorization and filtering |
| 🟣 Power Stone | Purple | Compute Resources | Search algorithms and ranking |
| 🟢 Time Stone | Green | Algorithm Selection | Search optimization and caching |
| 🟠 Soul Stone | Orange | Business Intelligence | Analytics and recommendations |

## 🚀 Features

### Core Search Capabilities
- **Multi-dimensional Search**: Combines text matching, category filtering, and semantic analysis
- **Intelligent Ranking**: Uses TF-IDF scoring and weighted stone powers for relevance
- **Performance Optimization**: Caching and efficient algorithms for fast searches
- **Domain Intelligence**: E-commerce specific categorization and filtering
- **Analytics Dashboard**: Comprehensive search analytics and business insights

### Infinity Stones Powers

#### 🔵 Space Stone - Data Exploration
- **Power**: Explores the entire product database space
- **Function**: Builds comprehensive indexes for fast text searching
- **Algorithm**: Inverted index with word-based matching
- **Use Case**: Finding products by any text content

#### 🟡 Mind Stone - Visualization
- **Power**: Presents search results in user-friendly formats
- **Function**: Enhances result presentation and readability
- **Algorithm**: Presentation scoring based on data completeness
- **Use Case**: Improving user experience and result clarity

#### 🔴 Reality Stone - Domain Knowledge
- **Power**: Understands e-commerce product categories
- **Function**: Categorizes products and applies domain-specific filtering
- **Algorithm**: Keyword-based category classification
- **Use Case**: Finding products by category (electronics, automotive, beauty, etc.)

#### 🟣 Power Stone - Computational Power
- **Power**: Provides raw computational force for advanced algorithms
- **Function**: Implements TF-IDF scoring and result combination
- **Algorithm**: Term Frequency-Inverse Document Frequency
- **Use Case**: Advanced relevance scoring and result ranking

#### 🟢 Time Stone - Performance Optimization
- **Power**: Optimizes search performance and selects efficient algorithms
- **Function**: Implements caching and fast approximate search
- **Algorithm**: Jaccard similarity with caching
- **Use Case**: Fast searches and performance optimization

#### 🟠 Soul Stone - Business Intelligence
- **Power**: Provides insights and business analytics
- **Function**: Analyzes search patterns and product popularity
- **Algorithm**: Statistical analysis and trend detection
- **Use Case**: Business insights and search analytics

## 📦 Installation

### Prerequisites
- Python 3.7+
- Flask (for web application)
- JSON dataset file (`data-set.json`)

### Setup
1. Clone or download the project files
2. Ensure `data-set.json` is in the same directory
3. Install required Python packages:

```bash
pip install flask flask-cors
```

### Quick Start
```bash
# Start the web application
python app.py

# Open your browser and navigate to:
# http://localhost:5000
```

## 🎯 Usage

### Web Application (Recommended)
1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. **Search Features:**
   - Enter search queries in the cosmic search box
   - Select individual stones or "Use All Stones" for different search behaviors
   - Filter results by category (Electronics, Automotive, Beauty, Home, Sports)
   - Sort results by relevance, brand, or type
   - **Pagination**: Navigate through results with 25 items per page
   - **Result Ranking**: Each result shows global ranking position (#1, #2, etc.)
   - **Smooth Navigation**: Automatic scroll to top when changing pages
   - Click on results to view detailed product information

4. **Stone Selection:**
   - **Individual Stones**: Select specific algorithms (Space=Fast Search, Mind=AI, Reality=Ranking, etc.)
   - **All Stones**: Ultimate search power combining all six algorithms
   - **Visual Feedback**: Notifications and power indicators show which algorithms are active
   - **Detailed Guide**: See `STONE_POWERS_EXPLAINED.md` for complete stone functionality guide

5. **Category Filtering:**
   - **Electronics**: Bluetooth devices, speakers, headphones, converters, LED lights
   - **Automotive**: Car accessories, bike parts, vacuum cleaners, converters
   - **Beauty**: Cosmetics, creams, skincare, hair products
   - **Home**: Furniture, mattresses, pillows, household items
   - **Sports**: Gym equipment, fitness gear, yoga accessories, exercise tools

### API Endpoints
The web application exposes RESTful API endpoints:

```bash
# Search API
POST /api/search
{
    "query": "bluetooth speaker",
    "stone": "all"  # or specific stone names
}

# Analytics API
GET /api/analytics

# Suggestions API
GET /api/suggestions?q=blue

# Stone Information API
GET /api/stones

# Health Check
GET /api/health
```

### Command Line Mode
For testing and development:

```bash
# Interactive search mode
python infinity_search_engine.py

# Demonstration mode
python demo_search.py
```

### Programmatic Usage
```python
from infinity_search_engine import InfinityStonesSearchEngine, StoneType

# Initialize the search engine
engine = InfinityStonesSearchEngine('data-set.json')

# Search with all stones (returns up to 50 results)
results = engine.search("bluetooth speaker")

# Search with specific stone
results = engine.search("car vacuum", stone_preference=StoneType.REALITY)

# Get analytics
analytics = engine.get_analytics()
```

## 🔍 Search Examples

### Basic Search
```python
# Search for bluetooth products
results = engine.search("bluetooth")
```

### Category-Specific Search
```python
# Search using Reality Stone for automotive products
results = engine.search("car", stone_preference=StoneType.REALITY)
```

### Performance-Optimized Search
```python
# Search using Time Stone for fast results
results = engine.search("electronics", stone_preference=StoneType.TIME)
```

### Business Intelligence Search
```python
# Search using Soul Stone for business insights
results = engine.search("popular", stone_preference=StoneType.SOUL)
```

## 📊 Analytics Features

The search engine provides comprehensive analytics:

- **Search Statistics**: Total searches, average search time
- **Stone Usage**: How often each stone is used
- **Popular Queries**: Most searched terms
- **Product Analytics**: Popular products and categories
- **Performance Metrics**: Search speed and efficiency

## 🏗️ Architecture

### Core Components

1. **InfinityStonesSearchEngine**: Main engine class that orchestrates all stones
2. **Stone Classes**: Individual stone implementations (SpaceStone, MindStone, etc.)
3. **SearchResult**: Data structure for search results with stone powers
4. **Analytics System**: Comprehensive tracking and analysis

### Data Flow

1. **Data Loading**: Space Stone loads and indexes the dataset
2. **Query Processing**: Each stone processes the query according to its specialty
3. **Result Combination**: Power Stone combines results from all stones
4. **Analytics**: Soul Stone analyzes search patterns and results
5. **Caching**: Time Stone caches results for performance

## 🎨 Design Philosophy

The search engine embodies the philosophical themes from the Infinity Stones:

- **Power vs Responsibility**: Advanced algorithms balanced with user-friendly presentation
- **Utilitarianism vs Deontology**: Practical search results vs ethical data handling
- **Unity in Diversity**: Different search approaches working together
- **Balance**: Performance vs accuracy, speed vs comprehensiveness

## 🔧 Customization

### Adding New Stones
Extend the `StoneType` enum and create new stone classes:

```python
class CustomStone:
    def __init__(self, engine):
        self.engine = engine
    
    def search(self, query: str) -> List[SearchResult]:
        # Implement custom search logic
        pass
```

### Modifying Stone Weights
Adjust the power distribution in `PowerStone.combine_results()`:

```python
stone_weights = {
    StoneType.SPACE: 0.3,    # Adjust these values
    StoneType.MIND: 0.1,
    # ... other stones
}
```

## 🧪 Testing

### Web Application Testing
1. **Main Application**: Navigate to `http://localhost:5000`
2. **Category Filter Test**: Use `http://localhost:5000/test_category_filter.html` for dedicated category testing
3. **Manual Testing**: Try various search queries and category combinations

### Command Line Testing
```bash
python demo_search.py
```

This will:
- Test each stone individually
- Demonstrate combined search power
- Show performance metrics
- Display analytics dashboard

### Test Queries
Recommended test queries for different categories:
- **Electronics**: "bluetooth", "speaker", "headphones", "led", "converter"
- **Automotive**: "car", "vacuum", "tyre", "bike", "vehicle"
- **Beauty**: "cream", "beauty", "skin", "hair"
- **Home**: "mattress", "furniture", "table", "chair", "pillow"
- **Sports**: "gym", "fitness", "exercise", "yoga", "workout"

## 📈 Performance

- **Dataset Size**: 21,176+ products indexed
- **Indexing**: O(n) where n is the number of products
- **Search Speed**: O(log n) for cached queries, O(n) for new queries
- **Pagination**: 25 results per page with smooth navigation
- **Result Priority**: Maintains relevance-based ranking across all pages
- **Memory Usage**: Efficient indexing with minimal memory overhead
- **Caching**: Advanced caching system for repeated queries
- **Category Filtering**: Intelligent mapping for accurate categorization

## 🆕 Recent Improvements

### Version 2.0 - Web Application
- ✅ **Full Web Application**: Beautiful cosmic-themed UI with Flask backend
- ✅ **Fixed Category Filtering**: Enhanced filtering logic for accurate categorization
- ✅ **Smart Pagination**: 25 results per page with smooth navigation and result priority
- ✅ **Unlimited Results**: Removed backend limits, now returns all matching results
- ✅ **Result Ranking**: Global ranking system maintains priority across all pages
- ✅ **Advanced Category Mapping**: Smart filtering for Electronics, Automotive, Beauty, Home, Sports
- ✅ **Real-time Search**: Instant search with live filtering
- ✅ **Interactive Animations**: 3D particle effects and stone animations
- ✅ **RESTful API**: Complete API endpoints for integration
- ✅ **Analytics Dashboard**: Comprehensive search analytics and insights

### Category Filtering Fix
Previously, the category filter was not working correctly due to simple string matching. Now it uses intelligent mapping:

- **Smart Text Analysis**: Searches across product type, brand, and features
- **Comprehensive Mapping**: Each category has multiple keyword associations
- **Case-Insensitive**: All comparisons are normalized for better matching
- **Flexible Matching**: Handles variations in product descriptions

## 🎓 Educational Value

This project demonstrates:

1. **Search Engine Design**: Complete search engine architecture
2. **Data Structures**: Inverted indexes, caching, and analytics
3. **Algorithms**: TF-IDF, Jaccard similarity, weighted scoring
4. **Software Architecture**: Modular design with clear separation of concerns
5. **Creative Problem Solving**: Using pop culture concepts to teach CS principles

## 🔮 Future Enhancements

- **Machine Learning Integration**: Add ML-based relevance scoring and recommendations
- **Advanced Personalization**: User-based search preferences and history
- **Elasticsearch Integration**: Enhanced full-text search capabilities
- **Advanced Visualizations**: Charts for search trends and category distribution
- **Mobile Responsiveness**: Optimized mobile experience
- **Multi-language Support**: International product search
- **Voice Search**: Speech-to-text search capability
- **Product Recommendations**: AI-powered similar product suggestions


## 👨‍💻 Author

**Amaan Ali D Doddamani**
- Task: Infinity Stones Search Engine Implementation
  - v1.0: Command-line search engine with all six stones
  - v2.0: Full web application with enhanced filtering and UI

---

*"With all six stones, I could simply snap my fingers, and search results would be perfectly relevant. The universe would be at my fingertips."* - Thanos (probably)

🔮 **May the power of the Infinity Stones guide your search!** 🔮
