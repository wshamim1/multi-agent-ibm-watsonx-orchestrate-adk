# API Data Fetcher - Directory Structure

```
api-data-fetcher/
│
├── README.md                           # Quick start guide and overview
├── requirements.txt                    # Python dependencies
│
├── agents/                            # Agent YAML definitions
│   ├── data_fetcher_agent.yaml        # Fetches data with basic auth
│   ├── data_processor_agent.yaml      # Processes and analyzes data
│   └── supervisor_agent.yaml          # Coordinates workflow
│
├── tools/                             # Python tool implementations
│   └── data_fetcher_tools.py          # 5 tools with connection support
│
├── backend/                           # FastAPI backend server
│   ├── fastapi_app.py                 # API application with auth
│   ├── run_server.sh                  # Server management script
│   └── test_api.py                    # API test suite
│
├── scripts/                           # Management scripts
│   └── manage_api_fetcher.sh          # Import/deploy/remove agents
│
└── docs/                              # Documentation
    ├── README.md                      # Detailed usage guide
    ├── FASTAPI_README.md              # Backend server documentation
    ├── CONNECTION_GUIDE.md            # Connection implementation guide
    └── Example_prompts.md             # Example prompts for agents
```

## File Descriptions

### Root Level
- **README.md** - Quick start guide with project overview
- **requirements.txt** - All Python dependencies (orchestrate, fastapi, requests)

### `/agents/` - Agent Definitions
Three YAML files that define the watsonx agents:
- **data_fetcher_agent.yaml** - Agent that handles API calls with basic authentication
- **data_processor_agent.yaml** - Agent that processes and analyzes fetched data
- **supervisor_agent.yaml** - Orchestrator agent that coordinates the workflow

### `/tools/` - Tool Implementations
- **data_fetcher_tools.py** - Python file containing 5 tools:
  - `fetch_api_data()` - Fetch from API endpoints (uses basic auth)
  - `fetch_user_info()` - Get user information (uses basic auth)
  - `search_api_data()` - Search with filters (uses basic auth)
  - `process_api_response()` - Analyze API responses
  - `format_data_report()` - Format data as reports

### `/backend/` - FastAPI Backend Server
Complete backend API server for testing:
- **fastapi_app.py** - FastAPI application with:
  - Basic authentication middleware
  - 10+ REST endpoints
  - Mock data (users, products, orders)
  - Interactive API docs at `/docs`
  
- **run_server.sh** - Server management script with commands:
  - `start`, `start-dev`, `start-background`
  - `stop`, `status`, `test-auth`, `logs`

- **test_api.py** - Automated test suite that validates all endpoints

### `/scripts/` - Management Scripts
- **manage_api_fetcher.sh** - Main management script for:
  - Importing tools with connection binding
  - Importing agents
  - Deploying/undeploying agents
  - Checking status
  - Testing connections
  - Removing everything

### `/docs/` - Documentation
- **README.md** - Complete usage guide with:
  - Detailed setup instructions
  - Architecture diagrams
  - Usage examples
  - Troubleshooting guide
  
- **FASTAPI_README.md** - Backend server documentation:
  - API endpoint reference
  - Authentication guide
  - Testing instructions
  - Development tips

- **CONNECTION_GUIDE.md** - Connection implementation guide:
  - Step-by-step implementation
  - Code examples
  - Best practices
  - Troubleshooting

- **Example_prompts.md** - Collection of example prompts:
  - Basic queries
  - Complex workflows
  - Search operations
  - Real-world scenarios

## Quick Navigation

### Getting Started
1. Start here: [README.md](../README.md)
2. Backend setup: [docs/FASTAPI_README.md](FASTAPI_README.md)
3. Detailed guide: [docs/README.md](README.md)

### Development
- Tool code: [tools/data_fetcher_tools.py](../tools/data_fetcher_tools.py)
- Agent definitions: [agents/](../agents/)
- Connection guide: [docs/CONNECTION_GUIDE.md](CONNECTION_GUIDE.md)

### Operations
- Manage agents: [scripts/manage_api_fetcher.sh](../scripts/manage_api_fetcher.sh)
- Manage server: [backend/run_server.sh](../backend/run_server.sh)
- Test API: [backend/test_api.py](../backend/test_api.py)

## Common Commands

```bash
# From project root

# Backend
cd backend && ./run_server.sh start-dev

# Import and deploy
./scripts/manage_api_fetcher.sh import-all
./scripts/manage_api_fetcher.sh deploy-all

# Check status
./scripts/manage_api_fetcher.sh status

# Test
cd backend && python test_api.py
```

## Key Features by Component

### Agents
- ✅ Basic authentication support
- ✅ Multi-agent coordination
- ✅ Supervisor pattern
- ✅ Clear role separation

### Tools
- ✅ Connection-aware decorators
- ✅ Runtime credential fetching
- ✅ Error handling
- ✅ Type hints and documentation

### Backend
- ✅ FastAPI framework
- ✅ Basic auth middleware
- ✅ Mock data for testing
- ✅ Interactive docs (Swagger UI)
- ✅ CORS enabled

### Scripts
- ✅ One-command deployment
- ✅ Connection testing
- ✅ Status checking
- ✅ Clean removal

### Documentation
- ✅ Quick start guide
- ✅ Detailed examples
- ✅ API reference
- ✅ Troubleshooting tips
