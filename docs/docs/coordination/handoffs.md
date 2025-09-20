---
sidebar_position: 2
---

# Handoffs

Handoffs in Gnosari AI Teams are mechanisms for transferring complete control from one agent to another. When an agent performs a handoff, the receiving agent takes over the conversation and doesn't return control to the original agent.

## What are Handoffs?

Handoffs are:
- **Control Transfer**: Complete transfer of conversation control
- **No Return**: The receiving agent doesn't respond back to the original agent
- **Escalation Mechanism**: For when an agent can't handle a request
- **Specialization Transfer**: Moving to agents with specific expertise
- **One-Way Communication**: From sender to receiver only

:::info Handoffs vs Delegation
Handoffs transfer complete control and don't return responses, while delegation assigns tasks and receives responses back.
:::

## Handoff Configuration

Handoffs are configured using the `can_transfer_to` property in agent configurations:

```yaml
agents:
  - name: CustomerService
    instructions: "Handle customer inquiries and escalate when needed"
    model: gpt-4o
    can_transfer_to: ["TechnicalSupport", "BillingSupport"]  # Handoff targets

  - name: TechnicalSupport
    instructions: "Handle technical support issues"
    model: gpt-4o
    can_transfer_to: ["SeniorEngineer"]  # Can escalate further

  - name: BillingSupport
    instructions: "Handle billing and account issues"
    model: gpt-4o

  - name: SeniorEngineer
    instructions: "Handle complex technical issues"
    model: gpt-4o
```

:::tip Handoff Targets
The `can_transfer_to` list defines which agents this agent can hand off control to. The receiving agents don't need special configuration.
:::

## When to Use Handoffs

### 1. **Escalation Scenarios**
When an agent encounters issues beyond their capabilities:

```yaml
agents:
  - name: FirstLevelSupport
    instructions: >
      Handle basic customer support issues. If you encounter complex technical problems,
      escalate to TechnicalSupport. For billing issues, escalate to BillingSupport.
    model: gpt-4o
    can_transfer_to: ["TechnicalSupport", "BillingSupport"]

  - name: TechnicalSupport
    instructions: "Handle technical support issues and complex problems"
    model: gpt-4o
    can_transfer_to: ["SeniorEngineer"]  # Can escalate further

  - name: BillingSupport
    instructions: "Handle billing, payments, and account issues"
    model: gpt-4o
```

### 2. **Specialization Transfer**
When an agent needs to transfer to a specialist:

```yaml
agents:
  - name: GeneralAssistant
    instructions: >
      Help users with general questions. For legal questions, transfer to LegalExpert.
      For medical questions, transfer to MedicalExpert.
    model: gpt-4o
    can_transfer_to: ["LegalExpert", "MedicalExpert"]

  - name: LegalExpert
    instructions: "Provide legal advice and information"
    model: gpt-4o

  - name: MedicalExpert
    instructions: "Provide medical information and guidance"
    model: gpt-4o
```

### 3. **Authority Levels**
When transferring to agents with higher authority:

```yaml
agents:
  - name: SalesRepresentative
    instructions: >
      Handle sales inquiries. For large deals or special pricing, transfer to SalesManager.
      For contract negotiations, transfer to LegalTeam.
    model: gpt-4o
    can_transfer_to: ["SalesManager", "LegalTeam"]

  - name: SalesManager
    instructions: "Handle large deals, special pricing, and sales management"
    model: gpt-4o
    can_transfer_to: ["SalesDirector"]  # Can escalate further

  - name: LegalTeam
    instructions: "Handle contract negotiations and legal matters"
    model: gpt-4o
```

## Handoff Escalation Data

When handoffs occur, escalation data is automatically captured:

```python
class HandoffEscalationData(BaseModel):
    reason: str                    # Why the handoff occurred
    from_agent: str               # Agent that initiated the handoff
    to_agent: str                 # Agent receiving the handoff
    context: Optional[str]        # Additional context information
    conversation_history: Optional[str]  # Relevant conversation history
```

:::info Automatic Escalation Tracking
The system automatically tracks handoff reasons, context, and conversation history for monitoring and debugging purposes.
:::

## Handoff Examples

### Example 1: Customer Support Escalation

```yaml
name: Customer Support Team

agents:
  - name: FrontDesk
    instructions: >
      Welcome customers and handle basic inquiries. For technical issues,
      transfer to TechnicalSupport. For billing questions, transfer to Billing.
      For complaints, transfer to Manager.
    model: gpt-4o
    can_transfer_to: ["TechnicalSupport", "Billing", "Manager"]

  - name: TechnicalSupport
    instructions: >
      Handle technical support issues. For complex problems beyond your expertise,
      transfer to SeniorEngineer.
    model: gpt-4o
    can_transfer_to: ["SeniorEngineer"]

  - name: Billing
    instructions: "Handle billing, payments, and account issues"
    model: gpt-4o

  - name: Manager
    instructions: "Handle complaints, escalations, and management issues"
    model: gpt-4o

  - name: SeniorEngineer
    instructions: "Handle complex technical issues and system problems"
    model: gpt-4o
```

### Example 2: Content Creation Workflow

```yaml
name: Content Creation Team

agents:
  - name: ContentCoordinator
    instructions: >
      Coordinate content creation requests. For technical content, transfer to TechnicalWriter.
      For marketing content, transfer to MarketingWriter. For legal content, transfer to LegalWriter.
    model: gpt-4o
    can_transfer_to: ["TechnicalWriter", "MarketingWriter", "LegalWriter"]

  - name: TechnicalWriter
    instructions: >
      Create technical documentation and content. For complex technical topics,
      transfer to SubjectMatterExpert.
    model: gpt-4o
    can_transfer_to: ["SubjectMatterExpert"]

  - name: MarketingWriter
    instructions: "Create marketing content, copy, and promotional materials"
    model: gpt-4o

  - name: LegalWriter
    instructions: "Create legal content, terms, and compliance materials"
    model: gpt-4o

  - name: SubjectMatterExpert
    instructions: "Provide expert knowledge for complex technical topics"
    model: gpt-4o
```

### Example 3: Sales Process

```yaml
name: Sales Team

agents:
  - name: SalesRep
    instructions: >
      Handle initial sales inquiries. For enterprise deals, transfer to EnterpriseSales.
      For technical questions, transfer to SalesEngineer. For pricing negotiations,
      transfer to SalesManager.
    model: gpt-4o
    can_transfer_to: ["EnterpriseSales", "SalesEngineer", "SalesManager"]

  - name: EnterpriseSales
    instructions: >
      Handle enterprise sales and large deals. For complex technical requirements,
      transfer to SalesEngineer. For contract negotiations, transfer to LegalTeam.
    model: gpt-4o
    can_transfer_to: ["SalesEngineer", "LegalTeam"]

  - name: SalesEngineer
    instructions: "Handle technical sales questions and product demonstrations"
    model: gpt-4o

  - name: SalesManager
    instructions: "Handle pricing negotiations and sales management"
    model: gpt-4o

  - name: LegalTeam
    instructions: "Handle contract negotiations and legal matters"
    model: gpt-4o
```

## Handoff Best Practices

### 1. **Clear Escalation Criteria**
Define when handoffs should occur:

```yaml
agents:
  - name: SupportAgent
    instructions: >
      Handle customer support issues. Transfer to TechnicalSupport when:
      - The issue involves system errors or bugs
      - The customer mentions technical problems
      - You cannot resolve the issue with standard procedures
      
      Transfer to Billing when:
      - The issue involves payments or charges
      - The customer has billing questions
      - Account access issues are mentioned
    model: gpt-4o
    can_transfer_to: ["TechnicalSupport", "Billing"]
```

### 2. **Appropriate Handoff Targets**
Choose the right agents for handoffs:

```yaml
agents:
  - name: GeneralAssistant
    instructions: >
      Help users with general questions. Transfer to specialists when:
      - Legal questions → LegalExpert
      - Medical questions → MedicalExpert
      - Technical questions → TechnicalExpert
    model: gpt-4o
    can_transfer_to: ["LegalExpert", "MedicalExpert", "TechnicalExpert"]
```

### 3. **Context Preservation**
Ensure receiving agents have necessary context:

```yaml
agents:
  - name: FirstLevelSupport
    instructions: >
      When transferring to specialists, provide clear context about:
      - The customer's issue
      - What you've already tried
      - Any relevant customer information
      - The urgency level
    model: gpt-4o
    can_transfer_to: ["TechnicalSupport", "Billing"]
```

## Handoff Monitoring

### Debug Mode
Use debug mode to see detailed handoff information:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Handoff Debugging
Debug mode shows detailed handoff information including:
- Which agent initiated the handoff
- Which agent received the handoff
- The reason for the handoff
- Context and conversation history
:::

### Handoff Logging
The system automatically logs handoff events:

```
🤝 HANDOFF ESCALATION: CustomerService → TechnicalSupport
📋 Reason: Complex technical issue requiring specialist knowledge
📝 Context: Customer experiencing system crashes with error codes
```

## Handoff Limitations

### 1. **No Return Communication**
Handoffs are one-way - the receiving agent doesn't respond back to the original agent.

### 2. **Context Transfer**
While context is preserved, the original agent loses control of the conversation.

### 3. **Escalation Chains**
Be careful with long escalation chains that might confuse users.

:::warning Handoff Considerations
- Handoffs are permanent - the original agent doesn't regain control
- Use handoffs for escalation and specialization, not for task distribution
- Consider user experience when designing handoff flows
:::

## Related Topics

- [Delegation](delegation) - Learn about task assignment and response handling
- [Orchestration](orchestration) - Understand overall coordination patterns
- [Agents](../agents) - Learn about individual agent configuration
- [Teams](../teams) - Understand team structure and coordination
- [Quickstart](../quickstart) - Create your first team with handoffs

## Next Steps

Now that you understand handoffs, learn about the complementary mechanism:

- [Delegation](delegation) - Task assignment with response handling
- [Orchestration](orchestration) - Overall coordination strategies
- [Agents](../agents) - Configure agents for handoffs
- [Teams](../teams) - Set up teams with handoff capabilities
- [Quickstart](../quickstart) - Build your first team with handoffs