# Examples

This section contains practical examples of Gnosari AI Teams configurations and use cases.

## Team Configurations

### Database Administration Team
A comprehensive team for database administration tasks including schema management, query optimization, and data analysis.

**File:** `examples/database_admin_team.yaml`

**Features:**
- MySQL database operations
- Schema analysis and optimization
- Data migration assistance
- Performance monitoring

### Universal Database Team
A versatile team that can work with multiple database systems and perform various database-related tasks.

**File:** `examples/universal_database_team.yaml`

**Features:**
- Multi-database support
- Query optimization
- Data analysis and reporting
- Database maintenance

### Team Designer
An intelligent team that helps design and configure other AI teams based on requirements.

**File:** `examples/team_designer.yaml`

**Features:**
- Team architecture design
- Configuration generation
- Best practices recommendations
- Team optimization suggestions

### Neomanex Demo
A demonstration team showcasing various capabilities of the Gnosari platform.

**File:** `examples/neomanex_demo.yaml`

**Features:**
- Multi-agent coordination
- Tool integration
- Knowledge base utilization
- Real-time collaboration

## Getting Started with Examples

1. **Choose an example** that matches your use case
2. **Review the configuration** to understand the team structure
3. **Customize the settings** for your specific needs
4. **Run the team** using the Gnosari CLI

### Running an Example

```bash
# Run a specific team configuration
gnosari --config "examples/database_admin_team.yaml" --message "Analyze the database schema" --stream

# Run with custom model settings
gnosari --config "examples/team_designer.yaml" --message "Design a team for web scraping" --model "gpt-4o" --temperature 0.3
```

## Creating Your Own Examples

When creating your own team configurations:

1. **Start with a simple team** - Begin with 2-3 agents
2. **Define clear roles** - Each agent should have a specific purpose
3. **Configure tools appropriately** - Only include tools that agents will actually use
4. **Test incrementally** - Add complexity gradually
5. **Document your configuration** - Include comments explaining your choices

## Contributing Examples

We welcome contributions of new examples! When submitting:

1. **Include comprehensive documentation** explaining the use case
2. **Provide clear instructions** for running the example
3. **Test thoroughly** to ensure the configuration works
4. **Follow naming conventions** (use descriptive names)
5. **Add appropriate comments** in the YAML configuration

For more information on team configuration, see the [Teams documentation](teams.md).