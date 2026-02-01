#########################################
# IBM watsonx Orchestrate ADK CLI Cheatsheet
#########################################

Source: https://developer.watson-orchestrate.ibm.com/

---

## Install ADK

```
pip install --upgrade ibm-watsonx-orchestrate
```

---

## Environments

### Add environment
```
orchestrate env add -n <environment-name> -u <your-instance-url>
```

### Add on-prem with IAM URL
```
orchestrate env add -n <onprem-environment-name> --iam-url https://api.us-east-1-reg.watson-orchestrate.ibm.com -u <watsonxorchestrateinstance>
```

### Add on-prem (self-signed cert)
```
orchestrate env add -n <onprem-environment-name> -u <your-instance-url> --insecure
```

### Activate environment (interactive)
```
orchestrate env activate <environment-name>
```

### Activate environment (non-interactive)
```
orchestrate env activate <environment-name> --api-key <your-api-key>
```

### Activate on-prem
```
orchestrate env activate <onprem-environment-name> --username=<username> --password=<password>
```

### Activate on-prem with API key
```
orchestrate env activate <onprem-environment-name> --username=<username> --api-key=<api-key>
```

### List environments
```
orchestrate env list
```

### Remove environment
```
orchestrate env remove -n <environment-name>
```

---

## Agents

### Import agent from file
```
orchestrate agents import -f <path to .yaml/.json/.py file>
```

### Create agent via CLI
```
orchestrate agents create \
	--name agent_name \
	--kind native \
	--description "Sample agent description" \
	--llm watsonx/ibm/granite-3-8b-instruct \
	--style default \
	--collaborators agent_1 \
	--tools tool_1 \
	--output "agent_name.agent.yaml"
```

### Deploy / undeploy
```
orchestrate agents deploy --name agent_name
orchestrate agents undeploy --name agent_name
```

### List agents
```
orchestrate agents list -v
```

### Export agent
```
orchestrate agents export -n <agent-name> -k <agent-type> -o <output-path>.zip
```

### Update agent
```
orchestrate agents import -f <path to agent file that you want to update>
```

### Remove agent
```
orchestrate agents remove --name my-agent --kind native
```

### Chat with agent (CLI)
```
orchestrate chat ask --agent-name <agent_name>
orchestrate chat ask --agent-name <agent_name> "What is the weather?"
orchestrate chat ask --agent-name <agent_name> "What is the weather?" --include-reasoning
```

---

## Tools

### Import Python tool
```
orchestrate tools import -k python -f my-tool.py -r requirements.txt -a app1 -a app2
```

### Import OpenAPI tool
```
orchestrate tools import -k openapi -f <file-path> -a <app-id>
```

### Import Langflow tool (by name)
```
orchestrate tools import -k langflow -n <langflow-flow-name>
```

### Import Langflow tool (by JSON file)
```
orchestrate tools import -k langflow -f <json-file-path> -a <app-id> -<requirements-file-path>
```

### Auto-discover Python tools
```
orchestrate tools auto-discover --file path\to\python\file --output path\to\output\file --env-file .env --llm groq/gpt-oss-120b --function-names name_of_function1 --function-names name_of_function2
```

### List tools
```
orchestrate tools list -v
```

### Export tools
```
orchestrate tools export -n <tool-name> -o <zip-output-path>
```

### Update tools
```
orchestrate tools import -k <kind of the tool> -f <path the tool file that you want to update> -a <id of the app> -r <path to the requirements.txt file>
```

### Remove tools
```
orchestrate tools remove -n my-tool-name
```

---

## Connections

### Import connection from file
```
orchestrate connections import -f my_app.yaml
```

### Add and configure connection
```
orchestrate connections add -a <app_id>
orchestrate connections configure -a <app_id> --env draft --kind basic --type team
```

### Set credentials (Basic)
```
orchestrate connections set-credentials -a application_id --env draft -u username -p password
```

### Set credentials (Bearer)
```
orchestrate connections set-credentials -a application_id --env draft --token thebearertoken
```

### Set credentials (API Key)
```
orchestrate connections set-credentials -a application_id --env draft --api-key theapikey
```

### Set credentials (Key-Value)
```
orchestrate connections set-credentials -a application_id --env draft -e 'key1=value1' -e 'key2=value2'
```

### Set credentials (OAuth Auth Code)
```
orchestrate connections set-credentials -a application_id \
	--env draft \
	--client-id 'clientid' \
	--client-secret 'clientsecret' \
	--authorization-url 'https://api.example.com/oauth2/authorize' \
	--token-url 'https://api.example.com/oauth2/token' \
	--scope admin
```

### Set credentials (OAuth Password)
```
orchestrate connections set-credentials -a application_id \
	--env draft \
	--client-id 'clientid' \
	--client-secret 'clientsecret' \
	--username 'username' \
	--password 'password' \
	--token-url 'https://api.example.com/oauth2/token' \
	--scope admin
```

### Set credentials (OAuth Client Credentials)
```
orchestrate connections set-credentials -a application_id \
	--env draft \
	--client-id 'clientid' \
	--client-secret 'clientsecret' \
	--token-url 'https://api.example.com/oauth2/token' \
	--scope admin
```

### SSO / IDP (single exchange)
```
orchestrate connections set-credentials \
	-a my_app \
	--env draft \
	--grant-type "urn:ietf:params:oauth:grant-type:token-exchange" \
	--client-id "<client_id>" \
	--token-url "<token_url>"
```

### SSO / IDP (flow)
```
orchestrate connections set-identity-provider --app-id workday \
	--env draft \
	--url https://idp-server/oauth2/v2.0/token \
	--client-id clientid \
	--client-secret clientsecret \
	--scope scope \
	--grant-type urn:ietf:params:oauth:grant-type:jwt-bearer

orchestrate connections set-credentials --app-id workday \
	--env draft \
	--client-id clientid \
	--token-url https://token-server/ccx/oauth2/ibmsrv_dpt1/token \
	--grant-type urn:ietf:params:oauth:grant-type:saml2-bearer
```

### List connections
```
orchestrate connections list
```

### Export connection
```
orchestrate connections export -a <app_id> -o <output_file>.yml
```

### Update connection
```
orchestrate connections import --file <path to file with the same --app-id <name of the connection that you want to update>
```

### Remove connection
```
orchestrate connections remove --app-id <my_app_id>
```

---

## Knowledge Bases

### Import knowledge base
```
orchestrate knowledge-bases import -f <knowledge-base-file-path>
```

### Import KB using a connection (external providers)
```
orchestrate connections add -a my_credentials
orchestrate connections configure -a my_credentials --env draft --kind basic --type team
orchestrate connections set-credentials -a my_credentials --env draft -u <username> -p <password>
orchestrate knowledge-bases import -f <my_knowledge_base_file> -a my_credentials
```

---

## Toolkits (MCP)

### Add local MCP toolkit
```
orchestrate toolkits add --kind mcp --name tavily --description "Search the internet" --command "pipx -y mcp-tavily@0.1.10" --tools "*" --app-id tavily
```

### Add remote MCP toolkit
```
orchestrate toolkits add --kind mcp --name <toolkit-name> --description <toolkit-description> --url <toolkit-url> --transport <protocol-for-remote-mcp> --tools <tools> --app-id <connection>
```

### Import MCP toolkit from file
```
orchestrate toolkits import -f toolkit_name.yaml -a my_connection
```

### List toolkits
```
orchestrate toolkits list -v
```

### Export toolkit
```
orchestrate toolkits export -n my-toolkit -o my-toolkit.zip
```

### Remove toolkit
```
orchestrate toolkits remove -n my-toolkit-name
```

---

## Observability (Langfuse)

### Configure Langfuse (inline)
```
orchestrate settings observability langfuse configure \
	--url "https://cloud.langfuse.com/api/public/otel" \
	--api-key "sk-lf-0000-0000-0000-0000-0000" \
	--health-uri "https://cloud.langfuse.com" \
	--config-json '{"public_key": "pk-lf-0000-0000-0000-0000-0000"}'
```

### Configure Langfuse (file)
```
orchestrate settings observability langfuse configure --config-file=path_to_file.yml
```
