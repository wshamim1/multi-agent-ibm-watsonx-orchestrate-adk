from typing import List, Optional

from pydantic import Field, BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Import shared mock storage
try:
    from mock_storage import get_all_incidents
except ImportError:
    # Fallback if import fails
    def get_all_incidents():
        return []

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
def get_my_service_now_incidents() -> List[ServiceNowIncident]:
    """
    Fetch all ServiceNow incidents that you created (Mock Implementation - No real ServiceNow connection required).

    Returns:
        The incident details including number, description, state, and urgency.
    """
    # Return incidents from mock storage, sorted by creation date (newest first)
    all_incidents = get_all_incidents()
    incidents = [ServiceNowIncident(**inc) for inc in all_incidents]
    incidents.sort(key=lambda o: o.created_on, reverse=True)
    
    # Return up to 10 most recent incidents
    return incidents[:min(len(incidents), 10)]