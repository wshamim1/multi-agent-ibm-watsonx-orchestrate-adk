#!/bin/bash

# Greeter Agent System Management Script
# This script helps manage the greeter agent system (weather agent, greeter agent, and supervisor) in IBM watsonx Orchestrate

WEATHER_AGENT_FILE="weather_agent.yml"
GREETER_AGENT_FILE="greeter_agent.yml"
SUPERVISOR_AGENT_FILE="greeter_supervisor_agent.yml"
WEATHER_TOOLS_FILE="weather_tools.py"
GREETER_TOOLS_FILE="greeter_tools.py"

WEATHER_AGENT_NAME="weather_agent"
GREETER_AGENT_NAME="greeter_agent"
SUPERVISOR_AGENT_NAME="greeter_supervisor_agent"

# Tool names
WEATHER_TOOLS=("get_weather" "get_forecast")
GREETER_TOOLS=("create_greeting" "format_greeting_with_weather")

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}Greeter Agent System Management Script${NC}"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  import-all          Import all tools and agents (weather, greeter, supervisor)"
    echo "  import-tools        Import all tools (weather and greeter tools)"
    echo "  import-agents       Import all agents (weather, greeter, supervisor)"
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

# Function to import weather tools
import_weather_tools() {
    echo -e "${BLUE}Importing weather tools...${NC}"
    orchestrate tools import -k python -f "$WEATHER_TOOLS_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Weather tools imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import weather tools${NC}"
        return 1
    fi
}

# Function to import greeter tools
import_greeter_tools() {
    echo -e "${BLUE}Importing greeter tools...${NC}"
    orchestrate tools import -k python -f "$GREETER_TOOLS_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Greeter tools imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import greeter tools${NC}"
        return 1
    fi
}

# Function to import weather agent
import_weather_agent() {
    echo -e "${BLUE}Importing weather agent...${NC}"
    orchestrate agents import -f "$WEATHER_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Weather agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import weather agent${NC}"
        return 1
    fi
}

# Function to import greeter agent
import_greeter_agent() {
    echo -e "${BLUE}Importing greeter agent...${NC}"
    orchestrate agents import -f "$GREETER_AGENT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Greeter agent imported successfully${NC}"
    else
        echo -e "${RED}✗ Failed to import greeter agent${NC}"
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

# Function to deploy all agents
deploy_all_agents() {
    echo -e "${BLUE}Deploying all agents...${NC}"
    
    echo -e "${YELLOW}Deploying weather agent...${NC}"
    orchestrate agents deploy --name "$WEATHER_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Weather agent deployed${NC}" || echo -e "${RED}✗ Failed to deploy weather agent${NC}"
    
    echo -e "${YELLOW}Deploying greeter agent...${NC}"
    orchestrate agents deploy --name "$GREETER_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Greeter agent deployed${NC}" || echo -e "${RED}✗ Failed to deploy greeter agent${NC}"
    
    echo -e "${YELLOW}Deploying supervisor agent...${NC}"
    orchestrate agents deploy --name "$SUPERVISOR_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Supervisor agent deployed${NC}" || echo -e "${RED}✗ Failed to deploy supervisor agent${NC}"
}

# Function to undeploy all agents
undeploy_all_agents() {
    echo -e "${BLUE}Undeploying all agents...${NC}"
    
    echo -e "${YELLOW}Undeploying supervisor agent...${NC}"
    orchestrate agents undeploy --name "$SUPERVISOR_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Supervisor agent undeployed${NC}" || echo -e "${RED}✗ Failed to undeploy supervisor agent${NC}"
    
    echo -e "${YELLOW}Undeploying greeter agent...${NC}"
    orchestrate agents undeploy --name "$GREETER_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Greeter agent undeployed${NC}" || echo -e "${RED}✗ Failed to undeploy greeter agent${NC}"
    
    echo -e "${YELLOW}Undeploying weather agent...${NC}"
    orchestrate agents undeploy --name "$WEATHER_AGENT_NAME"
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Weather agent undeployed${NC}" || echo -e "${RED}✗ Failed to undeploy weather agent${NC}"
}

# Function to remove all agents
remove_all_agents() {
    echo -e "${BLUE}Removing all agents...${NC}"
    
    echo -e "${YELLOW}Removing supervisor agent...${NC}"
    orchestrate agents remove --name "$SUPERVISOR_AGENT_NAME" --kind native
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Supervisor agent removed${NC}" || echo -e "${RED}✗ Failed to remove supervisor agent${NC}"
    
    echo -e "${YELLOW}Removing greeter agent...${NC}"
    orchestrate agents remove --name "$GREETER_AGENT_NAME" --kind native
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Greeter agent removed${NC}" || echo -e "${RED}✗ Failed to remove greeter agent${NC}"
    
    echo -e "${YELLOW}Removing weather agent...${NC}"
    orchestrate agents remove --name "$WEATHER_AGENT_NAME" --kind native
    [ $? -eq 0 ] && echo -e "${GREEN}✓ Weather agent removed${NC}" || echo -e "${RED}✗ Failed to remove weather agent${NC}"
}

# Function to remove all tools
remove_all_tools() {
    echo -e "${BLUE}Removing all tools...${NC}"
    
    for tool_name in "${WEATHER_TOOLS[@]}"; do
        echo -e "${YELLOW}Removing tool: $tool_name${NC}"
        orchestrate tools remove -n "$tool_name"
        [ $? -eq 0 ] && echo -e "${GREEN}✓ Tool '$tool_name' removed${NC}" || echo -e "${RED}✗ Failed to remove tool '$tool_name'${NC}"
    done
    
    for tool_name in "${GREETER_TOOLS[@]}"; do
        echo -e "${YELLOW}Removing tool: $tool_name${NC}"
        orchestrate tools remove -n "$tool_name"
        [ $? -eq 0 ] && echo -e "${GREEN}✓ Tool '$tool_name' removed${NC}" || echo -e "${RED}✗ Failed to remove tool '$tool_name'${NC}"
    done
}

# Function to show status
show_status() {
    echo -e "${BLUE}=== Greeter Agent System Status ===${NC}"
    echo ""
    echo -e "${YELLOW}Weather Tools:${NC}"
    for tool_name in "${WEATHER_TOOLS[@]}"; do
        orchestrate tools list | grep "$tool_name" || echo -e "${RED}Tool '$tool_name' not found${NC}"
    done
    echo ""
    echo -e "${YELLOW}Greeter Tools:${NC}"
    for tool_name in "${GREETER_TOOLS[@]}"; do
        orchestrate tools list | grep "$tool_name" || echo -e "${RED}Tool '$tool_name' not found${NC}"
    done
    echo ""
    echo -e "${YELLOW}Agents:${NC}"
    orchestrate agents list | grep "$WEATHER_AGENT_NAME" || echo -e "${RED}Weather agent not found${NC}"
    orchestrate agents list | grep "$GREETER_AGENT_NAME" || echo -e "${RED}Greeter agent not found${NC}"
    orchestrate agents list | grep "$SUPERVISOR_AGENT_NAME" || echo -e "${RED}Supervisor agent not found${NC}"
}

# Main script logic
case "$1" in
    import-all)
        echo -e "${BLUE}=== Importing All Tools and Agents ===${NC}"
        import_weather_tools
        echo ""
        import_greeter_tools
        echo ""
        import_weather_agent
        echo ""
        import_greeter_agent
        echo ""
        import_supervisor_agent
        echo -e "${GREEN}=== Import Complete ===${NC}"
        echo ""
        echo -e "${YELLOW}Note: Remember to deploy the agents with: $0 deploy-all${NC}"
        ;;
    import-tools)
        echo -e "${BLUE}=== Importing All Tools ===${NC}"
        import_weather_tools
        echo ""
        import_greeter_tools
        echo -e "${GREEN}=== Tools Import Complete ===${NC}"
        ;;
    import-agents)
        echo -e "${BLUE}=== Importing All Agents ===${NC}"
        import_weather_agent
        echo ""
        import_greeter_agent
        echo ""
        import_supervisor_agent
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

