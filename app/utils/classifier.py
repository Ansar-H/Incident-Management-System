"""
Priority classification logic for incidents.
Uses rule-based approach to predict incident priority (High/Medium/Low).
"""


def predict_priority(platform, journey, clients_affected, description):
    """
    Predict incident priority based on business rules.
    
    Args:
        platform (str): Platform name (Additiv, Avaloq)
        journey (str): Customer journey affected
        clients_affected (int): Number of clients impacted
        description (str): Incident description text
    
    Returns:
        str: Priority level ('High', 'Medium', or 'Low')
    
    Business Rules:
    - HIGH: Multiple clients (>10) OR critical journey with multiple clients (>3)
    - MEDIUM: Critical journey OR 2-10 clients affected
    - LOW: Single client, non-critical journey
    """
    
    description_lower = description.lower()
    
    # Critical journeys that require immediate attention
    critical_journeys = ['Login', 'Transfer', 'Payment', 'Balance View', 'Account Access']
    
    # Keywords indicating high severity
    high_severity_keywords = ['error', 'timeout', 'crash', 'down', 'failure', 'unavailable']
    
    # HIGH PRIORITY: Multiple clients affected
    if clients_affected > 10:
        return 'High'
    
    # HIGH PRIORITY: Critical journey with multiple clients
    if journey in critical_journeys and clients_affected > 3:
        return 'High'
    
    # HIGH PRIORITY: Error keywords in description with multiple clients
    if any(keyword in description_lower for keyword in high_severity_keywords) and clients_affected > 5:
        return 'High'
    
    # MEDIUM PRIORITY: Critical journey (even single client)
    if journey in critical_journeys:
        return 'Medium'
    
    # MEDIUM PRIORITY: 2-10 clients affected
    if clients_affected >= 2:
        return 'Medium'
    
    # LOW PRIORITY: Everything else (single client, non-critical)
    return 'Low'