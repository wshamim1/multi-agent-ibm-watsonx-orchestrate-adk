# Example Prompts for API Data Fetcher Agents

This document provides example prompts you can use to interact with the API Data Fetcher agent system.

## Basic Data Fetching

### Simple Endpoint Fetching
```
Can you fetch data from the /api/v1/products endpoint?
```

```
Retrieve data from /api/v1/orders using the API
```

```
Get the data available at /api/v1/dashboard
```

## User Information Retrieval

### Fetch Specific User Data
```
Can you get the information for user ID 123?
```

```
Fetch user details for user 456
```

```
Show me the profile data for user user_789
```

## Search Operations

### Basic Search
```
Search the API for products
```

```
Find all items matching "customer"
```

### Search with Filters
```
Search for products with status "active"
```

```
Find all customers where status is "active" and type is "premium"
```

```
Search for orders with filters: {"status": "completed", "priority": "high"}
```

## Combined Operations (Fetch + Process)

### Fetch and Analyze
```
Fetch data from /api/v1/sales and analyze the results
```

```
Get user information for ID 100 and show me a detailed report
```

```
Search for active products and give me a summary
```

### Fetch and Format
```
Retrieve data from /api/v1/inventory and format it as a table
```

```
Get user 250's data and show it in a detailed format
```

```
Search for "services" and display the results as a summary report
```

## Complex Workflows

### Multi-step Analysis
```
Fetch all data from /api/v1/users, process it, and show me:
1. How many users are active
2. How many are inactive
3. A summary report
```

```
Search for products with status "active", analyze the results, 
and create a detailed report showing categories and relevance scores
```

### Data Comparison
```
Get user information for ID 123 and ID 456, then compare their roles and status
```

```
Fetch data from /api/v1/products and /api/v1/inventory, then analyze inventory levels
```

## Reporting

### Summary Reports
```
Fetch /api/v1/metrics and give me a summary report
```

```
Search for all "transactions" and show me a summary with key statistics
```

### Detailed Reports
```
Get user 999's complete profile and create a detailed report
```

```
Fetch data from /api/v1/analytics and provide a detailed analysis
```

### Custom Format Reports
```
Search for "customers" and format the results as a table
```

```
Get data from /api/v1/logs and show it in summary format
```

## Error Handling & Troubleshooting

### Connection Testing
```
Can you test if the API connection is working?
```

```
Try fetching data from /api/v1/health to check the connection
```

### Retry Requests
```
The previous request failed, can you try fetching /api/v1/data again?
```

## Real-World Scenarios

### E-commerce
```
Search for products in category "electronics" with status "in-stock", 
then show me the top 5 results with their details
```

```
Get order details for user 123 and analyze their purchase history
```

### User Management
```
Fetch all active users and show me statistics about their departments and locations
```

```
Search for users in the "Engineering" department and create a summary report
```

### Analytics
```
Retrieve the latest metrics from /api/v1/analytics/dashboard 
and highlight the key performance indicators
```

```
Get sales data and calculate the total number of transactions and their status breakdown
```

### Monitoring
```
Fetch system status from /api/v1/system/health and tell me if everything is working properly
```

```
Search for error logs and summarize any critical issues
```

## Advanced Queries

### Conditional Logic
```
Fetch user data for ID 123. If the user is active, also get their recent orders.
Otherwise, just show their basic profile.
```

### Aggregation
```
Search for all products, calculate how many are in each category, 
and show me the distribution
```

### Data Transformation
```
Get customer data, extract only the email addresses and locations, 
and format them as a list
```

## Tips for Effective Prompts

1. **Be Specific**: Include exact endpoint paths and parameters
2. **Specify Format**: Mention if you want summary, detailed, or table format
3. **Include Filters**: When searching, specify filters in JSON format for precision
4. **Request Analysis**: Ask for specific metrics or insights you want to see
5. **Multi-step**: Break complex requests into clear steps

## Testing the Connection

Before using the agents extensively, test your connection:

```
Can you check if the basic authentication connection is set up correctly?
```

If you encounter authentication errors, make sure you've set up credentials:
```bash
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u your_username \
  -p your_password
```
