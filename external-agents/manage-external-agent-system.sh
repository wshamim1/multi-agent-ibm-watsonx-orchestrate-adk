#!/bin/bash

# External Agent System Management Script
# This script manages the external agent and its supervisor in IBM watsonx Orchestrate

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
EXTERNAL_AGENT_FILE="external-agent/greeter_external_agent.yml"
SUPERVISOR_AGENT_FILE="external-agent/supervisor_agent.yml"
EXTERNAL_AGENT_NAME="langchain_greeter_agent"
SUPERVISOR_AGENT_NAME="external_agent_supervisor"

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

# Function to import external agent
import_external_agent() {
    print_header "Importing External Agent"
    
    if [ ! -f "$EXTERNAL_AGENT_FILE" ]; then
        print_error "External agent file '$EXTERNAL_AGENT_FILE' not found"
        exit 1
    fi
    
    print_info "Importing external agent from $EXTERNAL_AGENT_FILE..."
    orchestrate agents import -f "$EXTERNAL_AGENT_FILE"
    
    if [ $? -eq 0 ]; then
        print_success "External agent '$EXTERNAL_AGENT_NAME' imported successfully"
    else
        print_error "Failed to import external agent '$EXTERNAL_AGENT_NAME'"
        exit 1
    fi
}

# Function to import supervisor agent
import_supervisor_agent() {
    print_header "Importing Supervisor Agent"
    
    if [ ! -f "$SUPERVISOR_AGENT_FILE" ]; then
        print_error "Supervisor agent file '$SUPERVISOR_AGENT_FILE' not found"
        exit 1
    fi
    
    print_info "Importing supervisor agent from $SUPERVISOR_AGENT_FILE..."
    orchestrate agents import -f "$SUPERVISOR_AGENT_FILE"
    
    if [ $? -eq 0 ]; then
        print_success "Supervisor agent '$SUPERVISOR_AGENT_NAME' imported successfully"
    else
        print_error "Failed to import supervisor agent '$SUPERVISOR_AGENT_NAME'"
        exit 1
    fi
}

# Function to deploy external agent
deploy_external_agent() {
    print_header "Deploying External Agent"
    
    print_info "Deploying external agent..."
    orchestrate agents deploy --name "$EXTERNAL_AGENT_NAME"
    
    if [ $? -eq 0 ]; then
        print_success "External agent '$EXTERNAL_AGENT_NAME' deployed successfully"
    else
        print_error "Failed to deploy external agent '$EXTERNAL_AGENT_NAME'"
        exit 1
    fi
}

# Function to deploy supervisor agent
deploy_supervisor_agent() {
    print_header "Deploying Supervisor Agent"
    
    print_info "Deploying supervisor agent..."
    orchestrate agents deploy --name "$SUPERVISOR_AGENT_NAME"
    
    if [ $? -eq 0 ]; then
        print_success "Supervisor agent '$SUPERVISOR_AGENT_NAME' deployed successfully"
    else
        print_error "Failed to deploy supervisor agent '$SUPERVISOR_AGENT_NAME'"
        exit 1
    fi
}

# Function to deploy all agents
deploy_all_agents() {
    print_header "Deploying All Agents"
    
    print_info "Step 1/2: Deploying external agent..."
    deploy_external_agent
    
    print_info "Step 2/2: Deploying supervisor agent..."
    deploy_supervisor_agent
    
    print_success "All agents deployed successfully!"
}

# Function to undeploy all agents
undeploy_all_agents() {
    print_header "Undeploying All Agents"
    
    print_info "Undeploying supervisor agent..."
    orchestrate agents undeploy --name "$SUPERVISOR_AGENT_NAME" 2>/dev/null || print_warning "Supervisor agent not deployed"
    
    print_info "Undeploying external agent..."
    orchestrate agents undeploy --name "$EXTERNAL_AGENT_NAME" 2>/dev/null || print_warning "External agent not deployed"
    
    print_success "All agents undeployed"
}

# Function to remove all agents
remove_all_agents() {
    print_header "Removing All Agents"
    
    print_warning "This will remove both the supervisor and external agent"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing supervisor agent..."
        orchestrate agents remove --name "$SUPERVISOR_AGENT_NAME" --kind native 2>/dev/null || print_warning "Supervisor agent not found"
        
        print_info "Removing external agent..."
        orchestrate agents remove --name "$EXTERNAL_AGENT_NAME" --kind external 2>/dev/null || print_warning "External agent not found"
        
        print_success "All agents removed successfully"
    else
        print_info "Removal cancelled"
    fi
}

# Function to show status
show_status() {
    print_header "External Agent System Status"
    
    print_info "Checking external agent status..."
    if orchestrate agents get --name "$EXTERNAL_AGENT_NAME" &> /dev/null; then
        print_success "External agent '$EXTERNAL_AGENT_NAME' is registered"
    else
        print_warning "External agent '$EXTERNAL_AGENT_NAME' is not registered"
    fi
    
    print_info "Checking supervisor agent status..."
    if orchestrate agents get --name "$SUPERVISOR_AGENT_NAME" &> /dev/null; then
        print_success "Supervisor agent '$SUPERVISOR_AGENT_NAME' is registered"
    else
        print_warning "Supervisor agent '$SUPERVISOR_AGENT_NAME' is not registered"
    fi
}

# Function to show usage
show_usage() {
    cat << EOF
${BLUE}External Agent System Management Script${NC}

${GREEN}Usage:${NC}
    $0 <command>

${GREEN}Commands:${NC}

  ${YELLOW}Import Commands:${NC}
    import-all              Import both external and supervisor agents
    import-external         Import only the external agent
    import-supervisor       Import only the supervisor agent

  ${YELLOW}Deploy Commands:${NC}
    deploy-all              Deploy both agents
    deploy-external         Deploy only the external agent
    deploy-supervisor       Deploy only the supervisor agent

  ${YELLOW}Management Commands:${NC}
    undeploy-all            Undeploy both agents
    remove-all              Remove both agents
    status                  Show system status

  ${YELLOW}Other:${NC}
    help                    Show this help message

${GREEN}Examples:${NC}
    $0 import-all           # Import both agents
    $0 deploy-all           # Deploy both agents
    $0 status               # Check status
    $0 remove-all           # Remove everything

${GREEN}Workflow:${NC}
    1. Ensure external LangChain agent is running (localhost:5001)
    2. Import agents: $0 import-all
    3. Deploy agents: $0 deploy-all
    4. Test: orchestrate agents chat $SUPERVISOR_AGENT_NAME

${GREEN}Configuration:${NC}
    External Agent:  $EXTERNAL_AGENT_NAME
    Supervisor:      $SUPERVISOR_AGENT_NAME
    External URL:    https://localhost:5001/chat (update in YAML)

EOF
}

# Main script logic
main() {
    case "${1:-}" in
        import-all)
            check_orchestrate_cli
            import_external_agent
            echo ""
            import_supervisor_agent
            print_success "All agents imported successfully!"
            echo ""
            print_info "Next step: Deploy agents with: $0 deploy-all"
            ;;
        import-external)
            check_orchestrate_cli
            import_external_agent
            ;;
        import-supervisor)
            check_orchestrate_cli
            import_supervisor_agent
            ;;
        deploy-all)
            check_orchestrate_cli
            deploy_all_agents
            ;;
        deploy-external)
            check_orchestrate_cli
            deploy_external_agent
            ;;
        deploy-supervisor)
            check_orchestrate_cli
            deploy_supervisor_agent
            ;;
        undeploy-all)
            check_orchestrate_cli
            undeploy_all_agents
            ;;
        remove-all)
            check_orchestrate_cli
            remove_all_agents
            ;;
        status)
            check_orchestrate_cli
            show_status
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