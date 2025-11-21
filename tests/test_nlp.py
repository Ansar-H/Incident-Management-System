"""
Test NLP duplicate detection system.
Validates text preprocessing, similarity calculation, and duplicate detection.
"""

import pytest
from app.utils.text_processor import TextProcessor
from app.utils.duplicate_detector import DuplicateDetector


class TestTextProcessor:
    """Test text preprocessing and similarity functions."""
    
    def test_preprocess_text_lowercase(self):
        """Test text is converted to lowercase."""
        text = "Client Cannot LOGIN to Additiv"
        tokens = TextProcessor.preprocess_text(text)
        
        # All tokens should be lowercase
        assert all(token.islower() for token in tokens)
    
    def test_preprocess_text_removes_stop_words(self):
        """Test stop words are removed."""
        text = "The client is unable to login and cannot access the system"
        tokens = TextProcessor.preprocess_text(text)
        
        # Stop words should be removed
        assert 'the' not in tokens
        assert 'is' not in tokens
        assert 'to' not in tokens
        assert 'and' not in tokens
        
        # Meaningful words should remain
        assert 'client' in tokens
        assert 'unable' in tokens
        assert 'login' in tokens
    
    def test_preprocess_text_removes_special_characters(self):
        """Test special characters are removed."""
        text = "Login! failed? (timeout)"
        tokens = TextProcessor.preprocess_text(text)
        
        # Should only contain alphanumeric tokens
        assert all(token.isalnum() for token in tokens)
    
    def test_extract_keywords(self):
        """Test keyword extraction returns most frequent words."""
        text = "login failure login timeout authentication login error"
        keywords = TextProcessor.extract_keywords(text, top_n=2)
        
        # 'login' appears 3 times, should be top keyword
        assert 'login' in keywords
        assert len(keywords) <= 2
    
    def test_calculate_similarity_identical_texts(self):
        """Test similarity of identical texts is 1.0."""
        text1 = "Client cannot login to Additiv platform"
        text2 = "Client cannot login to Additiv platform"
        
        similarity = TextProcessor.calculate_similarity(text1, text2)
        
        assert similarity == 1.0
    
    def test_calculate_similarity_completely_different(self):
        """Test similarity of completely different texts is low."""
        text1 = "Client login authentication failure timeout"
        text2 = "Balance display incorrect formatting issue"
        
        similarity = TextProcessor.calculate_similarity(text1, text2)
        
        # Should be very low similarity
        assert similarity < 0.3
    
    def test_calculate_similarity_similar_texts(self):
        """Test similarity of similar texts is high."""
        text1 = "Multiple clients cannot login to Additiv platform authentication timeout"
        text2 = "Clients experiencing login timeout on Additiv authentication failure"
        
        similarity = TextProcessor.calculate_similarity(text1, text2)
        
        # Should have moderate to high similarity
        assert similarity > 0.4
    
    def test_calculate_similarity_empty_text(self):
        """Test similarity with empty text returns 0."""
        text1 = "Some text here"
        text2 = ""
        
        similarity = TextProcessor.calculate_similarity(text1, text2)
        
        assert similarity == 0.0
    
    def test_is_duplicate_above_threshold(self):
        """Test is_duplicate returns True when similarity exceeds threshold."""
        text1 = "Additiv login timeout error affecting multiple clients"
        text2 = "Multiple clients experiencing Additiv login timeout errors"
        
        is_dup = TextProcessor.is_duplicate(text1, text2, threshold=0.5)
        
        assert is_dup is True
    
    def test_is_duplicate_below_threshold(self):
        """Test is_duplicate returns False when similarity below threshold."""
        text1 = "Login authentication failure"
        text2 = "Balance display formatting error"
        
        is_dup = TextProcessor.is_duplicate(text1, text2, threshold=0.75)
        
        assert is_dup is False


class TestDuplicateDetector:
    """Test duplicate incident detection functionality."""
    
    def test_check_for_duplicates_no_duplicates(self, app):
        """Test check returns no duplicates when none exist."""
        result = DuplicateDetector.check_for_duplicates(
            title="Completely unique incident title xyz123",
            description="This is a unique description that does not match anything",
            platform="Additiv",
            threshold=0.75
        )
        
        assert result['is_duplicate'] is False
        assert len(result['similar_incidents']) == 0
    
    def test_check_for_duplicates_finds_similar(self, app, sample_incident):
        """Test detector finds similar incidents."""
        # sample_incident has title "Test incident for unit testing"
        result = DuplicateDetector.check_for_duplicates(
            title="Test incident for unit testing purposes",
            description="This is a test incident created for automated testing",
            platform="Additiv",
            threshold=0.50
        )
        
        # Should find the sample incident as similar
        assert result['is_duplicate'] is True
        assert len(result['similar_incidents']) > 0
    
    def test_check_for_duplicates_platform_specific(self, app, sample_incident):
        """Test detector only compares same platform incidents."""
        # sample_incident is Additiv platform
        result = DuplicateDetector.check_for_duplicates(
            title="Test incident for unit testing",
            description="This is a test incident created for automated testing purposes",
            platform="Avaloq",  # Different platform
            threshold=0.50
        )
        
        # Should not find duplicates on different platform
        assert result['is_duplicate'] is False
    
    def test_check_for_duplicates_threshold_sensitivity(self, app, sample_incident):
        """Test threshold affects duplicate detection."""
        # High threshold (strict)
        result_strict = DuplicateDetector.check_for_duplicates(
            title="Similar test incident",
            description="Testing incident for automation",
            platform="Additiv",
            threshold=0.90
        )
        
        # Low threshold (lenient)
        result_lenient = DuplicateDetector.check_for_duplicates(
            title="Similar test incident",
            description="Testing incident for automation",
            platform="Additiv",
            threshold=0.30
        )
        
        # Lenient should find more (or equal) duplicates than strict
        assert len(result_lenient['similar_incidents']) >= len(result_strict['similar_incidents'])
    
    def test_find_similar_incidents_returns_sorted(self, app, sample_incident):
        """Test similar incidents are sorted by similarity score."""
        result = DuplicateDetector.find_similar_incidents(
            title="Test incident unit testing",
            description="Automated testing incident",
            platform="Additiv",
            threshold=0.40,
            limit=5
        )
        
        # Check results are sorted descending by similarity
        if len(result) > 1:
            for i in range(len(result) - 1):
                assert result[i][1] >= result[i+1][1]
    
    def test_find_similar_incidents_respects_limit(self, app):
        """Test similar incidents respects the limit parameter."""
        result = DuplicateDetector.find_similar_incidents(
            title="Test",
            description="Test",
            platform="Additiv",
            threshold=0.10,
            limit=3
        )
        
        # Should return at most 3 results
        assert len(result) <= 3