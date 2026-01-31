# HR Assistant Agent

An intelligent HR assistant agent that helps employees with company policies, benefits, and procedures using knowledge bases.

## Overview

This agent uses IBM watsonx Orchestrate ADK with Retrieval-Augmented Generation (RAG) to answer employee questions by searching company policy documents.

## Features

- **Knowledge Base Integration**: Accesses company policies, handbook, and procedures
- **Policy Search**: Finds relevant information from company documentation
- **PTO Calculations**: Calculates vacation and time-off balances
- **Compliance Checking**: Verifies actions against company policies
- **Professional Responses**: Provides accurate, policy-backed answers

## Files

- `hr_assistant_agent.yml` - Agent configuration
- `hr_assistant_tools.py` - Tools for HR operations
- `README.md` - This file

## Knowledge Base

This agent uses the `company_policies_kb` knowledge base which includes:
- Company Handbook
- Remote Work Policy
- Expense Reimbursement Policy

## Quick Start

### 1. Deploy the Knowledge Base

```bash
# From the project root
orchestrate knowledge-bases import -f knowledge_bases/company_policies_kb.yml
```

### 2. Deploy the Agent

```bash
# From this directory
orchestrate agents deploy hr_assistant_agent.yml
```

### 3. Test the Agent

```bash
orchestrate agents chat hr_assistant_agent
```

## Example Conversations

### Example 1: Vacation Policy
```
User: "How many vacation days do I get?"

Agent: According to the Company Handbook, vacation days are allocated based on years of service:
- 0-5 years: 15 days per year
- 5+ years: 20 days per year

Additionally, you receive:
- Sick Leave: 10 days per year
- Personal Days: 3 days per year
- Holidays: 10 company-observed holidays

Would you like me to calculate your current PTO balance?
```

### Example 2: Remote Work
```
User: "Can I work from home full-time?"

Agent: According to the Remote Work Policy, full-time remote work is available with the following requirements:

Eligibility:
- Must have completed 90-day probationary period
- Role must be suitable for remote work
- Manager approval required
- Must maintain reliable internet connection

You'll need to:
1. Discuss with your manager
2. Submit a remote work request
3. Ensure you have appropriate workspace
4. Be available during core hours (10 AM - 3 PM)

Would you like more details about the remote work policy?
```

### Example 3: Expense Reimbursement
```
User: "What's the meal allowance when traveling?"

Agent: According to the Expense Reimbursement Policy, daily meal allowances are:

- Breakfast: $15
- Lunch: $25
- Dinner: $40
- Total daily maximum: $80

Important notes:
- Receipts required for expenses over $25
- Submit expense reports within 30 days
- Alcohol limited to 2 drinks per person (client entertainment only)

Need help with anything else regarding expenses?
```

## Available Tools

### search_policy
Search company policies and procedures
```python
search_policy(query="vacation policy", policy_type="benefits")
```

### calculate_pto_balance
Calculate employee PTO balance
```python
calculate_pto_balance(employee_id="EMP123", year=2024)
```

### check_policy_compliance
Check if an action complies with company policies
```python
check_policy_compliance(action="expense claim", context="client dinner $150")
```

## Configuration

The agent is configured with:
- **Model**: `watsonx/meta-llama/llama-3-2-90b-vision-instruct`
- **Knowledge Base**: `company_policies_kb`
- **Style**: Professional and helpful

## Customization

### Adding New Policies

1. Add policy document to `knowledge_bases/documents/`
2. Update `knowledge_bases/company_policies_kb.yml`:
```yaml
documents:
  - documents/company_handbook.txt
  - documents/remote_work_policy.txt
  - documents/expense_policy.txt
  - documents/your_new_policy.txt  # Add here
```
3. Redeploy the knowledge base

### Modifying Agent Behavior

Edit `hr_assistant_agent.yml` to change:
- Instructions and guidelines
- Response style
- Available tools
- Knowledge bases

## Best Practices

1. **Keep Policies Updated**: Regularly update documents in the knowledge base
2. **Test Changes**: Test agent responses after policy updates
3. **Monitor Usage**: Track common questions to improve documentation
4. **Privacy**: Never include sensitive employee data in policies
5. **Escalation**: Direct complex issues to human HR staff

## Troubleshooting

### Agent Can't Find Policy Information
- Verify knowledge base is deployed
- Check document paths in YAML configuration
- Ensure documents are in correct format (TXT, PDF, DOCX)

### Incorrect Responses
- Review and update policy documents
- Improve document structure and formatting
- Add more specific examples to policies

### Deployment Issues
- Verify watsonx credentials in `.env`
- Check agent YAML syntax
- Ensure knowledge base name matches in agent config

## Support

For issues or questions:
- Review the [Knowledge Base Guide](../knowledge_bases/KNOWLEDGE_BASE_GUIDE.md)
- Check the [main README](../README.md)
- Contact your watsonx administrator

## License
Open