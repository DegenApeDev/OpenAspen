# Getting Started with OpenAspen

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
# Clone the repository
cd /home/degendev/Dev/Agents/OpenAspen

# Install with Poetry (recommended)
poetry install

# Or use the setup script
bash scripts/setup_dev.sh
```

### Step 2: Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Add your keys:
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
# Optional: GROK_API_KEY, etc.
```

### Step 3: Run Your First Example

```bash
# Run the basic example
poetry run python examples/basic_tree.py

# Or use make
make run-example
```

## 📖 5-Minute Tutorial

### Create a Simple Agent Tree

Create `my_first_agent.py`:

```python
import asyncio
import os
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config

# Define a simple skill
async def greet_user(name: str) -> str:
    """Greet a user by name"""
    return f"Hello, {name}! Welcome to OpenAspen! 🌲"

async def calculate_sum(numbers: str) -> dict:
    """Calculate sum of comma-separated numbers"""
    nums = [float(n.strip()) for n in numbers.split(",")]
    return {"numbers": nums, "sum": sum(nums)}

async def main():
    # 1. Configure LLM (using OpenAI)
    llm_configs = {
        "openai": create_llm_config(
            provider="openai",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    }
    
    # 2. Create the tree
    tree = OpenAspenTree(
        llm_configs=llm_configs,
        name="MyFirstTree"
    )
    
    # 3. Add a branch (agent) for greetings
    greeting_agent = tree.grow_branch(
        "greeting_assistant",
        description="Handles user greetings and welcomes",
        llm_provider="openai",
        system_prompt="You are a friendly greeter."
    )
    
    # 4. Add a branch for calculations
    math_agent = tree.grow_branch(
        "math_assistant",
        description="Performs mathematical calculations",
        llm_provider="openai",
        system_prompt="You are a helpful math assistant."
    )
    
    # 5. Add skills (leaves) to branches
    await tree.spawn_leaf(
        greeting_agent,
        "greet",
        greet_user,
        "Greet users by name"
    )
    
    await tree.spawn_leaf(
        math_agent,
        "sum_numbers",
        calculate_sum,
        "Calculate the sum of numbers"
    )
    
    # 6. Index the tree for RAG-based routing
    await tree.index_tree()
    
    # 7. Visualize the tree
    print("\n🌲 Your Tree Structure:")
    print(tree.visualize())
    print()
    
    # 8. Execute queries
    print("📊 Testing Queries:\n")
    
    # Query 1: Should route to greeting_assistant
    result1 = await tree.execute("Please greet Alice")
    print(f"Query: 'Please greet Alice'")
    print(f"Result: {result1}\n")
    
    # Query 2: Should route to math_assistant
    result2 = await tree.execute("What is the sum of 10, 20, 30?")
    print(f"Query: 'What is the sum of 10, 20, 30?'")
    print(f"Result: {result2}\n")
    
    # 9. View execution history
    print("📜 Execution History:")
    for record in tree.get_execution_history():
        print(f"  - Query: {record['query'][:40]}...")
        print(f"    Branch: {record['branch']}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
poetry run python my_first_agent.py
```

## 🎯 Common Use Cases

### Use Case 1: Multi-Domain Assistant

```python
# Create specialized agents for different domains
customer_support = tree.grow_branch("customer_support", llm_provider="openai")
technical_help = tree.grow_branch("technical_support", llm_provider="anthropic")
sales = tree.grow_branch("sales_assistant", llm_provider="grok")

# Add domain-specific skills
await tree.spawn_leaf(customer_support, "check_order", check_order_func)
await tree.spawn_leaf(technical_help, "debug_issue", debug_func)
await tree.spawn_leaf(sales, "product_info", product_info_func)

# Tree automatically routes to the right agent
await tree.execute("What's my order status?")  # → customer_support
await tree.execute("My app is crashing")       # → technical_help
await tree.execute("Tell me about pricing")    # → sales
```

### Use Case 2: Cost-Optimized System

```python
# Use expensive LLM for complex tasks
complex_agent = tree.grow_branch("complex_tasks", llm_provider="openai")

# Use free local LLM for simple tasks
simple_agent = tree.grow_branch("simple_tasks", llm_provider="ollama")

# Saves money while maintaining quality where it matters
```

### Use Case 3: API Server

```python
# server.py
from openaspen.server.api import create_app
import uvicorn

app = create_app(config_file="tree.json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Then use from any language:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "openaspen", "messages": [{"role": "user", "content": "Hello"}]}'
```

## 🛠️ Development Commands

```bash
# Run tests
make test

# Format code
make format

# Lint code
make lint

# Run example
make run-example

# Start API server
make run-server

# Clean build artifacts
make clean
```

## 📚 Next Steps

1. **Explore Examples**: Check `examples/` directory
   - `basic_tree.py` - Simple getting started
   - `advanced_tree.py` - Production-ready system
   - `server_example.py` - API deployment

2. **Read Documentation**:
   - `README.md` - Overview and features
   - `docs/QUICKSTART.md` - Detailed tutorial
   - `docs/ARCHITECTURE.md` - Deep dive

3. **Try the CLI**:
   ```bash
   openaspen init --name my_tree
   openaspen run tree.json --interactive
   ```

4. **Build Your Own**:
   - Define your skills as functions
   - Create agents for different domains
   - Let RAG handle the routing

## 🐛 Troubleshooting

### "No module named 'openaspen'"
```bash
# Make sure you're in the poetry shell
poetry shell
# Or prefix commands with poetry run
poetry run python your_script.py
```

### "API key not found"
```bash
# Check your .env file exists and has the key
cat .env | grep OPENAI_API_KEY

# Or set it directly
export OPENAI_API_KEY=sk-your-key
```

### "ChromaDB errors"
```bash
# Install ChromaDB explicitly
poetry add chromadb
```

### "Ollama connection failed"
```bash
# Make sure Ollama is running
ollama serve

# Pull a model
ollama pull llama2
```

## 💡 Tips

1. **Start Simple**: Begin with one branch and one leaf
2. **Use Local LLMs**: Ollama is free for development
3. **Test Functions First**: Test your skills before adding to tree
4. **Check Logs**: Set `LOG_LEVEL=DEBUG` for detailed output
5. **Use RAG**: Let the tree find the right agent automatically

## 🎓 Learning Path

**Beginner** (1 hour):
1. Run `examples/basic_tree.py`
2. Modify it with your own skills
3. Try the CLI commands

**Intermediate** (2-3 hours):
1. Study `examples/advanced_tree.py`
2. Build a multi-agent system
3. Deploy the API server

**Advanced** (1 day):
1. Read `docs/ARCHITECTURE.md`
2. Extend with custom node types
3. Contribute to the project

## 🤝 Getting Help

- **Documentation**: Check `docs/` folder
- **Examples**: See `examples/` folder
- **Issues**: GitHub Issues for bugs
- **Discussions**: GitHub Discussions for questions

## 🌟 Quick Reference

### Create Tree
```python
tree = OpenAspenTree(llm_configs=configs)
```

### Add Agent
```python
agent = tree.grow_branch("name", description="...", llm_provider="openai")
```

### Add Skill
```python
await tree.spawn_leaf(agent, "skill_name", function, "description")
```

### Execute
```python
result = await tree.execute("your query")
```

### Visualize
```python
print(tree.visualize())
```

---

**You're ready to grow your first OpenAspen tree! 🌲**

Happy coding!
