#########################################
# Multi-Agent IBM watsonx Orchestrate ADK Demos
#########################################

This repository provides multiple working examples for IBM watsonx Orchestrate ADK, covering:

- Native multi-agent systems and supervisor patterns
- Tools integrated with IBM connection types (Basic, Bearer, API Key, Key-Value)
- Knowledge-base (KB) backed agents
- MCP-based agent and server examples
- External agent configurations
- Optional FastAPI backends for local testing

Use the folder that matches the pattern you want to learn or prototype.

---

## Repository Structure

```
connections/               # Connection templates (basic, bearer, api-key, key-value, oauth, sso)
external-agents/           # External agent examples
knowledge-bases/           # KB-backed agent examples
mcp-example/               # MCP example with greeter server
native-agents/             # Native agent systems
product-customer_care/     # Customer care multi-agent example
```

---

## Examples Included

- MCP example: [mcp-example/greeter-mcp/](mcp-example/greeter-mcp/)
  - Greeter MCP server and agent wiring
- External agents: [external-agents/](external-agents/)
  - External agent definitions and supervisor orchestration
- Knowledge bases: [knowledge-bases/](knowledge-bases/)
  - KB-backed agents (HR assistant example with documents)
- Native agent packs: [native-agents/](native-agents/)
  - Multiple agent/tool systems including greeter and weather examples
- Customer care system: [product-customer_care/](product-customer_care/)
  - Customer care agents and ServiceNow tools

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
