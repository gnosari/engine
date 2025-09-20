---
sidebar_position: 5
---

# MySQL Query Tool

The **mysql_query** tool enables agents to execute SQL queries against MySQL databases. This tool provides secure, efficient database access with connection pooling, query validation, and comprehensive error handling.

## Overview

The MySQL query tool allows agents to:
- Execute SELECT queries to retrieve data
- Perform INSERT, UPDATE, DELETE operations
- Use connection pooling for efficient database access
- Handle query timeouts and connection management
- Validate SQL queries for safety
- Process results in structured JSON format

## Capabilities

- ✅ **SQL Query Execution**: Support for all standard SQL operations
- ✅ **Connection Pooling**: Efficient database connection management
- ✅ **Query Validation**: Basic safety checks for SQL queries
- ✅ **Timeout Handling**: Configurable query timeouts
- ✅ **Error Handling**: Comprehensive database error reporting
- ✅ **Result Formatting**: Structured JSON responses
- ✅ **Security**: SSL support and credential management
- ✅ **Performance**: Optimized connection pooling and query execution

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: mysql_query
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: localhost
      port: 3306
      database: my_database
      username: my_user
      password: my_password
```

:::warning Database Credentials
Never hardcode database passwords in your YAML files. Use environment variables for sensitive credentials.
:::

### Advanced Configuration

```yaml
tools:
  - name: production_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: db.example.com
      port: 3306
      database: production_db
      username: app_user
      password: secure_password
      charset: utf8mb4
      pool_size: 10
      max_overflow: 20
      pool_timeout: 30
      pool_recycle: 3600
      query_timeout: 60
      echo: false
```

### Multiple Database Configurations

```yaml
tools:
  - name: user_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: user-db.example.com
      port: 3306
      database: users
      username: user_service
      password: user_password
      pool_size: 5
      query_timeout: 30

  - name: analytics_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: analytics-db.example.com
      port: 3306
      database: analytics
      username: analytics_user
      password: analytics_password
      pool_size: 15
      query_timeout: 120
```

## Agent Assignment

Assign the MySQL query tool to agents that need database access:

```yaml
agents:
  - name: Data Analyst
    instructions: >
      You are a data analyst who works with databases. Use the mysql_query tool to:
      
      1. **Query Data**: Execute SELECT queries to retrieve information
      2. **Analyze Results**: Process and interpret query results
      3. **Generate Reports**: Create data-driven insights and reports
      4. **Validate Data**: Check data quality and consistency
      
      Always use appropriate SQL syntax and handle errors gracefully.
    model: gpt-4o
    tools:
      - mysql_query
```

## Usage Examples

### Example 1: Customer Data Analysis

```yaml
name: Customer Analytics Team

tools:
  - name: customer_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: customer-db.example.com
      port: 3306
      database: customers
      username: analytics_user
      password: analytics_password
      pool_size: 10
      query_timeout: 60

agents:
  - name: Customer Analyst
    instructions: >
      Analyze customer data and provide insights. Use the customer_db tool to:
      - Get customer information: SELECT * FROM customers WHERE id = ?
      - Analyze purchase patterns: SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id
      - Check customer activity: SELECT * FROM customer_activity WHERE last_login > ?
    model: gpt-4o
    tools:
      - customer_db

  - name: Report Generator
    instructions: "Generate reports based on customer analysis"
    model: gpt-4o
    tools:
      - customer_db
```

### Example 2: E-commerce Operations

```yaml
name: E-commerce Operations Team

tools:
  - name: ecommerce_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: ecommerce-db.example.com
      port: 3306
      database: ecommerce
      username: operations_user
      password: operations_password
      pool_size: 15
      query_timeout: 45

agents:
  - name: Inventory Manager
    instructions: >
      Manage inventory and product data. Use the ecommerce_db tool to:
      - Check stock levels: SELECT product_id, quantity FROM inventory WHERE quantity < ?
      - Update inventory: UPDATE inventory SET quantity = ? WHERE product_id = ?
      - Get product details: SELECT * FROM products WHERE category = ?
    model: gpt-4o
    tools:
      - ecommerce_db

  - name: Order Processor
    instructions: >
      Process orders and update order status. Use the ecommerce_db tool to:
      - Create orders: INSERT INTO orders (customer_id, total, status) VALUES (?, ?, ?)
      - Update order status: UPDATE orders SET status = ? WHERE order_id = ?
      - Get order history: SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC
    model: gpt-4o
    tools:
      - ecommerce_db
```

### Example 3: User Management System

```yaml
name: User Management Team

tools:
  - name: user_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: user-db.example.com
      port: 3306
      database: users
      username: user_service
      password: user_password
      pool_size: 8
      query_timeout: 30

agents:
  - name: User Administrator
    instructions: >
      Manage user accounts and permissions. Use the user_db tool to:
      - Create users: INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)
      - Update user info: UPDATE users SET email = ? WHERE username = ?
      - Check permissions: SELECT role FROM user_roles WHERE user_id = ?
      - Deactivate users: UPDATE users SET active = 0 WHERE username = ?
    model: gpt-4o
    tools:
      - user_db

  - name: User Support
    instructions: >
      Help users with account issues. Use the user_db tool to:
      - Find user accounts: SELECT * FROM users WHERE email = ? OR username = ?
      - Check login history: SELECT * FROM login_logs WHERE user_id = ? ORDER BY login_time DESC
      - Reset passwords: UPDATE users SET password_hash = ? WHERE username = ?
    model: gpt-4o
    tools:
      - user_db
```

## Tool Parameters

The MySQL query tool accepts the following configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | string | "localhost" | MySQL server hostname |
| `port` | int | 3306 | MySQL server port |
| `database` | string | "" | Database name |
| `username` | string | "" | Database username |
| `password` | string | "" | Database password |
| `charset` | string | "utf8mb4" | Character set for connections |
| `pool_size` | int | 5 | Number of connections in the pool |
| `max_overflow` | int | 10 | Maximum overflow connections |
| `pool_timeout` | int | 30 | Timeout for getting connection from pool |
| `pool_recycle` | int | 3600 | Time before connection is recycled (seconds) |
| `query_timeout` | int | 30 | Default query timeout (seconds) |
| `echo` | bool | false | Whether to echo SQL statements (debugging) |

## Per-Call Parameters

When agents use the tool, they can specify additional parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | The SQL query to execute |
| `query_type` | string | Type of query (SELECT, INSERT, UPDATE, DELETE) |
| `limit` | int | Maximum number of rows to return (SELECT queries) |
| `timeout` | int | Override configured query timeout |

## Agent Instructions

Provide clear instructions for database operations:

```yaml
agents:
  - name: Database Specialist
    instructions: >
      You are a database specialist who works with MySQL databases. When using the mysql_query tool:
      
      **Query Types:**
      - SELECT: Retrieve data from tables
      - INSERT: Add new records to tables
      - UPDATE: Modify existing records
      - DELETE: Remove records from tables
      
      **Best Practices:**
      - Use parameterized queries when possible
      - Include appropriate WHERE clauses for UPDATE/DELETE
      - Use LIMIT clauses for large result sets
      - Handle errors gracefully and provide meaningful messages
      
      **Security:**
      - Never execute DROP, TRUNCATE, or ALTER statements
      - Validate query types match the intended operation
      - Use appropriate timeouts for long-running queries
    model: gpt-4o
    tools:
      - mysql_query
```

## Security Best Practices

### 1. **Environment Variables**
Store database credentials in environment variables:

```yaml
tools:
  - name: secure_db
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: ${DB_HOST}
      port: ${DB_PORT}
      database: ${DB_NAME}
      username: ${DB_USER}
      password: ${DB_PASSWORD}
```

:::tip Environment Variables
Use environment variables for all sensitive database credentials. This keeps your configuration secure and makes it easier to manage different environments.
:::

### 2. **Connection Security**
Use SSL connections in production:

```yaml
args:
  charset: utf8mb4
  # SSL is handled by the connection string
```

### 3. **Query Validation**
The tool includes basic safety checks:
- Warns about potentially dangerous keywords (DROP, TRUNCATE, ALTER)
- Validates query types match the actual query
- Provides timeout protection

:::warning SQL Safety
The tool includes basic safety checks, but always validate SQL queries before execution. Never allow untrusted users to execute arbitrary SQL.
:::

## Error Handling

The MySQL query tool provides comprehensive error handling:

- **Connection Errors**: Database connectivity issues
- **SQL Errors**: Syntax and execution errors
- **Timeout Errors**: Long-running query protection
- **Permission Errors**: Database access restrictions
- **Data Type Errors**: Result processing issues

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify database host, port, and credentials
   - Check network connectivity
   - Ensure database server is running

2. **Authentication Errors**
   - Verify username and password
   - Check user permissions
   - Ensure user has access to the specified database

3. **Query Timeout Errors**
   - Increase query timeout for complex queries
   - Optimize query performance
   - Consider breaking large queries into smaller parts

4. **Permission Errors**
   - Check user permissions for specific tables
   - Verify user has appropriate privileges
   - Ensure user can execute the required operations

### Debug Mode

Use debug mode to see detailed database query logs:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Database Debugging
Debug mode shows detailed SQL query execution information, including connection details, query execution time, and result processing.
:::

## Related Tools

- [API Request Tool](api-request) - For external service integration
- [Delegate Agent Tool](delegate-agent) - For multi-agent coordination
- [Knowledge Query Tool](knowledge-query) - For information retrieval

The MySQL query tool is essential for creating data-driven AI agents that can interact with databases. Use it to build agents that can analyze data, generate reports, and perform database operations efficiently and securely.