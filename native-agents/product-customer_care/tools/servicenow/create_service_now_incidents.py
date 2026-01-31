import json
from typing import Optional
from datetime import datetime

from pydantic import Field, BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Import shared mock storage
try:
    from mock_storage import get_next_incident_number, add_incident
except ImportError:
    # Fallback if import fails
    MOCK_INCIDENTS = []
    INCIDENT_COUNTER = 1000
    
    def get_next_incident_number():
        global INCIDENT_COUNTER
        incident_number = f"INC{INCIDENT_COUNTER:07d}"
        INCIDENT_COUNTER += 1
        return incident_number
    
    def add_incident(incident_data):
        MOCK_INCIDENTS.append(incident_data)
        return incident_data

class ServiceNowIncident(BaseModel):
    """
    Represents the details of a ServiceNow incident.
    """
    incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
    short_description: str = Field(..., description='A brief summary of the incident')
    description: Optional[str] = Field(None, description='Detailed information about the incident')
    state: str = Field(..., description='Current state of the incident')
    urgency: str = Field(..., description='Urgency level of the incident')
    created_on: str = Field(..., description='The date and time the incident was created')

@tool(permission=ToolPermission.READ_WRITE)
def create_service_now_incident(
        short_description: str,
        description: Optional[str] = None,
        urgency: Optional[int] = 3
):
    """
    Create a new ServiceNow incident (Mock Implementation - No real ServiceNow connection required).

    Args:
        short_description: A brief summary of the incident.
        description: Detailed information about the incident (optional).
        urgency: Urgency level (1 - High, 2 - Medium, 3 - Low, default is 3).

    Returns:
        The created incident details including incident number and system ID.
    """
    # Generate mock incident data
    incident_number = get_next_incident_number()
    
    urgency_map = {1: "High", 2: "Medium", 3: "Low"}
    urgency_value = urgency if urgency is not None else 3
    
    incident = {
        "incident_number": incident_number,
        "short_description": short_description,
        "description": description or "",
        "state": "New",
        "urgency": urgency_map.get(urgency_value, "Low"),
        "created_on": datetime.now().isoformat()
    }
    
    # Store in mock database
    add_incident(incident)
    
    return ServiceNowIncident(**incident).model_dump_json()