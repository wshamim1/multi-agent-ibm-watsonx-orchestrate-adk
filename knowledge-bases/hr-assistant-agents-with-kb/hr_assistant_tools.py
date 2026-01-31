"""
Knowledge Base Tools for IBM watsonx Orchestrate ADK
These tools support agents that use knowledge bases for RAG (Retrieval-Augmented Generation)
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Optional
import datetime

@tool
def search_policy(query: str, policy_type: Optional[str] = None) -> str:
    """
    Search company policies and procedures.
    
    Args:
        query: The search query or question about policies
        policy_type: Optional filter (e.g., "remote_work", "expense", "benefits")
        
    Returns:
        Relevant policy information from the knowledge base
    """
    # The ADK automatically handles knowledge base search when the agent
    # has knowledge_bases configured. This tool provides a structured interface.
    
    result = f"Searching company policies for: {query}"
    if policy_type:
        result += f" (filtered by: {policy_type})"
    
    # In production, this would return actual search results from the knowledge base
    return result

@tool
def search_documentation(query: str, doc_type: Optional[str] = None) -> str:
    """
    Search product documentation, user guides, and technical resources.
    
    Args:
        query: The search query or technical question
        doc_type: Optional filter (e.g., "user_guide", "api", "troubleshooting")
        
    Returns:
        Relevant documentation from the knowledge base
    """
    result = f"Searching documentation for: {query}"
    if doc_type:
        result += f" (document type: {doc_type})"
    
    # In production, this would return actual search results from the knowledge base
    return result

@tool
def calculate_pto_balance(employee_id: str, year: Optional[int] = None) -> str:
    """
    Calculate an employee's PTO (Paid Time Off) balance.
    
    Args:
        employee_id: Employee identifier
        year: Year to calculate for (defaults to current year)
        
    Returns:
        PTO balance information
    """
    if year is None:
        year = datetime.datetime.now().year
    
    # Mock calculation - in production, this would query an HR system
    vacation_days = 15
    used_days = 5
    remaining_days = vacation_days - used_days
    
    return f"""PTO Balance for {year}:
- Total Vacation Days: {vacation_days}
- Days Used: {used_days}
- Days Remaining: {remaining_days}
- Sick Leave: 10 days (separate from vacation)
- Personal Days: 3 days

Note: According to company policy, vacation days must be used by December 31st.
Up to 5 days can be carried over to the next year with manager approval."""

@tool
def create_support_ticket(
    subject: str,
    description: str,
    priority: str = "medium",
    category: Optional[str] = None
) -> str:
    """
    Create a technical support ticket.
    
    Args:
        subject: Brief description of the issue
        description: Detailed description of the problem
        priority: Ticket priority (low, medium, high, critical)
        category: Issue category (e.g., "deployment", "database", "networking")
        
    Returns:
        Ticket ID and confirmation details
    """
    # Validate priority
    valid_priorities = ["low", "medium", "high", "critical"]
    if priority.lower() not in valid_priorities:
        return f"Error: Priority must be one of {valid_priorities}"
    
    # Generate ticket ID (in production, this would come from a ticketing system)
    ticket_id = f"TICKET-{abs(hash(subject)) % 10000:04d}"
    
    response_times = {
        "low": "24 hours",
        "medium": "8 hours",
        "high": "2 hours",
        "critical": "15 minutes"
    }
    
    result = f"""Support Ticket Created Successfully!

Ticket ID: {ticket_id}
Priority: {priority.upper()}
Expected Response Time: {response_times[priority.lower()]}
Status: Open

Subject: {subject}
Description: {description}"""
    
    if category:
        result += f"\nCategory: {category}"
    
    result += f"""

Next Steps:
1. You will receive an email confirmation at your registered email
2. Our support team will review your ticket
3. You can track ticket status at: https://support.acme.com/tickets/{ticket_id}
4. For urgent issues, call 1-800-ACME-HELP

Thank you for contacting ACME Support!"""
    
    return result

@tool
def check_system_status(service: Optional[str] = None) -> str:
    """
    Check the operational status of ACME Cloud Platform services.
    
    Args:
        service: Optional specific service to check (e.g., "compute", "database", "storage")
        
    Returns:
        Current system status information
    """
    # Mock status - in production, this would query a status API
    if service:
        return f"""Service Status: {service.upper()}

Status: ✅ Operational
Uptime: 99.99%
Last Incident: None in the past 30 days
Response Time: 45ms (average)

For detailed status, visit: https://status.acme.com"""
    
    return """ACME Cloud Platform - System Status

All Systems Operational ✅

Services:
- Compute: ✅ Operational
- Database: ✅ Operational  
- Storage: ✅ Operational
- Networking: ✅ Operational
- API: ✅ Operational

Current Performance:
- API Response Time: 45ms
- Global Uptime: 99.99%
- Active Incidents: 0

Last Updated: Just now
For real-time updates: https://status.acme.com"""

@tool
def get_api_documentation(endpoint: str) -> str:
    """
    Get documentation for a specific API endpoint.
    
    Args:
        endpoint: API endpoint path (e.g., "/compute/instances", "/databases")
        
    Returns:
        API documentation for the specified endpoint
    """
    # This would search the API documentation in the knowledge base
    return f"""Searching API documentation for endpoint: {endpoint}

The agent will search the knowledge base for detailed information about:
- Request/response format
- Authentication requirements
- Parameters and options
- Example requests
- Error codes

For complete API documentation, visit: https://docs.acme.com/api"""

@tool
def find_troubleshooting_guide(issue: str) -> str:
    """
    Find troubleshooting steps for a specific issue.
    
    Args:
        issue: Description of the problem or error
        
    Returns:
        Relevant troubleshooting steps from the knowledge base
    """
    return f"""Searching troubleshooting guides for: {issue}

The agent will search the knowledge base for:
- Common causes of this issue
- Step-by-step resolution steps
- Preventive measures
- Related documentation

If the issue persists after following troubleshooting steps, 
a support ticket can be created for further assistance."""

@tool
def check_policy_compliance(action: str, context: Optional[str] = None) -> str:
    """
    Check if an action complies with company policies.
    
    Args:
        action: The action to check (e.g., "expense claim", "remote work request")
        context: Additional context about the situation
        
    Returns:
        Policy compliance information
    """
    result = f"Checking policy compliance for: {action}"
    if context:
        result += f"\nContext: {context}"
    
    result += """

The agent will search company policies to determine:
- Whether the action is allowed
- Any requirements or restrictions
- Approval process needed
- Relevant policy sections

For specific questions, please consult with HR at hr@acme.com"""
    
    return result

