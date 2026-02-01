#!/bin/bash

# API Data Fetcher Agent System Management Script
# This script helps manage the API data fetcher system in IBM watsonx Orchestrate

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

DATA_FETCHER_AGENT_FILE="$PROJECT_ROOT/agents/data_fetcher_agent.yaml"
DATA_PROCESSOR_AGENT_FILE="$PROJECT_ROOT/agents/data_processor_agent.yaml"
SUPERVISOR_AGENT_FILE="$PROJECT_ROOT/agents/supervisor_agent.yaml"
TOOLS_FILE="$PROJECT_ROOT/tools/data_fetcher_tools.py"

DATA_FETCHER_AGENT_NAME="data_fetcher_agent"
DATA_PROCESSOR_AGENT_NAME="data_processor_agent"
SUPERVISOR_AGENT_NAME="api_data_supervisor_agent"

# Tool names
TOOLS=("fetch_api_data" "fetch_user_info" "search_api_data" "process_api_response" "format_data_report")

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}API Data Fetcher Agent System Management Script${NC}"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  import-all          Import all tools and agents"
    echo "  import-tools        Import all tools"
    echo "  import-agents       Import all agents"
    echo "  deploy-all          Deploy all agents"
    echo "  undeploy-all        Undeploy all agents"
    echo "  remove-all          Remove all agents and tools"
    echo "  remove-tools        Remove all tools"
    echo "  remove-agents       Remove all agents"
    echo "  status              Show current status of all components"
    echo "  test-connection     Test the basic authentication connection"
    echo "  help                Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 import-all       # Import everything (tools and agents)"
    echo "  $0 deploy-all       # Deploy all agents"
    echo "  $0 remove-all       # Remove everything"
    exit 1
}

# Function to import tools
import_tools() {
    echo -e "${BLUE}Importing API data fetcher tools...${NC}"
    echo -e "${YELLOW}Note: Binding basic-connection-app to the tools${NC}"
    orchestrate tools import -k python -f "$TOOLS_FILE" -a basic-connection-app
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Tools imported successfully${NC}"
        echo -e "${GREEN}✓ Tools are now bound to basic-connection-app${NC}"
    else
        echo -e "${RED}✗ Failed to import tools${NC}"
        echo -e "${YELLOW}Make sure basic-connection-app is configured:${NC}"
        echo -e "  cd ../../connections"
        echo -e "  orchestrate connections apply -f basic-connections.yml"
        return 1
    fi
}

# Function to import data fetcher agent
import_data_fetcher_agent() {
    echo -e "${BLUE}Importing data fetcher agent...${NC}"
    orchestrate agents import -f "$DATA_FETCHER_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Data fetcher agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import data fetcher agent${NC}"
        return 1
    fi
}

# Function to import data processor agent
import_data_processor_agent() {
    echo -e "${BLUE}Importing data processor agent...${NC}"
    orchestrate agents import -f "$DATA_PROCESSOR_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Data processor agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import data processor agent${NC}"
        return 1
    fi
}

# Function to import supervisor agent
import_supervisor_agent() {
    echo -e "${BLUE}Importing supervisor agent...${NC}"
    orchestrate agents import -f "$SUPERVISOR_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Supervisor agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import supervisor agent${NC}"
        return 1
    fi
}

# Function to deploy agent
deploy_agent() {
    local agent_name=$1
    echo -e "${BLUE}Deploying $agent_name...${NC}"
    orchestrate agents deploy -a "$agent_name"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $agent_name deployed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to deploy $agent_name${NC}"
        return 1
    fi
}

# Function to undeploy agent
undeploy_agent() {
    local agent_name=$1
    echo -e "${BLUE}Undeploying $agent_name...${NC}"
    orchestrate agents undeploy -a "$agent_name"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $agent_name undeployed successfully${NC}"
    else
        echo -e "${YELLOW}⚠ $agent_name may not be deployed${NC}"
    fi
}

# Function to remove agent
remove_agent() {
    local agent_name=$1
    echo -e "${BLUE}Removing $agent_name...${NC}"
    orchestrate agents remove -a "$agent_name"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $agent_name removed successfully${NC}"
    else
        echo -e "${YELLOW}⚠ $agent_name may not exist${NC}"
    fi
}

# Function to remove tool
remove_tool() {
    local tool_name=$1
    echo -e "${BLUE}Removing tool: $tool_name...${NC}"
    orchestrate tools remove -t "$tool_name"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Tool $tool_name removed successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Tool $tool_name may not exist${NC}"
    fi
}

# Function to test connection
test_connection() {
    echo -e "${BLUE}Testing basic authentication connection...${NC}"
    echo -e "${YELLOW}Checking if basic-connection-app is configured...${NC}"
    
    orchestrate connections list | grep "basic-connection-app"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Connection found${NC}"
        echo ""
        echo -e "${YELLOW}Note: To set or update credentials, run:${NC}"
        echo -e "  orchestrate connections set-credentials -a basic-connection-app --env draft -u <username> -p <password>"
    else
        echo -e "${RED}✗ Connection not found${NC}"
        echo ""
        echo -e "${YELLOW}To set up the connection:${NC}"
        echo -e "  1. cd ../../../connections"
        echo -e "  2. orchestrate connections apply -f basic-connections.yml"
        echo -e "  3. orchestrate connections set-credentials -a basic-connection-app --env draft -u <username> -p <password>"
    fi
}

# Function to show status
show_status() {
    echo -e "${BLUE}=== API Data Fetcher System Status ===${NC}"
    echo ""
    
    echo -e "${YELLOW}Tools:${NC}"
    for tool in "${TOOLS[@]}"; do
        orchestrate tools list | grep -q "$tool"
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✓${NC} $tool"
        else
            echo -e "  ${RED}✗${NC} $tool"
        fi
    done
    
    echo ""
    echo -e "${YELLOW}Agents:${NC}"
    
    for agent in "$DATA_FETCHER_AGENT_NAME" "$DATA_PROCESSOR_AGENT_NAME" "$SUPERVISOR_AGENT_NAME"; do
        orchestrate agents list | grep -q "$agent"
        if [ $? -eq 0 ]; then
            # Check if deployed
            orchestrate agents list --deployed | grep -q "$agent"
            if [ $? -eq 0 ]; then
                echo -e "  ${GREEN}✓${NC} $agent ${GREEN}(deployed)${NC}"
            else
                echo -e "  ${YELLOW}○${NC} $agent (imported, not deployed)"
            fi
        else
            echo -e "  ${RED}✗${NC} $agent"
        fi
    done
    
    echo ""
    echo -e "${YELLOW}Connection:${NC}"
    orchestrate connections list | grep -q "basic-connection-app"
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}✓${NC} basic-connection-app"
    else
        echo -e "  ${RED}✗${NC} basic-connection-app (not configured)"
    fi
}

# Main script logic
case "$1" in
    import-all)
        echo -e "${BLUE}=== Importing All Components ===${NC}"
        echo ""
        import_tools
        echo ""
        import_data_fetcher_agent
        import_data_processor_agent
        import_supervisor_agent
        echo ""
        echo -e "${GREEN}✓ All components imported${NC}"
        echo -e "${YELLOW}Run '$0 deploy-all' to deploy the agents${NC}"
        ;;
        
    import-tools)
        import_tools
        ;;
        
    import-agents)
        echo -e "${BLUE}=== Importing Agents ===${NC}"
        echo ""
        import_data_fetcher_agent
        import_data_processor_agent
        import_supervisor_agent
        ;;
        
    deploy-all)
        echo -e "${BLUE}=== Deploying All Agents ===${NC}"
        echo ""
        deploy_agent "$DATA_FETCHER_AGENT_NAME"
        deploy_agent "$DATA_PROCESSOR_AGENT_NAME"
        deploy_agent "$SUPERVISOR_AGENT_NAME"
        echo ""
        echo -e "${GREEN}✓ All agents deployed${NC}"
        ;;
        
    undeploy-all)
        echo -e "${BLUE}=== Undeploying All Agents ===${NC}"
        echo ""
        undeploy_agent "$SUPERVISOR_AGENT_NAME"
        undeploy_agent "$DATA_PROCESSOR_AGENT_NAME"
        undeploy_agent "$DATA_FETCHER_AGENT_NAME"
        echo ""
        echo -e "${GREEN}✓ All agents undeployed${NC}"
        ;;
        
    remove-all)
        echo -e "${BLUE}=== Removing All Components ===${NC}"
        echo ""
        
        # Undeploy first
        undeploy_agent "$SUPERVISOR_AGENT_NAME"
        undeploy_agent "$DATA_PROCESSOR_AGENT_NAME"
        undeploy_agent "$DATA_FETCHER_AGENT_NAME"
        
        echo ""
        
        # Remove agents
        remove_agent "$SUPERVISOR_AGENT_NAME"
        remove_agent "$DATA_PROCESSOR_AGENT_NAME"
        remove_agent "$DATA_FETCHER_AGENT_NAME"
        
        echo ""
        
        # Remove tools
        for tool in "${TOOLS[@]}"; do
            remove_tool "$tool"
        done
        
        echo ""
        echo -e "${GREEN}✓ All components removed${NC}"
        ;;
        
    remove-tools)
        echo -e "${BLUE}=== Removing Tools ===${NC}"
        echo ""
        for tool in "${TOOLS[@]}"; do
            remove_tool "$tool"
        done
        ;;
        
    remove-agents)
        echo -e "${BLUE}=== Removing Agents ===${NC}"
        echo ""
        undeploy_agent "$SUPERVISOR_AGENT_NAME"
        undeploy_agent "$DATA_PROCESSOR_AGENT_NAME"
        undeploy_agent "$DATA_FETCHER_AGENT_NAME"
        
        echo ""
        
        remove_agent "$SUPERVISOR_AGENT_NAME"
        remove_agent "$DATA_PROCESSOR_AGENT_NAME"
        remove_agent "$DATA_FETCHER_AGENT_NAME"
        ;;
        
    status)
        show_status
        ;;
        
    test-connection)
        test_connection
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
