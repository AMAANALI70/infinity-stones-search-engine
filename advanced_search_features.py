"""
Advanced Search Features for Infinity Stones Search Engine
Implements fuzzy search, boolean operators, and faceted filtering
"""

import re
import math
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import difflib
import logging

logger = logging.getLogger(__name__)

@dataclass
class FuzzyMatch:
    """Represents a fuzzy match result"""
    original_term: str
    matched_term: str
    similarity: float
    source: str  # Which field it was found in

class FuzzySearchEngine:
    """
    Fuzzy search implementation with configurable similarity thresholds
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold
        self.word_cache = {}  # Cache for performance
        
    def find_fuzzy_matches(self, query_term: str, corpus_terms: List[str], max_results: int = 10) -> List[FuzzyMatch]:
        """
        Find fuzzy matches for a query term in a corpus
        """
        matches = []
        query_lower = query_term.lower()
        
        for term in corpus_terms:
            term_lower = term.lower()
            
            # Skip exact matches (handle separately)
            if query_lower == term_lower:
                continue
                
            # Calculate similarity using multiple methods
            similarities = [
                difflib.SequenceMatcher(None, query_lower, term_lower).ratio(),
                self._jaro_similarity(query_lower, term_lower),
                self._levenshtein_similarity(query_lower, term_lower)
            ]
            
            # Use the best similarity score
            best_similarity = max(similarities)
            
            if best_similarity >= self.similarity_threshold:
                matches.append(FuzzyMatch(
                    original_term=query_term,
                    matched_term=term,
                    similarity=best_similarity,
                    source="corpus"
                ))
        
        # Sort by similarity and return top matches
        matches.sort(key=lambda x: x.similarity, reverse=True)
        return matches[:max_results]
    
    def _jaro_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate Jaro similarity between two strings
        """
        if len(s1) == 0 and len(s2) == 0:
            return 1.0
        if len(s1) == 0 or len(s2) == 0:
            return 0.0
            
        match_distance = (max(len(s1), len(s2)) // 2) - 1
        match_distance = max(0, match_distance)
        
        s1_matches = [False] * len(s1)
        s2_matches = [False] * len(s2)
        
        matches = 0
        transpositions = 0
        
        # Identify matches
        for i in range(len(s1)):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len(s2))
            
            for j in range(start, end):
                if s2_matches[j] or s1[i] != s2[j]:
                    continue
                s1_matches[i] = s2_matches[j] = True
                matches += 1
                break
        
        if matches == 0:
            return 0.0
        
        # Count transpositions
        k = 0
        for i in range(len(s1)):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
        
        jaro = (matches / len(s1) + matches / len(s2) + 
                (matches - transpositions / 2) / matches) / 3
        
        return jaro
    
    def _levenshtein_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate Levenshtein similarity (1 - normalized distance)
        """
        if len(s1) == 0 and len(s2) == 0:
            return 1.0
        
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
            
        distance = self._levenshtein_distance(s1, s2)
        return 1.0 - (distance / max_len)
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between two strings
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

class BooleanSearchEngine:
    """
    Boolean search with AND, OR, NOT operators
    """
    
    def __init__(self):
        self.operators = {'AND', 'OR', 'NOT', '(', ')'}
        
    def parse_boolean_query(self, query: str) -> Dict[str, Any]:
        """
        Parse a boolean query into structured format
        
        Examples:
        - "bluetooth AND wireless"
        - "phone OR tablet"
        - "camera NOT digital"
        - "bluetooth AND (headphone OR speaker)"
        """
        try:
            # Tokenize the query
            tokens = self._tokenize_boolean_query(query)
            
            # Parse into expression tree
            expression = self._parse_expression(tokens)
            
            return {
                'success': True,
                'expression': expression,
                'original_query': query,
                'tokens': tokens
            }
        except Exception as e:
            logger.error(f"Boolean query parsing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_terms': query.split()
            }
    
    def _tokenize_boolean_query(self, query: str) -> List[str]:
        """
        Tokenize boolean query into terms and operators
        """
        # Replace operators with standardized versions
        query = query.upper()
        
        # Handle parentheses with spaces
        query = query.replace('(', ' ( ').replace(')', ' ) ')
        
        # Tokenize
        tokens = []
        for token in query.split():
            token = token.strip()
            if token:
                if token in self.operators:
                    tokens.append(token)
                else:
                    # It's a search term
                    tokens.append(token.lower())
        
        return tokens
    
    def _parse_expression(self, tokens: List[str]) -> Dict[str, Any]:
        """
        Parse tokens into expression tree
        """
        if not tokens:
            return {'type': 'empty'}
        
        # Simple recursive descent parser
        return self._parse_or_expression(tokens, 0)[0]
    
    def _parse_or_expression(self, tokens: List[str], pos: int) -> Tuple[Dict[str, Any], int]:
        """Parse OR expression (lowest precedence)"""
        left, pos = self._parse_and_expression(tokens, pos)
        
        while pos < len(tokens) and tokens[pos] == 'OR':
            pos += 1  # consume OR
            right, pos = self._parse_and_expression(tokens, pos)
            left = {'type': 'or', 'left': left, 'right': right}
        
        return left, pos
    
    def _parse_and_expression(self, tokens: List[str], pos: int) -> Tuple[Dict[str, Any], int]:
        """Parse AND expression (medium precedence)"""
        left, pos = self._parse_not_expression(tokens, pos)
        
        while pos < len(tokens) and tokens[pos] == 'AND':
            pos += 1  # consume AND
            right, pos = self._parse_not_expression(tokens, pos)
            left = {'type': 'and', 'left': left, 'right': right}
        
        return left, pos
    
    def _parse_not_expression(self, tokens: List[str], pos: int) -> Tuple[Dict[str, Any], int]:
        """Parse NOT expression (highest precedence)"""
        if pos < len(tokens) and tokens[pos] == 'NOT':
            pos += 1  # consume NOT
            expr, pos = self._parse_primary_expression(tokens, pos)
            return {'type': 'not', 'operand': expr}, pos
        else:
            return self._parse_primary_expression(tokens, pos)
    
    def _parse_primary_expression(self, tokens: List[str], pos: int) -> Tuple[Dict[str, Any], int]:
        """Parse primary expression (terms and parentheses)"""
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
        
        if tokens[pos] == '(':
            pos += 1  # consume (
            expr, pos = self._parse_or_expression(tokens, pos)
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            pos += 1  # consume )
            return expr, pos
        elif tokens[pos] not in self.operators:
            # It's a term
            term = tokens[pos]
            pos += 1
            return {'type': 'term', 'value': term}, pos
        else:
            raise ValueError(f"Unexpected token: {tokens[pos]}")
    
    def evaluate_boolean_expression(self, expression: Dict[str, Any], product_matches: Dict[str, Set[str]]) -> Set[str]:
        """
        Evaluate boolean expression against product matches
        
        Args:
            expression: Parsed boolean expression
            product_matches: Dict mapping terms to sets of matching product IDs
        
        Returns:
            Set of product IDs that match the boolean expression
        """
        if expression['type'] == 'term':
            term = expression['value']
            return product_matches.get(term, set())
        
        elif expression['type'] == 'and':
            left_results = self.evaluate_boolean_expression(expression['left'], product_matches)
            right_results = self.evaluate_boolean_expression(expression['right'], product_matches)
            return left_results.intersection(right_results)
        
        elif expression['type'] == 'or':
            left_results = self.evaluate_boolean_expression(expression['left'], product_matches)
            right_results = self.evaluate_boolean_expression(expression['right'], product_matches)
            return left_results.union(right_results)
        
        elif expression['type'] == 'not':
            operand_results = self.evaluate_boolean_expression(expression['operand'], product_matches)
            # NOT returns all products except those matching the operand
            all_products = set()
            for product_set in product_matches.values():
                all_products.update(product_set)
            return all_products - operand_results
        
        else:
            return set()

class FacetedSearchEngine:
    """
    Faceted search and filtering capabilities
    """
    
    def __init__(self, products: List[Dict[str, Any]]):
        self.products = products
        self.facets = self._build_facets()
    
    def _build_facets(self) -> Dict[str, Dict[str, int]]:
        """
        Build facet indexes for filtering
        """
        facets = {
            'brand': defaultdict(int),
            'type': defaultdict(int), 
            'category': defaultdict(int),
            'price_range': defaultdict(int),
            'has_specs': defaultdict(int)
        }
        
        for product in self.products:
            # Brand facet
            if 'Brand' in product and product['Brand']:
                brand = product['Brand'].strip()
                if brand:
                    facets['brand'][brand] += 1
            
            # Type facet
            if 'Type' in product and product['Type']:
                product_type = product['Type'].strip()
                if product_type:
                    facets['type'][product_type] += 1
                    
                    # Infer category from type
                    category = self._infer_category(product_type)
                    if category:
                        facets['category'][category] += 1
            
            # Price range facet (if price info available)
            price_range = self._extract_price_range(product)
            if price_range:
                facets['price_range'][price_range] += 1
            
            # Specifications availability
            has_detailed_specs = self._has_detailed_specs(product)
            facets['has_specs']['Yes' if has_detailed_specs else 'No'] += 1
        
        # Convert defaultdicts to regular dicts and sort
        processed_facets = {}
        for facet_name, facet_data in facets.items():
            # Sort by count (descending) and keep top items
            sorted_items = sorted(facet_data.items(), key=lambda x: x[1], reverse=True)
            processed_facets[facet_name] = dict(sorted_items[:20])  # Top 20 items per facet
        
        return processed_facets
    
    def _infer_category(self, product_type: str) -> str:
        """
        Infer high-level category from product type
        """
        type_lower = product_type.lower()
        
        if any(keyword in type_lower for keyword in ['phone', 'mobile', 'smartphone', 'tablet']):
            return 'Mobile & Tablets'
        elif any(keyword in type_lower for keyword in ['laptop', 'computer', 'pc', 'desktop']):
            return 'Computers'
        elif any(keyword in type_lower for keyword in ['headphone', 'earphone', 'speaker', 'audio']):
            return 'Audio'
        elif any(keyword in type_lower for keyword in ['car', 'auto', 'vehicle']):
            return 'Automotive'
        elif any(keyword in type_lower for keyword in ['camera', 'photo', 'lens']):
            return 'Photography'
        elif any(keyword in type_lower for keyword in ['home', 'kitchen', 'furniture']):
            return 'Home & Kitchen'
        elif any(keyword in type_lower for keyword in ['beauty', 'cosmetic', 'skincare']):
            return 'Beauty'
        elif any(keyword in type_lower for keyword in ['sport', 'fitness', 'exercise']):
            return 'Sports & Fitness'
        else:
            return 'Other'
    
    def _extract_price_range(self, product: Dict[str, Any]) -> Optional[str]:
        """
        Extract price range information if available
        """
        # Look for price indicators in various fields
        text_fields = [product.get('Sales Package', ''), product.get('Name', '')]
        full_text = ' '.join(str(field) for field in text_fields).lower()
        
        # Look for price patterns
        if 'under' in full_text and any(price in full_text for price in ['1000', '500', '100']):
            return 'Under ₹1000'
        elif any(price in full_text for price in ['premium', 'expensive', 'high-end']):
            return 'Premium'
        elif any(price in full_text for price in ['budget', 'affordable', 'cheap']):
            return 'Budget'
        else:
            return 'Standard'
    
    def _has_detailed_specs(self, product: Dict[str, Any]) -> bool:
        """
        Determine if product has detailed specifications
        """
        sales_package = product.get('Sales Package', '')
        if not sales_package:
            return False
        
        # Count technical specifications
        spec_indicators = ['gb', 'mb', 'inch', 'mp', 'mah', 'hz', 'ghz', 'ram', 'storage', 'battery']
        spec_count = sum(1 for indicator in spec_indicators if indicator in sales_package.lower())
        
        return spec_count >= 2 or len(sales_package) > 200
    
    def get_facets(self) -> Dict[str, Dict[str, int]]:
        """
        Get all available facets
        """
        return self.facets
    
    def filter_by_facets(self, product_ids: Set[str], filters: Dict[str, List[str]]) -> Set[str]:
        """
        Filter products by selected facets
        
        Args:
            product_ids: Set of product IDs to filter
            filters: Dict of facet filters, e.g., {'brand': ['Samsung', 'Apple'], 'category': ['Mobile']}
        
        Returns:
            Filtered set of product IDs
        """
        if not filters:
            return product_ids
        
        filtered_ids = set()
        
        for product in self.products:
            product_id = product.get('id', '')
            if product_id not in product_ids:
                continue
            
            # Check if product matches all filter criteria
            matches_all_filters = True
            
            for facet_name, selected_values in filters.items():
                if not selected_values:  # Empty filter means no restriction
                    continue
                
                product_matches_facet = False
                
                if facet_name == 'brand':
                    product_brand = product.get('Brand', '')
                    if product_brand in selected_values:
                        product_matches_facet = True
                
                elif facet_name == 'type':
                    product_type = product.get('Type', '')
                    if product_type in selected_values:
                        product_matches_facet = True
                
                elif facet_name == 'category':
                    product_type = product.get('Type', '')
                    inferred_category = self._infer_category(product_type)
                    if inferred_category in selected_values:
                        product_matches_facet = True
                
                elif facet_name == 'price_range':
                    product_price_range = self._extract_price_range(product)
                    if product_price_range in selected_values:
                        product_matches_facet = True
                
                elif facet_name == 'has_specs':
                    has_specs = 'Yes' if self._has_detailed_specs(product) else 'No'
                    if has_specs in selected_values:
                        product_matches_facet = True
                
                if not product_matches_facet:
                    matches_all_filters = False
                    break
            
            if matches_all_filters:
                filtered_ids.add(product_id)
        
        return filtered_ids

# Global instances
global_fuzzy_engine = FuzzySearchEngine(similarity_threshold=0.6)
global_boolean_engine = BooleanSearchEngine()
global_faceted_engine = None  # Will be initialized with products
