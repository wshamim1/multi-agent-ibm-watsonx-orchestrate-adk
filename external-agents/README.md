## System Flow Diagram

Below is a flow diagram illustrating the interaction from the Supervisor Agent to the External Agent and then to the LangChain Agents:

```mermaid
flowchart TD
    User[User Request]
    Supervisor[Supervisor Agent (Native)]
    External[External Agent (Container)]
    LangChain[LangChain Agent Service]

    User --> Supervisor
    Supervisor --> External
    External --> LangChain
    LangChain --> External
    External --> Supervisor
    Supervisor --> User
```


# External Agent with Supervisor

This directory demonstrates how to use external agents as collaborators in a multi-agent system with IBM watsonx Orchestrate.

## Overview

This example shows:
1. **External Agent** - A LangChain-based agent running as an external service
2. **Supervisor Agent** - A native agent that coordinates and delegates to the external agent

## Architecture

```
User Request
     ↓
Supervisor Agent (Native)
     ↓
External LangChain Agent (External Service)
     ↓
Response with Greeting + Weather
```

## Components

### 1. External Agent (`greeter_external_agent.yml`)
- **Type**: External agent
- **Name**: `langchain_greeter_agent`
- **Service**: LangChain agent with OpenAI GPT-4o-mini
- **Capabilities**: Personalized greetings with weather information
- **Endpoint**: `https://localhost:5001/chat` (configurable)

### 2. Supervisor Agent (`supervisor_agent.yml`)
- **Type**: Native agent
- **Name**: `external_agent_supervisor`
- **Model**: watsonx/meta-llama/llama-3-2-90b-vision-instruct
- **Role**: Coordinates requests and delegates to external agent
- **Collaborator**: Uses `langchain_greeter_agent` as collaborator

## Prerequisites

1. IBM watsonx Orchestrate CLI installed
2. External LangChain agent running (see `../langchain-agents/`)
3. watsonx API credentials configured

## Quick Start

### 1. Start External Agent

First, ensure the external LangChain agent is running:

```bash
cd ../langchain-agents
./deploy_podman.sh deploy
# Or run locally:
# python app.py
```

Verify it's running:
```bash
curl http://localhost:5001/health
```

### 2. Update External Agent URL

If your external agent is not on localhost, update the URL in `greeter_external_agent.yml`:

```yaml
api_url: "https://your-external-agent-url.com/chat"
```

### 3. Deploy the System

Use the management script:

```bash
# Import both agents
./manage_external_agent_system.sh import-all

# Deploy both agents
./manage_external_agent_system.sh deploy-all

# Check status
./manage_external_agent_system.sh status
```

### 4. Test the System

Chat with the supervisor agent:

```bash
orchestrate agents chat external_agent_supervisor
```

## Example Conversations

### Example 1: Simple Greeting
```
User: My name is John and I'm in New York

Supervisor: I'll get a personalized greeting for you with the current weather in New York.
[Delegates to external agent]

External Agent: Hey hi John, welcome to the Agent System! The weather in New York is sunny with a temperature of 72°F
```

### Example 2: Welcome Request
```
User: Can you welcome Sarah from San Francisco?

Supervisor: Of course! Let me create a welcome message for Sarah with San Francisco weather.
[Delegates to external agent]

External Agent: Hey hi Sarah, welcome to the Agent System! The weather in San Francisco is partly cloudy with a temperature of 68°F
```

### Example 3: Multiple Users
```
User: Greet Mike and tell him the weather in Chicago

Supervisor: I'll create a personalized greeting for Mike with Chicago's current weather.
[Delegates to external agent]

External Agent: Hey hi Mike, welcome to the Agent System! The weather in Chicago is cloudy with a temperature of 65°F
```

## Management Commands

### Import Agents
```bash
# Import both agents
./manage_external_agent_system.sh import-all

# Import only external agent
./manage_external_agent_system.sh import-external

# Import only supervisor
./manage_external_agent_system.sh import-supervisor
```

### Deploy Agents
```bash
# Deploy both agents
./manage_external_agent_system.sh deploy-all

# Deploy only external agent
./manage_external_agent_system.sh deploy-external

# Deploy only supervisor
./manage_external_agent_system.sh deploy-supervisor
```

### Manage Agents
```bash
# Check status
./manage_external_agent_system.sh status

# Undeploy all
./manage_external_agent_system.sh undeploy-all

# Remove all
./manage_external_agent_system.sh remove-all

# Show help
./manage_external_agent_system.sh help
```

## Configuration

## Deployment Instructions (External Agent in Containers)

To deploy the external agent in containers, use the following steps:

```sh
git clone https://github.com/wshamim1/deploy-ai-agent-using-containers
cd langchain-agents
```

The external agent acts as a collaborator in the multi-agent system.


# Full deployment
./deploy_podman.sh deploy



### External Agent Configuration


```yaml
spec_version: v1
kind: external
name: langchain_greeter_agent
api_url: "https://localhost:5001/chat"
auth_scheme: NONE  # or BEARER, BASIC, API_KEY
chat_params:
  stream: true
config:
  enable_cot: true  # Show chain of thought
```

### Supervisor Agent Configuration

```yaml
spec_version: v1
kind: native
name: external_agent_supervisor
llm:
  model_id: watsonx/meta-llama/llama-3-2-90b-vision-instruct
collaborators:
  - name: langchain_greeter_agent
    description: "External agent for greetings and weather"
```

## Authentication

If your external agent requires authentication, update the configuration:

### Bearer Token
```yaml
auth_scheme: BEARER
auth_config:
  token: "${EXTERNAL_AGENT_TOKEN}"
```

### API Key
```yaml
auth_scheme: API_KEY
auth_config:
  api_key: "${EXTERNAL_AGENT_API_KEY}"
  header_name: "X-API-Key"
```

### Basic Auth
```yaml
auth_scheme: BASIC
auth_config:
  username: "${EXTERNAL_AGENT_USER}"
  password: "${EXTERNAL_AGENT_PASSWORD}"
```

## Deployment Options

### Local Development
```bash
# Run external agent locally
cd ../langchain-agents
python app.py

# Use localhost URL
api_url: "http://localhost:5001/chat"
```

### Production with ngrok
```bash
# Expose local agent
ngrok http 5001

# Update URL in YAML
api_url: "https://your-ngrok-url.ngrok.io/chat"
```

### Container Deployment
```bash
# Deploy with Podman/Docker
cd ../langchain-agents
./deploy_podman.sh deploy

# Use container URL
api_url: "http://localhost:5001/chat"
```

## Troubleshooting

### External Agent Not Responding
```bash
# Check if external agent is running
curl http://localhost:5001/health

# Check logs
cd ../langchain-agents
./deploy_podman.sh logs
```

### Supervisor Can't Find External Agent
```bash
# Verify external agent is deployed
orchestrate agents list | grep langchain_greeter_agent

# Check agent status
orchestrate agents get --name langchain_greeter_agent
```

### Connection Errors
```bash
# Test external endpoint directly
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "test"}]}'

# Check firewall/network settings
# Ensure URL is accessible from watsonx Orchestrate
```

### Deployment Issues
```bash
# Remove and redeploy
./manage_external_agent_system.sh remove-all
./manage_external_agent_system.sh import-all
./manage_external_agent_system.sh deploy-all
```

## Best Practices

1. **Always deploy external agent first** - Ensure it's running before deploying supervisor
2. **Use environment variables** - For API keys and sensitive configuration
3. **Enable Chain of Thought** - Set `enable_cot: true` to see reasoning
4. **Test external endpoint** - Verify it's accessible before integration
5. **Monitor logs** - Check both external agent and supervisor logs
6. **Use proper authentication** - Don't expose external agents without auth in production
7. **Set timeouts** - Configure appropriate timeout values for external calls
8. **Handle errors gracefully** - External agent might be temporarily unavailable

## Use Cases

### 1. Legacy System Integration
Use external agents to integrate with existing systems without rewriting them.

### 2. Specialized Services
Delegate to external agents with specialized capabilities (ML models, APIs, etc.).

### 3. Multi-Cloud Deployments
Coordinate agents running in different cloud environments.

### 4. Microservices Architecture
Build agent systems using microservices pattern with external agents.

### 5. Third-Party Services
Integrate with third-party AI services as external agents.

## Related Examples

- **LangChain Agent**: `../langchain-agents/` - The external agent implementation
- **Native Multi-Agent**: `../Native-agents/greeter-agent/` - Native multi-agent system
- **MCP Agents**: `../mcp/` - Model Context Protocol agents

## Support

For issues or questions:
- Check the [main README](../README.md)
- Review [IBM watsonx Orchestrate Docs](https://www.ibm.com/docs/en/watsonx/watson-orchestrate)
- Visit [Developer Portal](https://developer.watson-orchestrate.ibm.com/)