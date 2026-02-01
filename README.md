#+#+#+#+########################################
# Multi-Agent IBM watsonx Orchestrate ADK Demos
#+#+#+#+########################################

This repository contains working examples for IBM watsonx Orchestrate ADK, including:

- Native agent systems with supervisor patterns
- Tools wired to IBM connection types (Basic, Bearer, API Key, Key-Value)
- A FastAPI backend for testing multi-auth integrations
- Example knowledge-base and external agent setups

The most complete end-to-end example is **api-data-fetcher**, which includes agents, tools, a FastAPI backend, scripts, and docs.

---

## Repository Structure

```
connections/               # Connection templates (basic, bearer, api-key, key-value, oauth, sso)
external-agents/           # External agent examples
knowledge-bases/           # KB-backed agent examples
mcp-example/               # MCP example with greeter server
native-agents/             # Native agent systems
	api-data-fetcher/        # Full multi-auth example (agents + tools + backend)
product-customer_care/     # Customer care multi-agent example
```

---

## Quick Start (api-data-fetcher)

Path: `native-agents/api-data-fetcher`

### 1) Install backend dependencies

Use the requirements file in the backend folder:

```
cd native-agents/api-data-fetcher/backend
pip install -r requirements.txt
```

### 2) Start the FastAPI server

```
./run_server.sh start-dev
```

### 3) Test multi-auth

```
python test_multi_auth.py
```

The server supports **Basic Auth**, **Bearer Token**, **API Key**, and **Key-Value headers**. See the guide:

- `native-agents/api-data-fetcher/docs/MULTI_AUTH_GUIDE.md`

---

## Connections

Connection templates are stored in `connections/`. You can bind them to agents/tools using the Orchestrate CLI. Examples include:

- `basic-connections.yml`
- `bearer-connections.yml`
- `api-key-connections.yml`
- `key-value-connections.yml`

Use these to configure credentials that tools can access via the `connections` runtime API.

---

## Agents and Tools (api-data-fetcher)

Location: `native-agents/api-data-fetcher`

```
agents/      # data_fetcher_agent, data_processor_agent, supervisor_agent
tools/       # data_fetcher_tools.py with connection-aware tools
backend/     # FastAPI multi-auth API for local testing
scripts/     # manage_api_fetcher.sh for import/deploy
docs/        # guides and usage notes
```

Key docs:

- `docs/CONNECTION_GUIDE.md`
- `docs/FASTAPI_README.md`
- `docs/Example_prompts.md`
- `docs/MULTI_AUTH_GUIDE.md`

---

## Common Workflows

### Import and deploy agents/tools

```
cd native-agents/api-data-fetcher
./scripts/manage_api_fetcher.sh import-all
./scripts/manage_api_fetcher.sh deploy-all
```

### Stop the backend server

```
cd native-agents/api-data-fetcher/backend
./run_server.sh stop
```

---

## Notes

- The FastAPI server uses mock data for testing.
- Replace demo credentials before using in real environments.
- Some examples require the IBM watsonx Orchestrate CLI and SDK installed.

---

## Support

If you need additional examples or enhancements, open an issue or request changes.
