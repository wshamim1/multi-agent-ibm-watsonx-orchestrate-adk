# Shared mock storage for ServiceNow incidents
# This module provides in-memory storage that can be imported by all ServiceNow tools

from datetime import datetime

# Global storage for mock incidents
MOCK_INCIDENTS = []
INCIDENT_COUNTER = 1000

def get_next_incident_number():
    """Generate the next incident number."""
    global INCIDENT_COUNTER
    incident_number = f"INC{INCIDENT_COUNTER:07d}"
    INCIDENT_COUNTER += 1
    return incident_number

def add_incident(incident_data):
    """Add a new incident to the mock storage."""
    MOCK_INCIDENTS.append(incident_data)
    return incident_data

def get_all_incidents():
    """Get all incidents from mock storage."""
    return MOCK_INCIDENTS.copy()

def get_incident_by_number(incident_number):
    """Get a specific incident by its number."""
    for incident in MOCK_INCIDENTS:
        if incident.get('incident_number') == incident_number:
            return incident
    return None