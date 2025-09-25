---
sidebar_position: 1
---

# What is Gnosari?

**Gnosari AI Teams** is a next-generation framework for orchestrating multi-agent teams using Large Language Models. Built for production environments, Gnosari enables AI agents to collaborate seamlessly through real-time delegation, background processing, and human-in-the-loop capabilities.

## Core Philosophy

Gnosari is designed around three fundamental principles:

- **Production-Ready**: Built-in async processing, monitoring, and scalability
- **Human-Centric**: Seamless escalation to human operators when needed
- **Developer-Friendly**: Simple YAML configuration with powerful capabilities

## Key Capabilities

### 🤖 **Multi-Agent Orchestration**
- Real-time task delegation between agents
- Streaming responses for live collaboration
- Dynamic agent coordination patterns

### ⚡ **Async Execution**
- Background processing with Celery + Redis
- Non-blocking operations for better performance
- Scalable worker management

### 👥 **Human-in-the-Loop**
- Escalate complex tasks to human operators
- Seamless AI-to-human handoffs
- Collaborative decision making

### 🔧 **Dynamic Tool Discovery**
- Built-in tools (API requests, database queries, file operations)
- MCP (Model Context Protocol) server integration
- Extensible tool ecosystem

### 📚 **Knowledge Integration**
- RAG capabilities with Embedchain
- Multiple data sources (websites, documents, videos)
- Context-aware agent responses

## Gnosari vs CrewAI

| Feature | Gnosari | CrewAI |
|---------|---------|---------|
| **Async Processing** | ✅ Built-in Celery + Redis | ❌ Synchronous only |
| **Human-in-the-Loop** | ✅ Native escalation support | ❌ Not supported |
| **Background Execution** | ✅ Teams run independently | ❌ Blocking operations |
| **Streaming Responses** | ✅ Real-time collaboration | ❌ Batch processing |
| **Production Monitoring** | ✅ Flower UI + metrics | ❌ Limited monitoring |
| **Scalability** | ✅ Horizontal scaling | ❌ Single-threaded |
| **Tool Discovery** | ✅ MCP server integration | ❌ Static tool definitions |
| **Multi-Provider LLMs** | ✅ Per-agent model selection | ✅ Supported |
| **YAML Configuration** | ✅ Declarative setup | ✅ Supported |
| **Task Delegation** | ✅ Real-time delegation | ✅ Supported |

## Why Choose Gnosari?

### **For Production Teams**
- **Scalability**: Handle high-volume workloads with async processing
- **Reliability**: Built-in monitoring and error handling
- **Flexibility**: Escalate to humans when AI reaches limits

### **For Developers**
- **Simplicity**: Configure complex teams with simple YAML
- **Extensibility**: Add custom tools and agents easily
- **Performance**: Non-blocking operations for better user experience

### **For Enterprises**
- **Human Integration**: Seamless AI-human collaboration
- **Monitoring**: Full visibility into agent performance
- **Compliance**: Audit trails and escalation workflows

## Getting Started

Ready to build your first AI team? Start with our quickstart guide:

- 🚀 [Quickstart Guide](quickstart) - Get up and running in minutes
- 🤖 [Agents](agents) - Learn about agent configuration
- 👥 [Teams](teams) - Understand team orchestration
- ⚡ [Async Execution](queues/intro) - Background processing capabilities