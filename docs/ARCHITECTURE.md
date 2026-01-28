# OpenAspen Architecture

## Overview

OpenAspen implements a tree-structured agent framework inspired by aspen groves, where individual trees (agents) share a common root system (RAG database) for enhanced collaboration and context sharing.

## Core Design Principles

1. **Hierarchical Organization**: Agents (branches) contain skills (leaves) in a tree structure
2. **Shared Knowledge**: All agents access a common vector database for cross-context awareness
3. **Multi-LLM Flexibility**: Route queries to different LLMs based on cost, speed, or capability
4. **Async-First**: Non-blocking execution for high performance
5. **Type Safety**: Pydantic models ensure runtime correctness

## Component Architecture

### 1. TreeNode (Abstract Base)

The foundation of all tree components.

```python
class TreeNode(ABC):
    - id: Unique identifier
    - name: Human-readable name
    - parent: Reference to parent node
    - children: List of child nodes
    - llm_provider: Preferred LLM for this node
    - rag_context: Node-specific RAG metadata
    
    Methods:
    - execute(input_data): Abstract method for execution
    - add_child(child): Add a child node
    - get_path(): Get full path from root
    - get_depth(): Calculate depth in tree
```

**Design Rationale**: Abstract base ensures consistent interface across all tree components while allowing specialized implementations.

### 2. Leaf (Skill/Tool)

Represents a single executable skill or tool.

```python
class Leaf(TreeNode):
    - description: Skill description for RAG
    - tool_func: Actual function to execute
    - is_async: Whether function is async
    - parameters: Extracted function parameters
    
    Methods:
    - execute(input_data): Run the tool function
    - get_embedding_text(): Generate text for RAG indexing
```

**Key Features**:
- Automatic async/sync detection
- Parameter extraction via introspection
- Error handling with structured responses
- RAG-optimized text generation

### 3. Branch (Agent)

Represents an agent that manages multiple skills.

```python
class Branch(TreeNode):
    - description: Agent description
    - system_prompt: LLM system prompt
    - temperature: LLM temperature setting
    - max_tokens: Token limit
    
    Methods:
    - add_leaf(name, func, desc): Add a skill
    - execute(input_data): Route to best leaf via LLM
    - _find_relevant_leaves(query, rag_db): RAG-based skill discovery
    - _execute_with_llm(input, leaves, router): LLM-guided execution
```

**Execution Flow**:
1. Query arrives at branch
2. RAG search finds relevant leaves
3. LLM selects best leaf for query
4. Leaf executes and returns result

### 4. OpenAspenTree (Orchestrator)

The main tree that manages all branches and shared resources.

```python
class OpenAspenTree:
    - llm_router: Multi-LLM routing system
    - shared_rag_db: Group RAG vector store
    - branches: List of top-level agents
    - _execution_history: Query history
    
    Methods:
    - add_branch(name, desc, llm): Add new agent
    - spawn_leaf(branch, name, func): Add skill to agent
    - execute(query): Intelligent query routing
    - index_tree(): Index all skills in RAG
    - _find_best_branch(query): RAG-based branch selection
```

**Orchestration Logic**:
1. Query received
2. RAG search across all branches
3. Select branch with highest relevance score
4. Delegate to branch for execution
5. Record in execution history

## LLM Router Architecture

### Multi-Provider Support

```python
class LLMRouter:
    - configs: Dict of LLM configurations
    - _llm_cache: Cached LLM instances
    
    Routing Strategies:
    - route_by_cost(max_cost): Cheapest within budget
    - route_by_speed(min_speed): Fastest available
    - route_by_skill(skill_type): Best for task type
```

**Supported Providers**:
- **OpenAI**: GPT-4, GPT-3.5 (cloud, high quality)
- **Anthropic**: Claude 3 (cloud, creative tasks)
- **Grok**: X.AI's Grok (cloud, fast)
- **Ollama**: Local models (free, private)
- **LM Studio**: Local models (free, GUI)

**Provider Selection Matrix**:
| Use Case | Recommended Provider | Rationale |
|----------|---------------------|-----------|
| Coding | OpenAI, Anthropic | Best code understanding |
| Creative Writing | Anthropic, Grok | Strong creative abilities |
| Fast Responses | Grok, Ollama | Optimized for speed |
| Privacy/Local | Ollama, LM Studio | No data leaves machine |
| Cost-Sensitive | Ollama, LM Studio | Free to run |

## Group RAG System

### Vector Store Architecture

```python
class GroupRAGStore:
    - persist_directory: ChromaDB storage path
    - embedding_manager: Handles embeddings
    - _vectorstore: ChromaDB instance
    
    Methods:
    - index_leaf(leaf, branch): Add leaf to index
    - index_branch(branch): Recursively index branch
    - similarity_search(query, k, filter): Find relevant docs
    - get_sibling_context(branch, query): Cross-branch search
```

**Indexing Strategy**:
- Each leaf generates embedding text from:
  - Skill name
  - Description
  - Full path in tree
  - Parameter signatures
- Metadata includes:
  - Branch name (for filtering)
  - Leaf name
  - Type (leaf/branch)
  - Full path

**Search Strategy**:
1. Embed query using same embedding model
2. Similarity search in vector space
3. Filter by branch if needed
4. Return top-k most relevant skills
5. Score aggregation for branch selection

### Embedding Manager

```python
class EmbeddingManager:
    - provider: Embedding provider (default: OpenAI)
    - model: Embedding model (default: text-embedding-3-small)
    
    Methods:
    - embed_documents(texts): Batch embed
    - embed_query(text): Single query embed
```

**Why OpenAI Embeddings**:
- High quality semantic understanding
- Fast inference
- Good cost/performance ratio
- 1536 dimensions for rich representation

## Execution Flow

### Query Execution Pipeline

```
User Query
    ↓
OpenAspenTree.execute()
    ↓
RAG Search (find best branch)
    ↓
Branch.execute()
    ↓
RAG Search (find relevant leaves)
    ↓
LLM Decision (select best leaf)
    ↓
Leaf.execute()
    ↓
Tool Function Execution
    ↓
Result Aggregation
    ↓
Return to User
```

### Error Handling Strategy

1. **Leaf Level**: Catch exceptions, return structured error
2. **Branch Level**: Fallback to first relevant leaf if LLM fails
3. **Tree Level**: Return error response with context
4. **Logging**: All errors logged with full context

## API Server Architecture

### FastAPI Integration

```python
create_app(config_file):
    - Loads tree from JSON config
    - Initializes LLM providers
    - Sets up CORS middleware
    - Defines OpenAI-compatible endpoints
```

**Endpoints**:
- `/v1/chat/completions`: OpenAI-compatible chat
- `/v1/models`: Model listing
- `/tree/info`: Tree metadata
- `/tree/visualize`: ASCII visualization
- `/tree/execute`: Direct execution
- `/health`: Health check

**Why OpenAI-Compatible**:
- Drop-in replacement for existing apps
- Works with OpenAI SDKs
- Familiar API for developers
- Easy integration with tools

## CLI Architecture

### Command Structure

```
openaspen
├── init: Create new tree config
├── run: Execute tree with query
├── visualize: Show tree structure
└── info: Display tree metadata
```

**Design Philosophy**:
- Simple, intuitive commands
- JSON-based configuration
- Interactive mode for exploration
- Pipe-friendly output

## Performance Considerations

### Optimization Strategies

1. **LLM Caching**: Reuse initialized LLM instances
2. **Async Execution**: Non-blocking I/O throughout
3. **Lazy Loading**: Load resources only when needed
4. **Batch Operations**: Group RAG operations where possible
5. **Connection Pooling**: Reuse HTTP connections

### Scalability

**Current Limits**:
- Single machine execution
- In-memory tree structure
- ChromaDB file-based storage

**Future Scalability**:
- Distributed execution (Ray, Celery)
- Database-backed tree storage
- Cloud vector stores (Pinecone, Weaviate)
- Horizontal scaling of branches

## Security Considerations

1. **API Keys**: Environment variables, never hardcoded
2. **Input Validation**: Pydantic models validate all inputs
3. **Rate Limiting**: TODO - implement in API server
4. **Sandboxing**: TODO - isolate tool execution
5. **Audit Logging**: Execution history tracked

## Testing Strategy

### Test Coverage

1. **Unit Tests**: Each component tested in isolation
2. **Integration Tests**: Component interactions tested
3. **Async Tests**: pytest-asyncio for async code
4. **Mocking**: Mock LLM calls for deterministic tests

### Test Structure

```
tests/
├── test_core.py: TreeNode, Branch, Leaf tests
├── test_llm.py: LLM router and provider tests
├── test_tree.py: OpenAspenTree orchestration tests
└── test_rag.py: RAG and embedding tests
```

## Extension Points

### Adding New LLM Providers

1. Add provider to `LLMProvider` enum
2. Add defaults to `PROVIDER_DEFAULTS`
3. Implement creation logic in `LLMRouter._create_llm()`
4. Add tests

### Adding New Vector Stores

1. Create new store class implementing same interface
2. Update `GroupRAGStore` or create alternative
3. Add configuration options
4. Update documentation

### Custom Node Types

1. Inherit from `TreeNode`
2. Implement `execute()` method
3. Add to tree via `add_child()`
4. Optionally add convenience methods to `OpenAspenTree`

## Future Architecture Enhancements

1. **Streaming Responses**: Real-time output streaming
2. **Agent Memory**: Persistent conversation context
3. **Tool Calling**: Native function calling support
4. **Workflow Graphs**: LangGraph integration for complex flows
5. **Monitoring**: Metrics, tracing, observability
6. **Caching**: Response caching for common queries
7. **Load Balancing**: Distribute across multiple LLM instances
