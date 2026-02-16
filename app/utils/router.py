"""
Team routing logic for incidents.
Assigns incidents to appropriate resolver teams based on platform and issue type.
"""


def assign_team(platform, journey, description):
    """
    Assign incident to appropriate resolver team.
    
    Args:
        platform (str): Platform name (Additiv, Avaloq)
        journey (str): Customer journey affected
        description (str): Incident description text
    
    Returns:
        str: Team name (LCM, DevOps, Additiv LCM, Avaloq Support, Platform Support)
    
    Routing Rules:
    - Authentication issues → LCM
    - Data sync issues → DevOps
    - Platform-specific errors → Platform vendor teams
    - Performance issues → DevOps
    """
    
    description_lower = description.lower()
    
    # Keyword-based routing
    auth_keywords = ['login', 'password', 'auth', 'authenticate', 'access', 'locked', 'sign in']
    data_keywords = ['sync', 'mismatch', 'data', 'balance', 'discrepancy', 'incorrect']
    performance_keywords = ['slow', 'timeout', 'crash', 'frozen', 'hang', 'performance']
    transaction_keywords = ['transfer', 'payment', 'transaction', 'send', 'withdraw']
    
    # Authentication issues → LCM
    if journey == 'Login' or any(keyword in description_lower for keyword in auth_keywords):
        return 'LCM'
    
    # Data synchronisation issues → DevOps
    if journey == 'Data Sync' or any(keyword in description_lower for keyword in data_keywords):
        return 'DevOps'
    
    # Performance issues → DevOps
    if any(keyword in description_lower for keyword in performance_keywords):
        return 'DevOps'
    
    # Platform-specific routing
    if platform == 'Additiv':
        # Transaction issues on Additiv
        if journey in ['Transfer', 'Payment'] or any(keyword in description_lower for keyword in transaction_keywords):
            return 'Additiv LCM'
        # Other Additiv issues
        return 'Additiv LCM'
    
    elif platform == 'Avaloq':
        # Transaction issues on Avaloq
        if journey in ['Transfer', 'Payment'] or any(keyword in description_lower for keyword in transaction_keywords):
            return 'Avaloq Support'
        # Balance/reporting issues on Avaloq
        if journey in ['Balance View', 'Reporting']:
            return 'LCM'
        # Other Avaloq issues
        return 'Avaloq Support'
    
    # Default fallback
    return 'Platform Support'