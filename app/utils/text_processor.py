"""
Natural Language Processing utilities for incident text analysis.
Implements text preprocessing, keyword extraction, and similarity matching.
"""

import re
from difflib import SequenceMatcher


class TextProcessor:
    """
    Handles NLP operations for incident text analysis.
    Based on techniques from NLP fundamentals training.
    """
    
    # Common words that don't add meaning (stop words)
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'am', 'been', 'being', 'have', 'had',
        'having', 'do', 'does', 'did', 'doing', 'would', 'should', 'could',
        'ought', 'i', 'you', 'we', 'they', 'what', 'which', 'who', 'when',
        'where', 'why', 'how', 'this', 'these', 'those', 'but', 'or', 'can',
        'may', 'might', 'must', 'shall'
    }
    
    @staticmethod
    def preprocess_text(text):
        """
        Preprocess text for NLP analysis.
        
        Steps:
        1. Convert to lowercase
        2. Remove special characters
        3. Tokenise into words
        4. Remove stop words
        
        Args:
            text (str): Raw text to process
            
        Returns:
            list: List of meaningful tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Tokenise (split into words)
        tokens = text.split()
        
        # Remove stop words
        tokens = [word for word in tokens if word not in TextProcessor.STOP_WORDS]
        
        return tokens
    
    @staticmethod
    def extract_keywords(text, top_n=5):
        """
        Extract most important keywords from text.
        
        Args:
            text (str): Text to extract keywords from
            top_n (int): Number of top keywords to return
            
        Returns:
            list: Top N keywords by frequency
        """
        tokens = TextProcessor.preprocess_text(text)
        
        # Count word frequencies
        word_freq = {}
        for word in tokens:
            if len(word) > 2:  # Only consider words longer than 2 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top N
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]
    
    @staticmethod
    def calculate_similarity(text1, text2):
        """
        Calculate similarity between two texts using token overlap and sequence matching.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        # Preprocess both texts
        tokens1 = set(TextProcessor.preprocess_text(text1))
        tokens2 = set(TextProcessor.preprocess_text(text2))
        
        # Avoid division by zero
        if not tokens1 or not tokens2:
            return 0.0
        
        # Calculate Jaccard similarity (token overlap)
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        jaccard_score = len(intersection) / len(union) if union else 0.0
        
        # Calculate sequence similarity (considers word order)
        sequence_score = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # Weighted average (70% token overlap, 30% sequence)
        similarity = (0.7 * jaccard_score) + (0.3 * sequence_score)
        
        return similarity
    
    @staticmethod
    def is_duplicate(new_text, existing_text, threshold=0.75):
        """
        Determine if new text is a duplicate of existing text.
        
        Args:
            new_text (str): New incident text
            existing_text (str): Existing incident text
            threshold (float): Similarity threshold (default 0.75 = 75% similar)
            
        Returns:
            bool: True if texts are considered duplicates
        """
        similarity = TextProcessor.calculate_similarity(new_text, existing_text)
        return similarity >= threshold