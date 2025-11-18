"""
Duplicate incident detection using NLP similarity matching.
Prevents creation of duplicate incidents by comparing text similarity.
"""

from app.models.incident import Incident
from app.utils.text_processor import TextProcessor


class DuplicateDetector:
    """
    Detects potential duplicate incidents using fuzzy text matching.
    """
    
    @staticmethod
    def find_similar_incidents(title, description, platform, threshold=0.75, limit=5):
        """
        Find existing incidents similar to the provided text.
        
        Args:
            title (str): Incident title
            description (str): Incident description
            platform (str): Platform name (Additiv/Avaloq)
            threshold (float): Similarity threshold (0.0 to 1.0)
            limit (int): Maximum number of similar incidents to return
            
        Returns:
            list: List of tuples (Incident object, similarity_score)
        """
        # Combine title and description for comparison
        new_text = f"{title} {description}"
        
        # Get recent open incidents on same platform
        existing_incidents = Incident.query.filter_by(
            platform=platform,
            status='Open'
        ).order_by(Incident.created_at.desc()).limit(50).all()
        
        # Calculate similarity scores
        similar_incidents = []
        for incident in existing_incidents:
            existing_text = f"{incident.title} {incident.description}"
            
            similarity = TextProcessor.calculate_similarity(new_text, existing_text)
            
            if similarity >= threshold:
                similar_incidents.append((incident, similarity))
        
        # Sort by similarity (highest first) and limit results
        similar_incidents.sort(key=lambda x: x[1], reverse=True)
        return similar_incidents[:limit]
    
    @staticmethod
    def check_for_duplicates(title, description, platform, threshold=0.75):
        """
        Check if an incident is a potential duplicate.
        
        Args:
            title (str): Incident title
            description (str): Incident description
            platform (str): Platform name
            threshold (float): Similarity threshold
            
        Returns:
            dict: {
                'is_duplicate': bool,
                'similar_incidents': list of (Incident, score) tuples
            }
        """
        similar = DuplicateDetector.find_similar_incidents(
            title, description, platform, threshold
        )
        
        return {
            'is_duplicate': len(similar) > 0,
            'similar_incidents': similar
        }