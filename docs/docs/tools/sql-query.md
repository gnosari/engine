---
sidebar_position: 4
---

# SQL Query Tool

The **sql_query** tool enables agents to execute SQL queries against any database that supports SQLAlchemy connections. This universal database tool provides secure, efficient database access with connection pooling, query validation, and comprehensive error handling across multiple database types.

## Overview

The SQL query tool allows agents to:
- Execute SQL queries against any SQLAlchemy-compatible database
- Support multiple database types (PostgreSQL, MySQL, SQLite, Oracle, SQL Server, etc.)
- Use connection pooling for efficient database access
- Handle query timeouts and connection management
- Validate SQL queries for safety
- Process results in multiple formats (JSON, table, raw)
- Configure database-specific connection parameters

## Supported Databases

The SQL Query Tool supports all databases compatible with SQLAlchemy:

| Database | Connection String Example |
|----------|-------------------------|
| **PostgreSQL** | `postgresql://user:pass@host:port/db` |
| **MySQL** | `mysql://user:pass@host:port/db` |
| **SQLite** | `sqlite:///path/to/database.db` |
| **Oracle** | `oracle://user:pass@host:port/db` |
| **SQL Server** | `mssql://user:pass@host:port/db` |
| **ClickHouse** | `clickhouse://user:pass@host:port/db` |
| **Snowflake** | `snowflake://user:pass@host:port/db` |
| **BigQuery** | `bigquery://project/dataset` |
| **Redshift** | `redshift://user:pass@host:port/db` |
| **CockroachDB** | `cockroachdb://user:pass@host:port/db` |

## Capabilities

- ✅ **Universal Database Support**: Works with any SQLAlchemy-compatible database
- ✅ **Connection Pooling**: Efficient database connection management
- ✅ **Query Validation**: Safety checks for SQL queries
- ✅ **Timeout Handling**: Configurable query timeouts
- ✅ **Error Handling**: Comprehensive database error reporting
- ✅ **Multiple Result Formats**: JSON, table, and raw output formats
- ✅ **Security**: Schema restrictions and keyword blocking
- ✅ **Performance**: Optimized connection pooling and query execution
- ✅ **Database-Specific Configuration**: Tailored connection parameters

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: sql_query
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: postgresql://user:password@localhost:5432/mydb
```

:::warning Database Credentials
Never hardcode database passwords in your YAML files. Use environment variables for sensitive credentials.
:::

### Advanced Configuration

```yaml
tools:
  - name: production_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: postgresql://user:password@db.example.com:5432/production
      pool_size: 10
      max_overflow: 20
      pool_timeout: 30
      pool_recycle: 3600
      query_timeout: 60
      echo: false
      enable_unsafe_operations: false
      allowed_schemas: ["public", "analytics"]
      blocked_keywords: ["TRUNCATE", "DROP TABLE"]
```

### Multiple Database Configurations

```yaml
tools:
  - name: postgres_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: postgresql://user:pass@postgres.example.com:5432/main
      pool_size: 10
      query_timeout: 30

  - name: mysql_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: mysql://user:pass@mysql.example.com:3306/analytics
      pool_size: 15
      query_timeout: 60

  - name: sqlite_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: sqlite:///data/local.db
      query_timeout: 10
```

## Agent Assignment

Assign the SQL query tool to agents that need database access:

```yaml
agents:
  - name: Data Analyst
    instructions: >
      You are a data analyst who works with multiple databases. Use the sql_query tool to:
      
      1. **Query Data**: Execute SELECT queries to retrieve information
      2. **Analyze Results**: Process and interpret query results
      3. **Generate Reports**: Create data-driven insights and reports
      4. **Validate Data**: Check data quality and consistency
      
      Always use appropriate SQL syntax for the specific database type and handle errors gracefully.
    model: gpt-4o
    tools:
      - sql_query
```

## Usage Examples

### Example 1: Multi-Database Analytics

```yaml
name: Multi-Database Analytics Team

tools:
  - name: postgres_main
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: postgresql://analytics:password@postgres.example.com:5432/main
      pool_size: 10
      query_timeout: 60

  - name: mysql_analytics
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: mysql://analytics:password@mysql.example.com:3306/analytics
      pool_size: 15
      query_timeout: 120

agents:
  - name: Cross-Database Analyst
    instructions: >
      Analyze data across multiple databases. Use the appropriate database tool:
      - postgres_main: For user data and transactions
      - mysql_analytics: For analytics and reporting data
      
      Cross-reference data between databases when needed.
    model: gpt-4o
    tools:
      - postgres_main
      - mysql_analytics

  - name: Report Generator
    instructions: "Generate comprehensive reports using data from both databases"
    model: gpt-4o
    tools:
      - postgres_main
      - mysql_analytics
```

### Example 2: Data Migration Team

```yaml
name: Data Migration Team

tools:
  - name: source_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: mysql://migration:password@source.example.com:3306/legacy
      pool_size: 5
      query_timeout: 30

  - name: target_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: postgresql://migration:password@target.example.com:5432/new
      pool_size: 10
      query_timeout: 60

agents:
  - name: Migration Coordinator
    instructions: >
      Coordinate data migration between databases. Use the source_db to read data
      and target_db to write data. Ensure data integrity during migration.
    model: gpt-4o
    tools:
      - source_db
      - target_db

  - name: Data Validator
    instructions: >
      Validate migrated data by comparing source and target databases.
      Check data completeness and accuracy.
    model: gpt-4o
    tools:
      - source_db
      - target_db
```

### Example 3: Development Environment

```yaml
name: Development Team

tools:
  - name: dev_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: sqlite:///dev.db
      query_timeout: 10
      echo: true
      enable_unsafe_operations: true

agents:
  - name: Developer
    instructions: >
      Work with the development database. You can perform all operations including
      schema changes and data manipulation for development purposes.
    model: gpt-4o
    tools:
      - dev_db
```

## Tool Parameters

The SQL query tool accepts the following configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `database_url` | string | **Required** | SQLAlchemy database connection URL |
| `pool_size` | int | 5 | Number of connections in the pool |
| `max_overflow` | int | 10 | Maximum overflow connections |
| `pool_timeout` | int | 30 | Timeout for getting connection from pool (seconds) |
| `pool_recycle` | int | 3600 | Time before connection is recycled (seconds) |
| `query_timeout` | int | 30 | Default query timeout (seconds) |
| `echo` | bool | false | Whether to echo SQL statements (debugging) |
| `enable_unsafe_operations` | bool | false | Allow dangerous operations (DROP, TRUNCATE, etc.) |
| `allowed_schemas` | list | null | List of allowed schema names (null = all allowed) |
| `blocked_keywords` | list | [] | Additional keywords to block in queries |
| `tool_name` | string | "sql_query" | Name of the tool |
| `tool_description` | string | "Execute SQL queries against a database" | Tool description |

## Per-Call Parameters

When agents use the tool, they can specify additional parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | **Required** | The SQL query to execute |
| `query_type` | string | "SELECT" | Type of query (SELECT, INSERT, UPDATE, DELETE, etc.) |
| `limit` | int | null | Maximum number of rows to return (SELECT queries) |
| `timeout` | int | null | Override configured query timeout |
| `return_format` | string | "json" | Return format: 'json', 'table', or 'raw' |

### Supported Query Types

- **SELECT**: Retrieve data from tables
- **INSERT**: Add new records to tables
- **UPDATE**: Modify existing records
- **DELETE**: Remove records from tables
- **CREATE**: Create tables, indexes, etc.
- **DROP**: Drop tables, indexes, etc. (requires `enable_unsafe_operations: true`)
- **ALTER**: Modify table structure (requires `enable_unsafe_operations: true`)
- **SHOW**: Show database information
- **DESCRIBE**: Describe table structure
- **EXPLAIN**: Explain query execution plan

### Return Formats

1. **JSON Format** (default):
```json
{
  "status": "success",
  "database_type": "PostgreSQL",
  "query_type": "SELECT",
  "row_count": 3,
  "columns": ["id", "name", "email"],
  "data": [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"}
  ]
}
```

2. **Table Format**:
```
id | name | email
---|------|------------------
1  | John | john@example.com
2  | Jane | jane@example.com

(2 rows)
```

3. **Raw Format**:
```
Columns: ['id', 'name', 'email']
Rows (2):
  1: [1, 'John', 'john@example.com']
  2: [2, 'Jane', 'jane@example.com']
```

## Agent Instructions

Provide clear instructions for database operations:

```yaml
agents:
  - name: Database Specialist
    instructions: >
      You are a database specialist who works with multiple database types. When using the sql_query tool:
      
      **Query Types:**
      - SELECT: Retrieve data from tables
      - INSERT: Add new records to tables
      - UPDATE: Modify existing records
      - DELETE: Remove records from tables
      
      **Database-Specific Considerations:**
      - PostgreSQL: Use standard SQL syntax
      - MySQL: Be aware of MySQL-specific functions and syntax
      - SQLite: Use SQLite-compatible syntax
      - SQL Server: Use T-SQL syntax when needed
      
      **Best Practices:**
      - Use parameterized queries when possible
      - Include appropriate WHERE clauses for UPDATE/DELETE
      - Use LIMIT clauses for large result sets
      - Handle errors gracefully and provide meaningful messages
      - Choose appropriate return format based on use case
      
      **Security:**
      - Never execute DROP, TRUNCATE, or ALTER statements unless explicitly allowed
      - Validate query types match the intended operation
      - Use appropriate timeouts for long-running queries
    model: gpt-4o
    tools:
      - sql_query
```

## Security Best Practices

### 1. **Environment Variables**
Store database credentials in environment variables:

```yaml
tools:
  - name: secure_db
    module: gnosari.tools.builtin.sql_query
    class: SQLQueryTool
    args:
      database_url: ${DATABASE_URL}
```

:::tip Environment Variables
Use environment variables for all sensitive database credentials. This keeps your configuration secure and makes it easier to manage different environments.
:::

### 2. **Schema Restrictions**
Limit access to specific schemas:

```yaml
args:
  allowed_schemas: ["public", "analytics"]
  blocked_keywords: ["TRUNCATE", "DROP TABLE", "ALTER USER"]
```

### 3. **Unsafe Operations**
Control dangerous operations:

```yaml
args:
  enable_unsafe_operations: false  # Production
  enable_unsafe_operations: true   # Development only
```

### 4. **Connection Security**
Use SSL connections in production:

```yaml
args:
  database_url: postgresql://user:pass@host:5432/db?sslmode=require
```

:::warning SQL Safety
The tool includes basic safety checks, but always validate SQL queries before execution. Never allow untrusted users to execute arbitrary SQL.
:::

## Database-Specific Configuration

### PostgreSQL
```yaml
args:
  database_url: postgresql://user:pass@host:5432/db
  pool_size: 10
  query_timeout: 60
```

### MySQL
```yaml
args:
  database_url: mysql://user:pass@host:3306/db
  pool_size: 15
  query_timeout: 45
```

### SQLite
```yaml
args:
  database_url: sqlite:///path/to/database.db
  query_timeout: 10
  # Note: SQLite doesn't support connection pooling
```

### SQL Server
```yaml
args:
  database_url: mssql://user:pass@host:1433/db
  pool_size: 10
  query_timeout: 60
```

## Error Handling

The SQL query tool provides comprehensive error handling:

- **Connection Errors**: Database connectivity issues
- **SQL Errors**: Syntax and execution errors
- **Timeout Errors**: Long-running query protection
- **Permission Errors**: Database access restrictions
- **Data Type Errors**: Result processing issues
- **Validation Errors**: Query safety violations

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify database URL format
   - Check network connectivity
   - Ensure database server is running
   - Verify credentials and permissions

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

5. **Database-Specific Issues**
   - **PostgreSQL**: Check SSL mode and connection parameters
   - **MySQL**: Verify charset and connection timeout settings
   - **SQLite**: Ensure file permissions and path accessibility
   - **SQL Server**: Check authentication mode and port configuration

### Debug Mode

Use debug mode to see detailed database query logs:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Database Debugging
Debug mode shows detailed SQL query execution information, including connection details, query execution time, and result processing.
:::

## Performance Optimization

### Connection Pooling
Configure appropriate pool settings based on your workload:

```yaml
args:
  pool_size: 10        # Base connections
  max_overflow: 20     # Additional connections under load
  pool_timeout: 30     # Wait time for connection
  pool_recycle: 3600   # Connection refresh interval
```

### Query Optimization
- Use appropriate indexes
- Limit result sets with LIMIT clauses
- Use efficient WHERE clauses
- Consider query complexity and timeout settings

## Related Tools

- [MySQL Query Tool](mysql-query) - Specialized MySQL operations
- [API Request Tool](api-request) - For external service integration
- [Delegate Agent Tool](delegate-agent) - For multi-agent coordination
- [Knowledge Query Tool](knowledge-query) - For information retrieval

The SQL Query Tool is the most versatile database tool in Gnosari AI Teams, supporting virtually any database through SQLAlchemy. Use it to build agents that can work with multiple database types, perform complex data operations, and integrate seamlessly with your existing database infrastructure.