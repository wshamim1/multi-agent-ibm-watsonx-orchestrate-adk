#########################################
# Multi-Agent IBM watsonx Orchestrate ADK Examples
#########################################

This repository provides comprehensive working examples for IBM watsonx Orchestrate ADK, covering:

- **Connections**: All authentication types (Basic, Bearer, API Key, Key-Value, OAuth, SSO)
- **Native Agents**: Multi-agent systems with supervisor patterns
- **External Agents**: Integration with external agent systems
- **Knowledge Bases**: KB-backed agents with document retrieval
- **MCP Integration**: Model Context Protocol server examples
- **FastAPI Backend**: Multi-auth API server for testing and integration
- **Tools**: Python tools with connection bindings

---

## Repository Structure

```
├── connections/                      # Connection examples and backend
│   ├── connections-types/            # Templates for all auth types
│   │   ├── basic-connections.yml
│   │   ├── bearer-connections.yml
│   │   ├── api-key-connections.yml
│   │   ├── key-value-connections.yml
│   │   └── oauth-*.yml (multiple flows)
│   ├── agents-tools/                 # Connection-aware agents and tools
│   │   └── api-data-fetcher/         # Complete example system
│   ├── backend/                      # FastAPI multi-auth server
│   │   ├── fastapi_app.py            # Multi-auth API (4 methods)
│   │   ├── run_server.sh             # Server management
│   │   └── test_multi_auth.py        # Test suite
│   └── scripts/                      # Deployment scripts
│
├── native-agents/                    # Native agent systems
│   ├── greeter-agents/               # Simple greeter examples
│   └── product-customer_care/        # Customer care workflow
│
├── external-agents/                  # External agent examples
│   ├── greeter-external-agent.yml
│   └── greeter-supervisor-agent.yml
│
├── knowledge-bases/                  # KB-backed agents
│   ├── hr-assistant-agents-with-kb/  # HR assistant with documents
│   └── technical-support-agent-with-kb/
│
├── mcp-example/                      # MCP server examples
│   └── greeter-mcp/                  # Greeter MCP implementation
│
├── flow-builder/                     # Agentic workflow examples
│
└── WATSONX_ORCHESTRATE_CLI_CHEATSHEET.md  # Complete CLI reference
```

---

## Quick Start

### 1. Install Dependencies

```bash
# Install the ADK
pip install --upgrade ibm-watsonx-orchestrate

# For FastAPI backend
cd connections/backend
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend (Optional)

The backend demonstrates multi-authentication support:

```bash
cd connections/backend
./run_server.sh start

# Or manually:
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

The server supports:
- **Basic Auth**: `demo/demo123`
- **Bearer Token**: `demo-token-456`
- **API Key**: `demo-api-key` (via `x-api-key` header)
- **Key-Value**: `client-123` (via `x-client-id` header)

### 3. Configure Environment

```bash
# Add your watsonx Orchestrate environment
orchestrate env add -n my-env -u <your-instance-url>

# Activate it
orchestrate env activate my-env
```

### 4. Import Connections

```bash
# Example: Basic Auth connection
orchestrate connections import -f connections/connections-types/basic-connections.yml
orchestrate connections set-credentials -a basic-connection-app --env draft -u demo -p demo123
```

### 5. Import and Deploy Agents/Tools

```bash
# Navigate to an example
cd connections/agents-tools/api-data-fetcher

# See the README for specific instructions
cat README.md
```

---

## Examples Overview

### 🔗 Connections System (Featured)

**Location**: `connections/`

Complete connection examples with a **multi-authentication FastAPI backend**:

- **8 Authentication Types**: Basic, Bearer, API Key, Key-Value, OAuth (4 flows)
- **Working Backend**: FastAPI server with 4 auth methods
- **Test Scripts**: Comprehensive test suite for all auth types
- **Agent Integration**: Example agents and tools using connections

**Quick Test**:
```bash
cd connections/backend
./run_server.sh start

# Test different auth methods
curl -u demo:demo123 http://localhost:8000/api/v1/data
curl -H "Authorization: Bearer demo-token-456" http://localhost:8000/api/v1/data
curl -H "x-api-key: demo-api-key" http://localhost:8000/api/v1/data
curl -H "x-client-id: client-123" http://localhost:8000/api/v1/data
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### 🤖 Native Agents

**Locations**: `native-agents/`, `connections/agents-tools/`

- **Greeter System**: Simple hello world agents with tools
- **Customer Care**: Multi-agent customer support workflow
- **API Data Fetcher**: Complete system with connection-aware tools

### 🌐 External Agents

**Location**: `external-agents/`

Integration patterns for external agent systems with supervisor coordination.

### 📚 Knowledge Bases

**Location**: `knowledge-bases/`

- **HR Assistant**: Policy documents with conversational search
- **Technical Support**: KB-backed support agent

### 🔌 MCP Integration

**Location**: `mcp-example/greeter-mcp/`

Model Context Protocol server implementation examples.

### 🔄 Agentic Workflows

**Location**: `flow-builder/`

Complex multi-step workflow examples with agents and tools.

---

## How to Use This Repo

### 0) Clone the repository

```
git clone <your-repo-url>
cd multi-agent-ibm-watsonx-orchestrate-adk
```

### 1) Choose an example

Pick the folder that matches your goal:

- For MCP flows: [mcp-example/greeter-mcp/](mcp-example/greeter-mcp/)
- For KB agents: [knowledge-bases/](knowledge-bases/)
- For native agent systems: [native-agents/](native-agents/)
- For external agents: [external-agents/](external-agents/)
- For customer care workflows: [product-customer_care/](product-customer_care/)

### 2) Read the example docs

Most examples include their own README or docs. Start in the example folder:

- [native-agents/api-data-fetcher/](native-agents/api-data-fetcher/)
- [external-agents/README.md](external-agents/README.md)
- [mcp-example/greeter-mcp/README.md](mcp-example/greeter-mcp/README.md)

### 3) Configure connections

Connection templates are in [connections/](connections/). Bind them to your agents/tools via the Orchestrate CLI.

Common templates:

- [connections/basic-connections.yml](connections/basic-connections.yml)
- [connections/bearer-connections.yml](connections/bearer-connections.yml)
- [connections/api-key-connections.yml](connections/api-key-connections.yml)
- [connections/key-value-connections.yml](connections/key-value-connections.yml)

### 4) Import and deploy agents/tools

Each example includes a management script or instructions. For instance:

```
cd native-agents/api-data-fetcher
./scripts/manage_api_fetcher.sh import-all
./scripts/manage_api_fetcher.sh deploy-all
```

### 5) Run optional backends (if included)

Some examples provide local APIs (e.g., FastAPI). Follow their docs to start the backend.

---

## Example Highlight: api-data-fetcher

This is a full end-to-end system with agents, tools, a FastAPI backend, and test scripts.

Location: [native-agents/api-data-fetcher/](native-agents/api-data-fetcher/)

Key docs:

- [native-agents/api-data-fetcher/docs/CONNECTION_GUIDE.md](native-agents/api-data-fetcher/docs/CONNECTION_GUIDE.md)
- [native-agents/api-data-fetcher/docs/FASTAPI_README.md](native-agents/api-data-fetcher/docs/FASTAPI_README.md)
- [native-agents/api-data-fetcher/docs/Example_prompts.md](native-agents/api-data-fetcher/docs/Example_prompts.md)
- [native-agents/api-data-fetcher/docs/MULTI_AUTH_GUIDE.md](native-agents/api-data-fetcher/docs/MULTI_AUTH_GUIDE.md)

---

## Notes

- Some examples require the IBM watsonx Orchestrate CLI and SDK.
- Backends use mock data for testing unless otherwise noted.
- Replace demo credentials before using in real environments.

---

## Support

If you need additional examples or enhancements, open an issue or request changes.
