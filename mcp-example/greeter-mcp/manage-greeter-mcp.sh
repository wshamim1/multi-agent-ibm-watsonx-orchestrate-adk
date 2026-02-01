#!/bin/bash

# MCP Greeter Agent Management Script
# This script manages the MCP toolkit and agent for IBM watsonx Orchestrate

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TOOLKIT_NAME="greetme"
AGENT_NAME="greeterMCP"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$SCRIPT_DIR"
# Use absolute path to python and script
PYTHON_PATH="$(which python3)"
COMMAND="$PYTHON_PATH $SCRIPT_DIR/GreetingsServer.py"
APP_ID="mcp_greeter_app"
AGENT_FILE="$SCRIPT_DIR/greetermcp.yml"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

# Function to check if orchestrate CLI is available
check_orchestrate_cli() {
    if ! command -v orchestrate &> /dev/null; then
        print_error "orchestrate CLI not found. Please install IBM watsonx Orchestrate CLI first."
        exit 1
    fi
    print_success "orchestrate CLI found"
}

# Function to import MCP toolkit
import_toolkit() {
    print_header "Importing MCP Toolkit: $TOOLKIT_NAME"
    
    print_info "Importing toolkit with MCP kind..."
    print_info "Package root: $PACKAGE_ROOT"
    print_info "Command: $COMMAND"
    
    orchestrate toolkits add \
        --kind mcp \
        --name "$TOOLKIT_NAME" \
        --description "MCP toolkit that helps you greet users by name" \
        --package-root "$PACKAGE_ROOT" \
        --command "$COMMAND"
    
    if [ $? -eq 0 ]; then
        print_success "Toolkit '$TOOLKIT_NAME' imported successfully"
    else
        print_error "Failed to import toolkit '$TOOLKIT_NAME'"
        exit 1
    fi
}

# Function to list toolkits
list_toolkits() {
    print_header "Listing All Toolkits"
    orchestrate toolkits list
}

# Function to get toolkit details
get_toolkit() {
    print_header "Getting Toolkit Details: $TOOLKIT_NAME"
    orchestrate toolkits get --name "$TOOLKIT_NAME"
}

# Function to remove toolkit
remove_toolkit() {
    print_header "Removing MCP Toolkit: $TOOLKIT_NAME"
    
    print_warning "This will remove the toolkit '$TOOLKIT_NAME'"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        orchestrate toolkits remove --name "$TOOLKIT_NAME"
        if [ $? -eq 0 ]; then
            print_success "Toolkit '$TOOLKIT_NAME' removed successfully"
        else
            print_error "Failed to remove toolkit '$TOOLKIT_NAME'"
            exit 1
        fi
    else
        print_info "Toolkit removal cancelled"
    fi
}

# Function to import agent
import_agent() {
    print_header "Importing Agent: $AGENT_NAME"
    
    if [ ! -f "$AGENT_FILE" ]; then
        print_error "Agent file '$AGENT_FILE' not found"
        exit 1
    fi
    
    print_info "Importing agent from $AGENT_FILE..."
    orchestrate agents import -f "$AGENT_FILE"
    
    if [ $? -eq 0 ]; then
        print_success "Agent '$AGENT_NAME' imported successfully"
    else
        print_error "Failed to import agent '$AGENT_NAME'"
        exit 1
    fi
}

# Function to deploy agent
deploy_agent() {
    print_header "Deploying Agent: $AGENT_NAME"
    
    print_info "Deploying agent..."
    orchestrate agents deploy --name "$AGENT_NAME"
    
    if [ $? -eq 0 ]; then
        print_success "Agent '$AGENT_NAME' deployed successfully"
    else
        print_error "Failed to deploy agent '$AGENT_NAME'"
        exit 1
    fi
}

# Function to list agents
list_agents() {
    print_header "Listing All Agents"
    orchestrate agents list
}

# Function to get agent details
get_agent() {
    print_header "Getting Agent Details: $AGENT_NAME"
    orchestrate agents get --name "$AGENT_NAME"
}

# Function to remove agent
remove_agent() {
    print_header "Removing Agent: $AGENT_NAME"
    
    print_warning "This will remove the agent '$AGENT_NAME'"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        orchestrate agents remove --name "$AGENT_NAME" -k native
        if [ $? -eq 0 ]; then
            print_success "Agent '$AGENT_NAME' removed successfully"
        else
            print_error "Failed to remove agent '$AGENT_NAME'"
            exit 1
        fi
    else
        print_info "Agent removal cancelled"
    fi
}

# Function to deploy everything (toolkit + agent)
deploy_all() {
    print_header "Deploying Complete MCP Greeter System"
    
    print_info "Step 1/4: Checking orchestrate CLI..."
    check_orchestrate_cli
    
    print_info "Step 2/4: Importing MCP toolkit..."
    import_toolkit
    
    print_info "Step 3/4: Importing agent..."
    import_agent
    
    print_info "Step 4/4: Deploying agent..."
    deploy_agent
    
    print_success "Complete MCP Greeter system deployed successfully!"
    echo ""
    print_info "You can now use the agent in IBM watsonx Orchestrate"
}

# Function to remove everything
remove_all() {
    print_header "Removing Complete MCP Greeter System"
    
    print_warning "This will remove both the agent and toolkit"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing agent..."
        orchestrate agents remove --name "$AGENT_NAME" 2>/dev/null || print_warning "Agent not found or already removed"
        
        print_info "Removing toolkit..."
        orchestrate toolkits remove --name "$TOOLKIT_NAME" 2>/dev/null || print_warning "Toolkit not found or already removed"
        
        print_success "MCP Greeter system removed successfully"
    else
        print_info "Removal cancelled"
    fi
}

# Function to show status
show_status() {
    print_header "MCP Greeter System Status"
    
    print_info "Checking toolkit status..."
    if orchestrate toolkits get --name "$TOOLKIT_NAME" &> /dev/null; then
        print_success "Toolkit '$TOOLKIT_NAME' is registered"
    else
        print_warning "Toolkit '$TOOLKIT_NAME' is not registered"
    fi
    
    print_info "Checking agent status..."
    if orchestrate agents get --name "$AGENT_NAME" &> /dev/null; then
        print_success "Agent '$AGENT_NAME' is registered"
    else
        print_warning "Agent '$AGENT_NAME' is not registered"
    fi
}

# Function to test MCP server locally
test_server() {
    print_header "Testing MCP Server Locally"
    
    print_info "Starting MCP server..."
    print_warning "Press Ctrl+C to stop the server"
    echo ""
    
    cd "$PACKAGE_ROOT"
    python3 GreetingsServer.py
}

# Function to show usage
show_usage() {
    cat << EOF
${BLUE}MCP Greeter Agent Management Script${NC}

${GREEN}Usage:${NC}
    $0 <command>

${GREEN}Commands:${NC}

  ${YELLOW}Toolkit Commands:${NC}
    import-toolkit      Import the MCP toolkit
    list-toolkits       List all toolkits
    get-toolkit         Get toolkit details
    remove-toolkit      Remove the MCP toolkit

  ${YELLOW}Agent Commands:${NC}
    import-agent        Import the agent
    deploy-agent        Deploy the agent
    list-agents         List all agents
    get-agent           Get agent details
    remove-agent        Remove the agent

  ${YELLOW}System Commands:${NC}
    deploy              Deploy complete system (toolkit + agent)
    remove              Remove complete system
    status              Show system status
    test                Test MCP server locally

  ${YELLOW}Other:${NC}
    help                Show this help message

${GREEN}Examples:${NC}
    $0 deploy           # Deploy everything
    $0 status           # Check status
    $0 test             # Test server locally
    $0 remove           # Remove everything

${GREEN}Configuration:${NC}
    Toolkit Name:  $TOOLKIT_NAME
    Agent Name:    $AGENT_NAME
    Package Root:  $PACKAGE_ROOT
    Command:       $COMMAND
    App ID:        $APP_ID

EOF
}

# Main script logic
main() {
    case "${1:-}" in
        import-toolkit)
            check_orchestrate_cli
            import_toolkit
            ;;
        list-toolkits)
            check_orchestrate_cli
            list_toolkits
            ;;
        get-toolkit)
            check_orchestrate_cli
            get_toolkit
            ;;
        remove-toolkit)
            check_orchestrate_cli
            remove_toolkit
            ;;
        import-agent)
            check_orchestrate_cli
            import_agent
            ;;
        deploy-agent)
            check_orchestrate_cli
            deploy_agent
            ;;
        list-agents)
            check_orchestrate_cli
            list_agents
            ;;
        get-agent)
            check_orchestrate_cli
            get_agent
            ;;
        remove-agent)
            check_orchestrate_cli
            remove_agent
            ;;
        deploy)
            deploy_all
            ;;
        remove)
            check_orchestrate_cli
            remove_all
            ;;
        status)
            check_orchestrate_cli
            show_status
            ;;
        test)
            test_server
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            print_error "Unknown command: ${1:-}"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"

