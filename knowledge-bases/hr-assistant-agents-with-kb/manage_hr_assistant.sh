#!/bin/bash

# HR Assistant Agent Management Script
# This script helps manage the HR assistant agent, its tools, and knowledge base in IBM watsonx Orchestrate

AGENT_FILE="Native-agents/hr-assistant-agent/hr_assistant_agent.yml"
TOOL_FILE="Native-agents/hr-assistant-agent/hr_assistant_tools.py"
KB_FILE="Native-agents/hr-assistant-agent/knowledge_bases/company_policies_kb.yml"
AGENT_NAME="hr_assistant_agent"
KB_NAME="company_policies_kb"

# Tool names from the hr_assistant_tools.py file
TOOL_NAMES=("search_policy" "calculate_pto_balance")

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}HR Assistant Agent Management Script${NC}"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  import-all          Import agent, tools, and knowledge base"
    echo "  import-agent        Import only the agent"
    echo "  import-tools        Import only the tools"
    echo "  import-kb           Import only the knowledge base"
    echo "  deploy              Deploy the agent"
    echo "  undeploy            Undeploy the agent"
    echo "  remove-all          Remove agent, tools, and knowledge base"
    echo "  remove-agent        Remove only the agent"
    echo "  remove-tools        Remove all tools individually"
    echo "  remove-kb           Remove the knowledge base"
    echo "  status              Show current status"
    echo "  help                Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 import-all       # Import everything (KB, tools, agent)"
    echo "  $0 deploy           # Deploy the agent"
    echo "  $0 remove-all       # Remove everything"
    exit 1
}

# Function to import knowledge base
import_kb() {
    echo -e "${BLUE}Importing knowledge base...${NC}"
    orchestrate knowledge-bases import -f "$KB_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Knowledge base imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import knowledge base${NC}"
        return 1
    fi
}

# Function to import tools
import_tools() {
    echo -e "${BLUE}Importing HR assistant tools...${NC}"
    orchestrate tools import -k python -f "$TOOL_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Tools imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import tools${NC}"
        return 1
    fi
}

# Function to import agent
import_agent() {
    echo -e "${BLUE}Importing HR assistant agent...${NC}"
    orchestrate agents import -f "$AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import agent${NC}"
        return 1
    fi
}

# Function to deploy agent
deploy_agent() {
    echo -e "${BLUE}Deploying HR assistant agent...${NC}"
    orchestrate agents deploy --name "$AGENT_NAME"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Agent deployed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to deploy agent${NC}"
        return 1
    fi
}

# Function to undeploy agent
undeploy_agent() {
    echo -e "${BLUE}Undeploying HR assistant agent...${NC}"
    orchestrate agents undeploy --name "$AGENT_NAME"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Agent undeployed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to undeploy agent${NC}"
        return 1
    fi
}

# Function to remove agent
remove_agent() {
    echo -e "${BLUE}Removing HR assistant agent...${NC}"
    orchestrate agents remove --name "$AGENT_NAME" --kind native
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Agent removed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to remove agent${NC}"
        return 1
    fi
}

# Function to remove all tools
remove_tools() {
    echo -e "${BLUE}Removing HR assistant tools...${NC}"
    for tool_name in "${TOOL_NAMES[@]}"; do
        echo -e "${YELLOW}Removing tool: $tool_name${NC}"
        orchestrate tools remove -n "$tool_name"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Tool '$tool_name' removed successfully${NC}"
        else
            echo -e "${RED}✗ Failed to remove tool '$tool_name'${NC}"
        fi
    done
}

# Function to remove knowledge base
remove_kb() {
    echo -e "${BLUE}Removing knowledge base...${NC}"
    orchestrate knowledge-bases remove --name "$KB_NAME"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Knowledge base removed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to remove knowledge base${NC}"
        return 1
    fi
}

# Function to show status
show_status() {
    echo -e "${BLUE}=== HR Assistant Agent Status ===${NC}"
    echo ""
    echo -e "${YELLOW}Checking knowledge base status...${NC}"
    orchestrate knowledge-bases list | grep "$KB_NAME" || echo -e "${RED}Knowledge base not found${NC}"
    echo ""
    echo -e "${YELLOW}Checking tools status...${NC}"
    for tool_name in "${TOOL_NAMES[@]}"; do
        orchestrate tools list | grep "$tool_name" || echo -e "${RED}Tool '$tool_name' not found${NC}"
    done
    echo ""
    echo -e "${YELLOW}Checking agent status...${NC}"
    orchestrate agents list | grep "$AGENT_NAME" || echo -e "${RED}Agent not found${NC}"
}

# Main script logic
case "$1" in
    import-all)
        echo -e "${BLUE}=== Importing Knowledge Base, Tools, and Agent ===${NC}"
        import_kb
        echo ""
        import_tools
        echo ""
        import_agent
        echo -e "${GREEN}=== Import Complete ===${NC}"
        echo ""
        echo -e "${YELLOW}Note: Remember to deploy the agent with: $0 deploy${NC}"
        ;;
    import-kb)
        import_kb
        ;;
    import-tools)
        import_tools
        ;;
    import-agent)
        import_agent
        ;;
    deploy)
        deploy_agent
        ;;
    undeploy)
        undeploy_agent
        ;;
    remove-all)
        echo -e "${BLUE}=== Removing Agent, Tools, and Knowledge Base ===${NC}"
        undeploy_agent
        echo ""
        remove_agent
        echo ""
        remove_tools
        echo ""
        remove_kb
        echo -e "${GREEN}=== Removal Complete ===${NC}"
        ;;
    remove-agent)
        undeploy_agent
        remove_agent
        ;;
    remove-tools)
        remove_tools
        ;;
    remove-kb)
        remove_kb
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
