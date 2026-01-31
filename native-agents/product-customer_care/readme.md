# Customer Care Example - E-Commerce Edition

This example simulates a customer care agent for **TechMart**, an e-commerce company. The agent can help customers with:
- Browsing products by category
- Checking order status
- Finding nearby store locations
- Creating support tickets for issues

**Note:** This implementation uses **mock data** and does NOT require a real ServiceNow account. All ServiceNow functionality is simulated with in-memory storage.

## Features

### Customer Care Agent Features
- **Browse Products** - Search product catalog by category or keywords
- **Check Orders** - View order history, status, and tracking information
- **Track Shipments** - Real-time package tracking with delivery updates
- **Product Reviews** - Read customer reviews and ratings
- **Check Availability** - See real-time stock at online warehouse and physical stores
- **Calculate Shipping** - Get shipping costs for different delivery methods
- **Find Stores** - Locate nearby TechMart store locations
- **Support Tickets** - Escalate issues to customer support team

### ServiceNow Agent (Mock Implementation)
- Create support tickets for customer issues
- View all created tickets
- Retrieve specific tickets by incident number
- No external ServiceNow connection required!

## Setup Instructions

### Prerequisites - Choose Your LLM Provider

You need to configure ONE of these options:

### Option 1: Using WatsonX (Pre-configured, Recommended)
✅ **Already configured in the agents!**

Your `.env` file should have:
```
WATSONX_APIKEY=<your watsonx api key>
WXO_API_KEY=<your watsonx api key>
WATSONX_SPACE_ID=<your space id>
```

The agents use: `watsonx/meta-llama/llama-3-2-90b-vision-instruct`

**This should work out of the box if your WatsonX keys are valid.**

### Option 2: Using OpenAI
⚠️ **Your current OpenAI key appears to be invalid or expired.**

1. Get a NEW API key from: https://platform.openai.com/api-keys
2. Update your `.env` file in the project root:
   ```
   OPENAI_API_KEY=sk-proj-YOUR_NEW_KEY_HERE
   ```
3. Update both agent files (`agents/customer_care_agent.yaml` and `agents/service_now_agent.yaml`):
   ```yaml
   llm: openai/gpt-4o-mini
   ```

Recommended OpenAI models:
- `openai/gpt-4o` - Most capable
- `openai/gpt-4o-mini` - Faster and cheaper (recommended)
- `openai/gpt-4-turbo` - Good balance
- `openai/gpt-3.5-turbo` - Most economical

### Option 3: Using Groq (Free Alternative)
1. Get a FREE API key from: https://console.groq.com/keys
2. Add to your `.env` file:
   ```
   GROQ_API_KEY=gsk_YOUR_KEY_HERE
   ```
3. Update both agent files:
   ```yaml
   llm: groq/llama-3.1-70b-versatile
   ```

### 🔑 Where to Set API Keys

**IMPORTANT:** API keys go in the `.env` file in the project ROOT directory:
```
/Users/wilsonshamim/Desktop/Code/pythonProjectsOld/genai-IBM_watsonx_orchestrate_adk/IBM_watsonx_Orchestrate_ADK/.env
```

**NOT** in the customer_care folder!

### ⚠️ Common Issue: "gateway" Error

If you see an error like "Incorrect API key provided: gateway", it means the orchestrate server isn't loading your .env file properly.

**Solution:**
1. **Stop the orchestrate server** (Ctrl+C or close the terminal)
2. **Restart it with the .env file explicitly:**
   ```bash
   cd /Users/wilsonshamim/Desktop/Code/pythonProjectsOld/genai-IBM_watsonx_orchestrate_adk/IBM_watsonx_Orchestrate_ADK
   orchestrate server start -e .env
   ```
3. Wait for the server to fully start
4. In a NEW terminal, run the chat:
   ```bash
   orchestrate chat start
   ```

The server MUST be restarted after any .env file changes!

### Installation Steps

1. Install dependencies:
   ```bash
   pip install -r tools/requirements.txt
   ```

2. Start the orchestrate server:
   ```bash
   orchestrate server start -e .env
   ```

4. Import and deploy the agents using the management script:
   ```bash
   ./manage_customer_care.sh import-all
   ./manage_customer_care.sh deploy-all
   ```
   
   Or use the legacy import script:
   ```bash
   ./import-all.sh
   ```

5. Start chatting:
   ```bash
   orchestrate chat start
   ```

## Management Script

The `manage_customer_care.sh` script provides easy management of the customer care system:

```bash
# Import everything (tools and agents)
./manage_customer_care.sh import-all

# Deploy all agents
./manage_customer_care.sh deploy-all

# Check status of all components
./manage_customer_care.sh status

# Undeploy all agents
./manage_customer_care.sh undeploy-all

# Remove everything (undeploy, remove agents, remove tools)
./manage_customer_care.sh remove-all

# Show help
./manage_customer_care.sh help
```

Available commands:
- `import-all` - Import all tools and agents
- `import-tools` - Import only tools
- `import-agents` - Import only agents
- `deploy-all` - Deploy all agents
- `undeploy-all` - Undeploy all agents
- `remove-all` - Remove everything
- `remove-tools` - Remove only tools
- `remove-agents` - Remove only agents
- `status` - Show current status
- `help` - Display help message

## Sample Conversation Scripts

### Product Browsing & Reviews
- "Show me electronics products"
- "What books do you have available?"
- "Search for headphones"
- "Show me reviews for product ELEC001"
- "What do customers think about the Smart Watch Pro?"

### Order Management & Tracking
- "Show me my recent orders"
- "What's the status of my orders?"
- "When will my order ORD7654321 arrive?"
- "Track my shipment with tracking number TRK9876543210"
- "Where is my package right now?"

### Product Availability & Stock
- "Is the Smart Watch Pro in stock?"
- "Check availability for product ELEC001"
- "Which stores have the cookware set in stock?"
- "Can I pick up the yoga mat at the Boston store?"

### Shipping & Delivery
- "How much does shipping cost to zip code 02101?"
- "Calculate shipping for a $75 order to Boston"
- "What shipping options are available?"
- "Do I qualify for free shipping?"

### Store Locations
- "Find stores near Boston"
- "Where is your nearest pickup point?"
- "Show me all warehouse locations"

### Support Tickets
- "I need help with a damaged product. Can you create a ticket?"
- "My order hasn't arrived yet, please open a support ticket"
- "Show me all my support tickets"
- "What's the status of incident INC0001000?"

## Mock Data

The system includes pre-populated mock data for:
- **6 sample products** across different categories (Electronics, Clothing, Home & Garden, Sports, Books)
- **4 sample orders** with various statuses (Delivered, Shipped, Processing, Cancelled)
- **4 store locations** in the Boston area (Flagship, Outlet, Warehouse, Pickup Point)
- **Product reviews** with ratings and verified purchase status
- **Shipment tracking** with real-time delivery updates
- **Inventory levels** across online warehouse and physical stores
- **Shipping rates** for different delivery methods
- **Support tickets** created dynamically as you interact with the agent

No external APIs or databases are required! All data is mocked for demonstration purposes.

## New Features Added

### 🌟 Product Reviews (`get_product_reviews`)
- Read customer reviews with ratings (1-5 stars)
- See verified purchase badges
- View helpful counts for each review
- Filter reviews by minimum rating

### 📦 Shipment Tracking (`track_shipment`)
- Real-time package tracking
- Detailed tracking events with timestamps
- Carrier information (FedEx, UPS, USPS)
- Estimated delivery dates
- Current package location

### 📊 Product Availability (`check_product_availability`)
- Check online warehouse stock levels
- See inventory at physical store locations
- Stock status indicators (In Stock, Low Stock, Out of Stock, Backordered)
- Next restock dates for out-of-stock items
- Same-day shipping availability

### 💰 Shipping Calculator (`calculate_shipping_cost`)
- Calculate shipping costs for different methods
- Standard, Express, Overnight, and Same Day options
- Free shipping for orders over $50
- Weight-based pricing
- Local delivery options for Boston metro area