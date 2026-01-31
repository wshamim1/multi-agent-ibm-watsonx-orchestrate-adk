from typing import Optional

from pydantic import Field, BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Import shared mock storage
try:
    from mock_storage import get_incident_by_number
except ImportError:
    # Fallback if import fails
    def get_incident_by_number(incident_number):
        return None

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

@tool
def get_service_now_incident_by_number(incident_number: str):
    """
    Fetch a ServiceNow incident by its incident number (Mock Implementation - No real ServiceNow connection required).

    Args:
        incident_number: The uniquely identifying incident number of the ticket.

    Returns:
        The incident details including number, description, state, and urgency.
    """
    # Search for the incident in mock storage
    incident = get_incident_by_number(incident_number)
    
    if incident:
        return ServiceNowIncident(**incident).model_dump_json()
    
    # If not found, return an error message
    return f"Incident {incident_number} not found"