"""Test duplicate detection with actual incident data."""

from app import create_app
from app.utils.duplicate_detector import DuplicateDetector
from app.models.incident import Incident

# Create app context
app = create_app()

with app.app_context():
    # Get incident #5 from database
    incident5 = Incident.query.get(5)
    
    if incident5:
        print("=== Testing Incident #5 ===")
        print(f"Title: {incident5.title}")
        print(f"Description: {incident5.description}")
        print(f"Platform: {incident5.platform}\n")
        
        # Check for duplicates
        result = DuplicateDetector.check_for_duplicates(
            title=incident5.title,
            description=incident5.description,
            platform=incident5.platform,
            threshold=0.75
        )
        
        print(f"Is duplicate: {result['is_duplicate']}")
        print(f"Found {len(result['similar_incidents'])} similar incidents:\n")
        
        for incident, similarity in result['similar_incidents']:
            print(f"Incident #{incident.id}: {similarity:.2%} similar")
            print(f"  Title: {incident.title}")
            print(f"  Description: {incident.description}")
            print()
    else:
        print("Incident #5 not found!")
    
    # Also show all Additiv login incidents
    print("\n=== All Additiv Login Incidents ===")
    additiv_incidents = Incident.query.filter_by(
        platform='Additiv',
        journey='Login',
        status='Open'
    ).all()
    
    for inc in additiv_incidents:
        print(f"#{inc.id}: {inc.title}")
        print(f"  Desc: {inc.description}")
        print()