#!/bin/bash

# Customer Care Agent System Management Script
# This script helps manage the customer care agent system (e-commerce) in IBM watsonx Orchestrate

# Agent files
CUSTOMER_CARE_AGENT_FILE="agents/customer_care_agent.yaml"
SERVICE_NOW_AGENT_FILE="agents/service_now_agent.yaml"

# Tool files
PRODUCT_TOOLS_FILE="tools/customer_care/get_product_catalog.py"
ORDER_TOOLS_FILE="tools/customer_care/get_my_orders.py"
STORE_TOOLS_FILE="tools/customer_care/search_store_locations.py"
REVIEWS_TOOLS_FILE="tools/customer_care/get_product_reviews.py"
TRACKING_TOOLS_FILE="tools/customer_care/track_shipment.py"
AVAILABILITY_TOOLS_FILE="tools/customer_care/check_product_availability.py"
SHIPPING_TOOLS_FILE="tools/customer_care/calculate_shipping_cost.py"
SERVICENOW_CREATE_FILE="tools/servicenow/create_service_now_incident.py"
SERVICENOW_GET_ALL_FILE="tools/servicenow/get_my_service_now_incidents.py"
SERVICENOW_GET_BY_NUMBER_FILE="tools/servicenow/get_service_now_incident_by_number.py"
REQUIREMENTS_FILE="tools/requirements.txt"

# Agent names
CUSTOMER_CARE_AGENT_NAME="customer_care_agent"
SERVICE_NOW_AGENT_NAME="service_now_agent"

# Tool names
CUSTOMER_CARE_TOOLS=("get_product_catalog" "get_my_orders" "search_store_locations" "get_product_reviews" "track_shipment" "check_product_availability" "calculate_shipping_cost")
SERVICENOW_TOOLS=("create_service_now_incident" "get_my_service_now_incidents" "get_service_now_incident_by_number")

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}Customer Care Agent System Management Script${NC}"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  import-all          Import all tools and agents (customer care and ServiceNow)"
    echo "  import-tools        Import all tools (customer care and ServiceNow tools)"
    echo "  import-agents       Import all agents (customer care and ServiceNow)"
    echo "  deploy-all          Deploy all agents"
    echo "  undeploy-all        Undeploy all agents"
    echo "  remove-all          Remove all agents and tools"
    echo "  remove-tools        Remove all tools"
    echo "  remove-agents       Remove all agents"
    echo "  status              Show current status of all components"
    echo "  help                Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 import-all       # Import everything (tools and agents)"
    echo "  $0 deploy-all       # Deploy all agents"
    echo "  $0 remove-all       # Remove everything"
    exit 1
}

# Function to import customer care tools
import_customer_care_tools() {
    echo -e "${BLUE}Importing customer care tools...${NC}"
    
    echo -e "${YELLOW}Importing product catalog tool...${NC}"
    orchestrate tools import -k python -f "$PRODUCT_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Product catalog tool imported${NC}" || echo -e "${RED}✗ Failed to import product catalog tool${NC}"
    
    echo -e "${YELLOW}Importing order management tool...${NC}"
    orchestrate tools import -k python -f "$ORDER_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Order management tool imported${NC}" || echo -e "${RED}✗ Failed to import order management tool${NC}"
    
    echo -e "${YELLOW}Importing store location tool...${NC}"
    orchestrate tools import -k python -f "$STORE_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Store location tool imported${NC}" || echo -e "${RED}✗ Failed to import store location tool${NC}"
    
    echo -e "${YELLOW}Importing product reviews tool...${NC}"
    orchestrate tools import -k python -f "$REVIEWS_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Product reviews tool imported${NC}" || echo -e "${RED}✗ Failed to import product reviews tool${NC}"
    
    echo -e "${YELLOW}Importing shipment tracking tool...${NC}"
    orchestrate tools import -k python -f "$TRACKING_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Shipment tracking tool imported${NC}" || echo -e "${RED}✗ Failed to import shipment tracking tool${NC}"
    
    echo -e "${YELLOW}Importing product availability tool...${NC}"
    orchestrate tools import -k python -f "$AVAILABILITY_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Product availability tool imported${NC}" || echo -e "${RED}✗ Failed to import product availability tool${NC}"
    
    echo -e "${YELLOW}Importing shipping cost calculator tool...${NC}"
    orchestrate tools import -k python -f "$SHIPPING_TOOLS_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Shipping cost calculator tool imported${NC}" || echo -e "${RED}✗ Failed to import shipping cost calculator tool${NC}"
}

# Function to import ServiceNow tools
import_servicenow_tools() {
    echo -e "${BLUE}Importing ServiceNow tools (Mock Implementation)...${NC}"
    
    echo -e "${YELLOW}Importing create incident tool...${NC}"
    orchestrate tools import -k python -f "$SERVICENOW_CREATE_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Create incident tool imported${NC}" || echo -e "${RED}✗ Failed to import create incident tool${NC}"
    
    echo -e "${YELLOW}Importing get all incidents tool...${NC}"
    orchestrate tools import -k python -f "$SERVICENOW_GET_ALL_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Get all incidents tool imported${NC}" || echo -e "${RED}✗ Failed to import get all incidents tool${NC}"
    
    echo -e "${YELLOW}Importing get incident by number tool...${NC}"
    orchestrate tools import -k python -f "$SERVICENOW_GET_BY_NUMBER_FILE" -r "$REQUIREMENTS_FILE"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Get incident by number tool imported${NC}" || echo -e "${RED}✗ Failed to import get incident by number tool${NC}"
}

# Function to import customer care agent
import_customer_care_agent() {
    echo -e "${BLUE}Importing customer care agent...${NC}"
    orchestrate agents import -f "$CUSTOMER_CARE_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Customer care agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import customer care agent${NC}"
        return 1
    fi
}

# Function to import ServiceNow agent
import_servicenow_agent() {
    echo -e "${BLUE}Importing ServiceNow agent...${NC}"
    orchestrate agents import -f "$SERVICE_NOW_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ ServiceNow agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import ServiceNow agent${NC}"
        return 1
    fi
}

# Function to deploy all agents
deploy_all_agents() {
    echo -e "${BLUE}Deploying all agents...${NC}"
    
    echo -e "${YELLOW}Deploying ServiceNow agent...${NC}"
    orchestrate agents deploy --name "$SERVICE_NOW_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ ServiceNow agent deployed${NC}" || echo -e "${RED}✗ Failed to deploy ServiceNow agent${NC}"
    
    echo -e "${YELLOW}Deploying customer care agent...${NC}"
    orchestrate agents deploy --name "$CUSTOMER_CARE_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Customer care agent deployed${NC}" || echo -e "${RED}✗ Failed to deploy customer care agent${NC}"
}

# Function to undeploy all agents
undeploy_all_agents() {
    echo -e "${BLUE}Undeploying all agents...${NC}"
    
    echo -e "${YELLOW}Undeploying customer care agent...${NC}"
    orchestrate agents undeploy --name "$CUSTOMER_CARE_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Customer care agent undeployed${NC}" || echo -e "${RED}✗ Failed to undeploy customer care agent${NC}"
    
    echo -e "${YELLOW}Undeploying ServiceNow agent...${NC}"
    orchestrate agents undeploy --name "$SERVICE_NOW_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ ServiceNow agent undeployed${NC}" || echo -e "${RED}✗ Failed to undeploy ServiceNow agent${NC}"
}

# Function to remove all agents
remove_all_agents() {
    echo -e "${BLUE}Removing all agents...${NC}"
    
    echo -e "${YELLOW}Removing customer care agent...${NC}"
    orchestrate agents remove --name "$CUSTOMER_CARE_AGENT_NAME" --kind native
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Customer care agent removed${NC}" || echo -e "${RED}✗ Failed to remove customer care agent${NC}"
    
    echo -e "${YELLOW}Removing ServiceNow agent...${NC}"
    orchestrate agents remove --name "$SERVICE_NOW_AGENT_NAME" --kind native
    [ $? -eq 0 ] && echo -e "${GREEN}✓ ServiceNow agent removed${NC}" || echo -e "${RED}✗ Failed to remove ServiceNow agent${NC}"
}

# Function to remove all tools
remove_all_tools() {
    echo -e "${BLUE}Removing all tools...${NC}"
    
    for tool_name in "${CUSTOMER_CARE_TOOLS[@]}"; do
        echo -e "${YELLOW}Removing tool: $tool_name${NC}"
        orchestrate tools remove -n "$tool_name"
        [ $? -eq 0 ] && echo -e "${GREEN}✓ Tool '$tool_name' removed${NC}" || echo -e "${RED}✗ Failed to remove tool '$tool_name'${NC}"
    done
    
    for tool_name in "${SERVICENOW_TOOLS[@]}"; do
        echo -e "${YELLOW}Removing tool: $tool_name${NC}"
        orchestrate tools remove -n "$tool_name"
        [ $? -eq 0 ] && echo -e "${GREEN}✓ Tool '$tool_name' removed${NC}" || echo -e "${RED}✗ Failed to remove tool '$tool_name'${NC}"
    done
}

# Function to show status
show_status() {
    echo -e "${BLUE}=== Customer Care Agent System Status ===${NC}"
    echo ""
    echo -e "${YELLOW}Customer Care Tools:${NC}"
    for tool_name in "${CUSTOMER_CARE_TOOLS[@]}"; do
        orchestrate tools list | grep "$tool_name" || echo -e "${RED}Tool '$tool_name' not found${NC}"
    done
    echo ""
    echo -e "${YELLOW}ServiceNow Tools (Mock):${NC}"
    for tool_name in "${SERVICENOW_TOOLS[@]}"; do
        orchestrate tools list | grep "$tool_name" || echo -e "${RED}Tool '$tool_name' not found${NC}"
    done
    echo ""
    echo -e "${YELLOW}Agents:${NC}"
    orchestrate agents list | grep "$CUSTOMER_CARE_AGENT_NAME" || echo -e "${RED}Customer care agent not found${NC}"
    orchestrate agents list | grep "$SERVICE_NOW_AGENT_NAME" || echo -e "${RED}ServiceNow agent not found${NC}"
}

# Main script logic
case "$1" in
    import-all)
        echo -e "${BLUE}=== Importing All Tools and Agents ===${NC}"
        import_customer_care_tools
        echo ""
        import_servicenow_tools
        echo ""
        echo -e "${YELLOW}Note: Importing ServiceNow agent first (required as collaborator)${NC}"
        import_servicenow_agent
        echo ""
        import_customer_care_agent
        echo -e "${GREEN}=== Import Complete ===${NC}"
        echo ""
        echo -e "${YELLOW}Note: Remember to deploy the agents with: $0 deploy-all${NC}"
        ;;
    import-tools)
        echo -e "${BLUE}=== Importing All Tools ===${NC}"
        import_customer_care_tools
        echo ""
        import_servicenow_tools
        echo -e "${GREEN}=== Tools Import Complete ===${NC}"
        ;;
    import-agents)
        echo -e "${BLUE}=== Importing All Agents ===${NC}"
        echo -e "${YELLOW}Note: Importing ServiceNow agent first (required as collaborator)${NC}"
        import_servicenow_agent
        echo ""
        import_customer_care_agent
        echo -e "${GREEN}=== Agents Import Complete ===${NC}"
        ;;
    deploy-all)
        deploy_all_agents
        echo -e "${GREEN}=== Deployment Complete ===${NC}"
        ;;
    undeploy-all)
        undeploy_all_agents
        echo -e "${GREEN}=== Undeployment Complete ===${NC}"
        ;;
    remove-all)
        echo -e "${BLUE}=== Removing All Agents and Tools ===${NC}"
        undeploy_all_agents
        echo ""
        remove_all_agents
        echo ""
        remove_all_tools
        echo -e "${GREEN}=== Removal Complete ===${NC}"
        ;;
    remove-tools)
        remove_all_tools
        echo -e "${GREEN}=== Tools Removal Complete ===${NC}"
        ;;
    remove-agents)
        undeploy_all_agents
        echo ""
        remove_all_agents
        echo -e "${GREEN}=== Agents Removal Complete ===${NC}"
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo -e "${RED}Error: Invalid option '$1'${NC}"
        echo ""
        usage
        ;;
esac

exit 0