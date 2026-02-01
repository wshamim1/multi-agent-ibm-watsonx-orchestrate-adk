# API Data Fetcher with Basic Connections

Complete example of IBM Watsonx agents and tools that utilize **basic authentication connections** to fetch and process data from external APIs.

## 📁 Project Structure

```
api-data-fetcher/
├── agents/                     # Agent definitions
│   ├── data_fetcher_agent.yaml       # Handles API data retrieval
│   ├── data_processor_agent.yaml     # Processes fetched data
│   └── supervisor_agent.yaml         # Coordinates workflow
│
├── tools/                      # Tool implementations
│   └── data_fetcher_tools.py         # Python tools with connections
│
├── backend/                    # FastAPI backend server
│   ├── fastapi_app.py               # API application
│   ├── run_server.sh                # Server management script
│   └── test_api.py                  # API test suite
│
├── scripts/                    # Management scripts
│   └── manage_api_fetcher.sh        # Import/deploy agents
│
├── docs/                       # Documentation
│   ├── README.md                    # Detailed documentation
│   ├── FASTAPI_README.md            # Backend server guide
│   ├── CONNECTION_GUIDE.md          # Connection implementation guide
│   └── Example_prompts.md           # Usage examples
│
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend (Optional)

For a complete working example with a real API:

```bash
cd backend
./run_server.sh start-dev
```

The server starts at http://localhost:8000 with credentials:
- **Username**: `demo`
- **Password**: `demo123`

### 3. Configure Connection

```bash
cd ../../../connections

# Apply the connection
orchestrate connections apply -f basic-connections.yml

# Set credentials (for local server)
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u demo \
  -p demo123
```

**Note**: Update `server_url` in `basic-connections.yml` to `http://localhost:8000` for local testing.

### 4. Import and Deploy

```bash
cd ../native-agents/api-data-fetcher

# Import all tools and agents
./scripts/manage_api_fetcher.sh import-all

# Deploy agents
./scripts/manage_api_fetcher.sh deploy-all

# Check status
./scripts/manage_api_fetcher.sh status
```

## 📖 Documentation

- **[docs/README.md](docs/README.md)** - Complete usage guide and examples
- **[docs/FASTAPI_README.md](docs/FASTAPI_README.md)** - FastAPI backend documentation
- **[docs/CONNECTION_GUIDE.md](docs/CONNECTION_GUIDE.md)** - Connection implementation guide
- **[docs/Example_prompts.md](docs/Example_prompts.md)** - Example prompts for agents

## 🏗️ Architecture

```
User Request
     ↓
Supervisor Agent (Orchestrator)
     ↓
     ├─→ Data Fetcher Agent (uses basic auth)
     │        ↓
     │   Tools: fetch_api_data, fetch_user_info, search_api_data
     │        ↓
     │   FastAPI Backend (http://localhost:8000)
     │        ↓
     └─→ Data Processor Agent
              ↓
         Tools: process_api_response, format_data_report
              ↓
         Return formatted results
```

## 🛠️ Management Commands

### Agent Management

```bash
# From project root
./scripts/manage_api_fetcher.sh [command]

Commands:
  import-all          Import all tools and agents
  import-tools        Import only tools
  import-agents       Import only agents
  deploy-all          Deploy all agents
  undeploy-all        Undeploy all agents
  remove-all          Remove everything
  status              Show current status
  test-connection     Test basic auth connection
```

### Backend Server Management

```bash
# From backend directory
cd backend
./run_server.sh [command]

Commands:
  start               Start server in foreground
  start-dev           Start with auto-reload
  start-background    Start in background
  stop                Stop server
  status              Check server status
  test-auth           Test authentication
  logs                View server logs
```

## 🧪 Testing

### Test the API Backend

```bash
cd backend
./run_server.sh start-background
python test_api.py
```

### Test with Agents

```bash
# Start the server
cd backend
./run_server.sh start-background

# Deploy agents (if not already)
cd ..
./scripts/manage_api_fetcher.sh deploy-all

# Now interact with agents through Watsonx Orchestrate
```

## 💡 Example Usage

Once deployed, try these prompts:

```
Can you fetch user information for user ID 123?
```

```
Search for all products with status "active"
```

```
Get the dashboard metrics and show me a summary
```

```
Fetch data from /api/v1/orders and analyze the results
```

See [docs/Example_prompts.md](docs/Example_prompts.md) for more examples.

## 🔑 Key Features

- ✅ **Real Basic Authentication** - Uses IBM Watsonx connection framework
- ✅ **Complete Backend API** - FastAPI server with mock data
- ✅ **Multi-agent System** - Supervisor pattern with specialized agents
- ✅ **Production-ready Tools** - Proper error handling and authentication
- ✅ **Interactive API Docs** - Built-in Swagger UI at `/docs`
- ✅ **Comprehensive Testing** - Test suite included
- ✅ **Easy Management** - Scripts for all operations

## 📦 Components

### Agents

- **data_fetcher_agent** - Fetches data from authenticated APIs
- **data_processor_agent** - Processes and analyzes data
- **api_data_supervisor_agent** - Coordinates the workflow

### Tools

- `fetch_api_data` - GET/POST requests to API endpoints
- `fetch_user_info` - Retrieve user information
- `search_api_data` - Search with queries and filters
- `process_api_response` - Analyze API responses
- `format_data_report` - Format data as reports

### Backend API Endpoints

- `GET /api/v1/data` - General data
- `GET /api/v1/users/{id}` - User information
- `GET /api/v1/products` - Product catalog
- `GET /api/v1/search` - Search endpoint
- `GET /api/v1/dashboard` - Metrics
- And more...

## 🔧 Configuration

### Using Your Own API

1. Update connection in `../../../connections/basic-connections.yml`:
   ```yaml
   server_url: https://your-api.example.com
   ```

2. Set your credentials:
   ```bash
   orchestrate connections set-credentials -a basic-connection-app \
     --env draft \
     -u your_username \
     -p your_password
   ```

3. Modify tools if needed in `tools/data_fetcher_tools.py`

4. Re-import:
   ```bash
   ./scripts/manage_api_fetcher.sh import-tools
   ```

## 📚 Learning Resources

- [IBM Watsonx Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [Connection Types Reference](https://developer.watson-orchestrate.ibm.com/connections/associate_connection_to_tool/python_connections)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🐛 Troubleshooting

### Connection Issues

```bash
# Check connection status
./scripts/manage_api_fetcher.sh test-connection

# Re-set credentials
orchestrate connections set-credentials -a basic-connection-app \
  --env draft -u demo -p demo123
```

### Server Issues

```bash
# Check if server is running
cd backend
./run_server.sh status

# View logs
./run_server.sh logs

# Restart server
./run_server.sh stop
./run_server.sh start-dev
```

### Agent Issues

```bash
# Check agent status
./scripts/manage_api_fetcher.sh status

# View agent logs
orchestrate agents logs data_fetcher_agent

# Re-deploy
./scripts/manage_api_fetcher.sh undeploy-all
./scripts/manage_api_fetcher.sh deploy-all
```

## 📄 License

This is an example project for IBM Watsonx Orchestrate ADK.

---

For detailed documentation, see the [docs/](docs/) folder.
