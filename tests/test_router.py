"""
Test team routing algorithm.
Validates business logic for incident team assignment.
"""

import pytest
from app.utils.router import assign_team


def test_additiv_login_routes_to_lcm():
    """Test Additiv login issues route to LCM team."""
    team = assign_team(
        platform='Additiv',
        journey='Login',
        description='Users cannot authenticate'
    )
    assert team == 'LCM'


def test_avaloq_login_routes_to_lcm():
    """Test Avaloq login issues route to LCM team."""
    team = assign_team(
        platform='Avaloq',
        journey='Login',
        description='Authentication timeout'
    )
    assert team == 'LCM'


def test_additiv_data_sync_routes_to_devops():
    """Test Additiv data sync routes to DevOps."""
    team = assign_team(
        platform='Additiv',
        journey='Data Sync',
        description='Data synchronisation failure'
    )
    assert team == 'DevOps'


def test_avaloq_data_sync_routes_to_devops():
    """Test Avaloq data sync routes to DevOps."""
    team = assign_team(
        platform='Avaloq',
        journey='Data Sync',
        description='Sync process failing'
    )
    assert team == 'DevOps'


def test_additiv_payment_routes_to_devops():
    """Test Additiv payment issues route to DevOps."""
    team = assign_team(
        platform='Additiv',
        journey='Payment',
        description='Payment transaction timeout'
    )
    assert team == 'DevOps'


def test_additiv_api_keyword_routes_to_additiv_support():
    """Test API-related keywords route to Additiv Support."""
    team = assign_team(
        platform='Additiv',
        journey='Balance View',
        description='API endpoint returning 500 error'
    )
    assert team == 'Additiv Support'


def test_avaloq_database_keyword_routing():
    """Test database keywords routing for Avaloq."""
    team = assign_team(
        platform='Avaloq',
        journey='Transfer',
        description='Database query timeout affecting transfers'
    )
    assert team == 'DevOps'


def test_additiv_balance_view_routing():
    """Test Additiv balance view routing."""
    team = assign_team(
        platform='Additiv',
        journey='Balance View',
        description='Balance displaying incorrectly'
    )
    assert team == 'DevOps'


def test_additiv_transfer_routing():
    """Test Additiv transfer routing."""
    team = assign_team(
        platform='Additiv',
        journey='Transfer',
        description='Transfer confirmation not showing'
    )
    assert team == 'Additiv Support'


def test_routing_consistency():
    """Test routing logic is consistent for same inputs."""
    team1 = assign_team(
        platform='Additiv',
        journey='Login',
        description='Login failure'
    )
    
    team2 = assign_team(
        platform='Additiv',
        journey='Login',
        description='Login failure'
    )
    
    assert team1 == team2
    assert team1 == 'LCM'


def test_avaloq_routes_to_correct_teams():
    """Test Avaloq incidents route to appropriate teams."""
    login_team = assign_team(
        platform='Avaloq',
        journey='Login',
        description='Login issue'
    )
    
    data_sync_team = assign_team(
        platform='Avaloq',
        journey='Data Sync',
        description='Sync problem'
    )
    
    assert login_team == 'LCM'
    assert data_sync_team == 'DevOps'