# TechMart Customer Care Agent - Example Prompts

This document contains example prompts to test all features of the TechMart customer care agent system.

## 🛍️ Product Browsing

### Browse by Category
```
Show me electronics products
```
```
What clothing items do you have?
```
```
Show me products in the Home & Garden category
```
```
What sports equipment is available?
```

### Search Products
```
Search for headphones
```
```
Do you have any smartwatches?
```
```
Show me yoga mats
```

## ⭐ Product Reviews

### Get Reviews
```
Show me reviews for product ELEC001
```
```
What do customers think about the wireless headphones?
```
```
Can I see reviews for the Smart Watch Pro?
```

### Filter Reviews
```
Show me 5-star reviews for ELEC001
```
```
What are the best reviews for the cookware set?
```

## 📦 Order Management

### View Orders
```
Show me my recent orders
```
```
What's the status of my orders?
```
```
Do I have any pending orders?
```

### Specific Order
```
When will my order ORD7654321 arrive?
```
```
What's in order ORD1234567?
```

## 🚚 Shipment Tracking

### Track Packages
```
Track shipment TRK9876543210
```
```
Where is my package with tracking number TRK1234567890?
```
```
Track my order
```

### Delivery Status
```
When will my package arrive?
```
```
Has my order been delivered?
```

## 📊 Product Availability

### Check Stock
```
Is the Smart Watch Pro in stock?
```
```
Check availability for product ELEC001
```
```
Do you have the cookware set available?
```

### Store Inventory
```
Which stores have the wireless headphones in stock?
```
```
Can I pick up the yoga mat at the Boston store?
```
```
Show me store availability for ELEC002
```

## 💰 Shipping Costs

### Calculate Shipping
```
How much does shipping cost to zip code 02101?
```
```
Calculate shipping for a $75 order to Boston
```
```
What are my shipping options for a 10 lb package?
```

### Shipping Methods
```
What shipping methods are available?
```
```
Do I qualify for free shipping?
```
```
How much is overnight shipping to 02101?
```

## 🏪 Store Locations

### Find Stores
```
Find stores near Boston
```
```
Where is your nearest pickup point?
```
```
Show me all warehouse locations
```

### Store Details
```
What are the hours for the Boston flagship store?
```
```
Which stores offer same-day pickup?
```

## 🎫 Support Tickets

### Create Tickets
```
I need help with a damaged product. Can you create a ticket?
```
```
My order hasn't arrived yet, please open a support ticket
```
```
The product I received is defective, I need assistance
```
```
I want to return an item, can you help?
```

### View Tickets
```
Show me all my support tickets

## 📋 Quick Reference - IDs to Use

### Product IDs
- `ELEC001` - Wireless Bluetooth Headphones
- `ELEC002` - Smart Watch Pro
- `CLOTH001` - Cotton T-Shirt Pack
- `HOME001` - Stainless Steel Cookware Set
- `SPORT001` - Yoga Mat with Carrying Strap
- `BOOK001` - The Art of Programming

### Order IDs
- `ORD1234567` - Delivered order (2x Headphones)
- `ORD7654321` - Shipped order (Smartwatch + Yoga Mat)
- `ORD9876543` - Processing order (Cookware Set)
- `ORD5555555` - Cancelled order (2x Books)

### Tracking Numbers
- `TRK9876543210` - Delivered package (FedEx)
- `TRK1234567890` - In transit package (UPS)

### Store IDs
- `STR001` - TechMart Boston Flagship
- `STR002` - TechMart Cambridge Outlet
- `STR003` - TechMart Warehouse - Somerville
- `STR004` - TechMart Pickup - Brookline

### Incident Numbers
- Incidents are auto-generated starting from `INC0001000`
- After creating a ticket, use the returned incident number

## 🎬 Complete Example Conversations

### Scenario 1: Product Research & Purchase
```
User: "Show me electronics products"
Agent: [Shows product catalog]

User: "Show me reviews for ELEC001"
Agent: [Shows customer reviews]

User: "Is ELEC001 in stock at STR001?"
Agent: [Shows availability]

User: "Calculate shipping to 02101 for a $80 order"
Agent: [Shows shipping options with free shipping]
```

### Scenario 2: Order Issue Resolution
```
User: "Show me my orders"
Agent: [Shows order list]

User: "My order ORD7654321 hasn't arrived, create a support ticket"
Agent: [Creates ticket INC0001000]

User: "What's the status of INC0001000?"
Agent: [Shows ticket details]
```

### Scenario 3: Package Tracking
```
User: "Track shipment TRK9876543210"
Agent: [Shows delivered status with full tracking history]

User: "Where is package TRK1234567890?"
Agent: [Shows in-transit status with current location]
```
```
```
What's the status of incident INC0001000?
```
```
Do I have any open tickets?
```

## 🔄 Complex Multi-Step Scenarios

### Shopping Journey
```
1. Show me electronics products
2. What do customers say about the wireless headphones?
3. Is it in stock at the Boston store?
4. How much is shipping to 02101?
5. Great! I'll order it.
```

### Order Issue Resolution
```
1. Show me my recent orders
2. Track shipment for order ORD7654321
3. The package hasn't arrived, can you create a support ticket?
4. Show me the ticket status
```

### Product Research
```
1. Search for smartwatches
2. Show me reviews for the Smart Watch Pro
3. Check if it's available at nearby stores
4. What's the price with express shipping?
```

## 💡 Tips for Best Results

1. **Be Specific**: Use product IDs (like ELEC001) for precise results
2. **Use Tracking Numbers**: Provide tracking numbers for shipment queries
3. **Mention Location**: Include zip codes for shipping and store searches
4. **Reference Order Numbers**: Use order IDs (like ORD1234567) for order queries
5. **Describe Issues Clearly**: When creating tickets, explain the problem in detail

## 🎯 Testing All Features Checklist

- [ ] Browse products by category
- [ ] Search for specific products
- [ ] Read product reviews
- [ ] Check order status
- [ ] Track a shipment
- [ ] Check product availability
- [ ] Calculate shipping costs
- [ ] Find nearby stores
- [ ] Create a support ticket
- [ ] View ticket status

## 📝 Sample Test Script

Run through this complete test to verify all features:

```
1. "Show me electronics products"
2. "Show me reviews for the wireless headphones"
3. "Is product ELEC001 in stock at Boston stores?"
4. "Calculate shipping cost to 02101 for a $80 order"
5. "Show me my recent orders"
6. "Track shipment TRK9876543210"
7. "Find stores near Boston"
8. "I received a damaged product, can you create a support ticket?"
9. "Show me all my support tickets"
10. "What's the status of the ticket you just created?"
```

## 🚀 Advanced Queries

### Comparison Shopping
```
Compare the wireless headphones and the Smart Watch Pro
```

### Bundle Deals
```
If I buy the headphones and smartwatch together, what's the total shipping cost?
```

### Urgent Issues
```
I need the yoga mat urgently - what's the fastest delivery option to 02101?
```

### Multiple Products
```
Check availability for products ELEC001, ELEC002, and SPORT001 at the Cambridge store
```

---

**Note**: All data is mocked for demonstration purposes. No real orders, shipments, or support tickets are created.