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

## Usage Patterns

### 🎯 Connection-Aware Tools (Recommended Starting Point)

If you need to integrate with external APIs requiring authentication:

**Path**: [connections/agents-tools/api-data-fetcher/](connections/agents-tools/api-data-fetcher/)

1. Start the backend server:
   ```bash
   cd connections/backend
   ./run_server.sh start
   # Server runs on http://localhost:8000
   ```

2. Import a connection template:
   ```bash
   orchestrate connections import -f connections/connections-types/basic-connections.yml
   orchestrate connections set-credentials -a basic-connection-app --env draft -u demo -p demo123
   ```

3. Import and deploy tools:
   ```bash
   cd connections/agents-tools/api-data-fetcher
   cat README.md  # Follow specific instructions
   ```

4. Test the integration:
   ```bash
   # Via API directly
   curl -u demo:demo123 http://localhost:8000/api/v1/data
   
   # Via agent in watsonx Orchestrate playground
   ```

---

### 🤝 Simple Native Agents

For learning agent basics without external APIs:

**Path**: [native-agents/greeter-agents/](native-agents/greeter-agents/)

```bash
cd native-agents/greeter-agents
./manage-greeter-systems.sh  # Follow prompts
```

No backend required - pure agent-to-agent and agent-to-tool interactions.

---

### 📚 Knowledge Base Integration

For document-backed conversational agents:

**Path**: [knowledge-bases/hr-assistant-agents-with-kb/](knowledge-bases/hr-assistant-agents-with-kb/)

```bash
cd knowledge-bases/hr-assistant-agents-with-kb
cat README.md  # Detailed setup instructions
```

Demonstrates:
- Document ingestion (company policies, handbooks)
- KB-backed agent queries
- Conversational document search

---

### 🌐 External Agent Systems

**Path**: [external-agents/](external-agents/)

```bash
cd external-agents
./manage-external-agent-system.sh
```

Shows supervisor patterns coordinating external agent systems.

---

### 🔌 MCP Integration

**Path**: [mcp-example/greeter-mcp/](mcp-example/greeter-mcp/)

Model Context Protocol server implementation:
```bash
cd mcp-example/greeter-mcp
cat README.md  # MCP setup instructions
```

---

### 🛠️ Customer Care Workflow

**Path**: [native-agents/product-customer_care/](native-agents/product-customer_care/)

Multi-agent customer support system with ServiceNow integration:
```bash
cd native-agents/product-customer_care
./manage_customer_care.sh
```

---

## All Connection Types

The [connections/connections-types/](connections/connections-types/) folder includes templates for:

| Auth Type | YAML File | Shell Script |
|-----------|-----------|--------------|
| Basic Auth | `basic-connections.yml` | `basic-connections.sh` |
| Bearer Token | `bearer-connections.yml` | `bearer-connections.sh` |
| API Key | `api-key-connections.yml` | `api-key-connections.sh` |
| Key-Value Headers | `key-value-connections.yml` | `key-value-connections.sh` |
| OAuth Authorization Code | `oauth-auth-code-connections.yml` | `oauth-auth-code-connections.sh` |
| OAuth Client Credentials | `oauth-client-credentials-connections.yml` | `oauth-client-credentials-connections.sh` |
| OAuth Password | `oauth-password-connections.yml` | `oauth-password-connections.sh` |
| SSO IdP Flow | `sso-idp-flow-connections.yml` | `sso-idp-flow-connections.sh` |
| SSO IdP Single Exchange | `sso-idp-single-exchange-connections.yml` | `sso-idp-single-exchange-connections.sh` |

Each pair includes:
- **YAML**: Import template for `orchestrate connections import`
- **Shell Script**: Helper script with CLI commands

---

## CLI Reference

See [WATSONX_ORCHESTRATE_CLI_CHEATSHEET.md](WATSONX_ORCHESTRATE_CLI_CHEATSHEET.md) for complete command reference covering:
- Environments
- Agents & Tools
- Connections
- Knowledge Bases
- Toolkits (MCP)
- Observability

---

## Prerequisites

```bash
# Install watsonx Orchestrate CLI
pip install --upgrade ibm-watsonx-orchestrate

# Configure environment
orchestrate env add -n my-env -u <your-watsonx-orchestrate-url>
orchestrate env activate my-env

# Optional: Python dependencies for FastAPI backend
cd connections/backend
pip install -r requirements.txt
```

---

## Testing the Backend

The [connections/backend/](connections/backend/) FastAPI server supports multiple auth methods:

```bash
# Start server
cd connections/backend
./run_server.sh start

# Test Basic Auth
curl -u demo:demo123 http://localhost:8000/api/v1/data

# Test Bearer Token
curl -H "Authorization: Bearer demo-token-456" http://localhost:8000/api/v1/data

# Test API Key
curl -H "x-api-key: demo-api-key" http://localhost:8000/api/v1/data

# Test Key-Value
curl -H "x-client-id: client-123" http://localhost:8000/api/v1/data

# Interactive API docs
open http://localhost:8000/docs
```

Run test suite:
```bash
cd connections/backend
python test_multi_auth.py
```

---

## Notes

- All backends use **mock data** for demonstration
- Replace demo credentials before production use
- Each example folder contains its own README with detailed instructions
- Connection templates require credential configuration via CLI

---

## Resources

- **IBM watsonx Orchestrate Documentation**: https://developer.watson-orchestrate.ibm.com/
- **CLI Cheatsheet**: [WATSONX_ORCHESTRATE_CLI_CHEATSHEET.md](WATSONX_ORCHESTRATE_CLI_CHEATSHEET.md)
- **Connection Guide**: [connections/agents-tools/api-data-fetcher/docs/](connections/agents-tools/api-data-fetcher/docs/)

---

## Support

For issues or feature requests, please open an issue in this repository.
