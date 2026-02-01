#!/bin/bash

# FastAPI Backend Server Management Script
# This script helps manage the FastAPI backend server for testing

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PORT=8000
HOST="0.0.0.0"
APP_FILE="fastapi_app.py"
LOG_FILE="$SCRIPT_DIR/fastapi.log"

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}FastAPI Backend Server Management${NC}"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  start               Start the FastAPI server"
    echo "  start-dev           Start in development mode with auto-reload"
    echo "  start-background    Start server in background"
    echo "  stop                Stop the server running in background"
    echo "  status              Check if server is running"
    echo "  test-auth           Test basic authentication"
    echo "  logs                Show server logs (if running in background)"
    echo "  help                Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start-dev        # Start with auto-reload for development"
    echo "  $0 test-auth        # Test authentication endpoints"
    exit 1
}

# Function to check if port is in use
check_port() {
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start server
start_server() {
    echo -e "${BLUE}Starting FastAPI server...${NC}"
    
    if check_port; then
        echo -e "${YELLOW}⚠ Port $PORT is already in use${NC}"
        echo -e "${YELLOW}Run '$0 stop' to stop the existing server${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Starting server at http://$HOST:$PORT${NC}"
    echo -e "${GREEN}API documentation: http://localhost:$PORT/docs${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    
    cd "$SCRIPT_DIR"
    uvicorn fastapi_app:app --host $HOST --port $PORT
}

# Function to start server in development mode
start_dev() {
    echo -e "${BLUE}Starting FastAPI server in development mode...${NC}"
    
    if check_port; then
        echo -e "${YELLOW}⚠ Port $PORT is already in use${NC}"
        echo -e "${YELLOW}Run '$0 stop' to stop the existing server${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Starting server at http://$HOST:$PORT with auto-reload${NC}"
    echo -e "${GREEN}API documentation: http://localhost:$PORT/docs${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    
    cd "$SCRIPT_DIR"
    uvicorn fastapi_app:app --host $HOST --port $PORT --reload
}

# Function to start server in background
start_background() {
    echo -e "${BLUE}Starting FastAPI server in background...${NC}"
    
    if check_port; then
        echo -e "${YELLOW}⚠ Port $PORT is already in use${NC}"
        echo -e "${YELLOW}Server may already be running${NC}"
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
    nohup uvicorn fastapi_app:app --host $HOST --port $PORT > "$LOG_FILE" 2>&1 &
    
    sleep 2
    
    if check_port; then
        echo -e "${GREEN}✓ Server started successfully in background${NC}"
        echo -e "${GREEN}URL: http://localhost:$PORT${NC}"
        echo -e "${GREEN}Docs: http://localhost:$PORT/docs${NC}"
        echo -e "${YELLOW}Logs: $LOG_FILE${NC}"
        echo -e "${YELLOW}Run '$0 stop' to stop the server${NC}"
    else
        echo -e "${RED}✗ Failed to start server${NC}"
        echo -e "${YELLOW}Check $LOG_FILE for details${NC}"
        exit 1
    fi
}

# Function to stop server
stop_server() {
    echo -e "${BLUE}Stopping FastAPI server...${NC}"
    
    if ! check_port; then
        echo -e "${YELLOW}⚠ No server running on port $PORT${NC}"
        exit 0
    fi
    
    # Find and kill the process
    PID=$(lsof -ti:$PORT)
    
    if [ -n "$PID" ]; then
        kill $PID
        sleep 1
        
        if ! check_port; then
            echo -e "${GREEN}✓ Server stopped successfully${NC}"
        else
            echo -e "${RED}✗ Failed to stop server gracefully, trying force kill${NC}"
            kill -9 $PID
            sleep 1
            
            if ! check_port; then
                echo -e "${GREEN}✓ Server force stopped${NC}"
            else
                echo -e "${RED}✗ Failed to stop server${NC}"
                exit 1
            fi
        fi
    fi
}

# Function to check server status
check_status() {
    echo -e "${BLUE}Checking server status...${NC}"
    echo ""
    
    if check_port; then
        PID=$(lsof -ti:$PORT)
        echo -e "${GREEN}✓ Server is running${NC}"
        echo -e "  PID: $PID"
        echo -e "  Port: $PORT"
        echo -e "  URL: http://localhost:$PORT"
        echo -e "  Docs: http://localhost:$PORT/docs"
        echo ""
        
        # Try to reach the health endpoint
        if command -v curl &> /dev/null; then
            echo -e "${YELLOW}Testing health endpoint...${NC}"
            curl -s http://localhost:$PORT/health | python3 -m json.tool
        fi
    else
        echo -e "${RED}✗ Server is not running${NC}"
    fi
}

# Function to test authentication
test_auth() {
    echo -e "${BLUE}Testing Basic Authentication...${NC}"
    echo ""
    
    if ! check_port; then
        echo -e "${RED}✗ Server is not running${NC}"
        echo -e "${YELLOW}Run '$0 start' or '$0 start-background' first${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Testing with valid credentials (demo/demo123)...${NC}"
    curl -s -u demo:demo123 http://localhost:$PORT/api/v1/data | python3 -m json.tool
    echo ""
    
    echo -e "${YELLOW}Testing with invalid credentials...${NC}"
    curl -s -u wrong:wrong http://localhost:$PORT/api/v1/data | python3 -m json.tool
    echo ""
    
    echo -e "${GREEN}Authentication test complete${NC}"
    echo ""
    echo -e "${YELLOW}Valid test credentials:${NC}"
    echo -e "  Username: demo"
    echo -e "  Password: demo123"
    echo ""
    echo -e "  Username: admin"
    echo -e "  Password: admin123"
}

# Function to show logs
show_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}⚠ No log file found${NC}"
        echo -e "${YELLOW}Server may not be running in background mode${NC}"
        exit 0
    fi
    
    echo -e "${BLUE}Server logs:${NC}"
    echo ""
    tail -f "$LOG_FILE"
}

# Main script logic
case "$1" in
    start)
        start_server
        ;;
        
    start-dev)
        start_dev
        ;;
        
    start-background)
        start_background
        ;;
        
    stop)
        stop_server
        ;;
        
    status)
        check_status
        ;;
        
    test-auth)
        test_auth
        ;;
        
    logs)
        show_logs
        ;;
        
    help|--help|-h|"")
        usage
        ;;
        
    *)
        echo -e "${RED}Error: Invalid option '$1'${NC}"
        echo ""
        usage
        ;;
esac