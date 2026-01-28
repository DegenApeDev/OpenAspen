# LM Studio Quick Start - 5 Minutes ⚡

## Step 1: Start LM Studio (2 min)

1. Open **LM Studio**
2. Go to **"Local Server"** tab (left sidebar)
3. Select your model from dropdown
4. Click **"Start Server"**
5. Verify: `Server running on http://localhost:1234` ✅

## Step 2: Run OpenAspen Example (1 min)

```bash
cd /home/degendev/Dev/Agents/OpenAspen
source venv/bin/activate.fish
python examples/lmstudio_example.py
```

## Step 3: Done! 🎉

Your OpenAspen tree is now powered by your local LM Studio model - **completely free and private**!

---

## Quick Code Template

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config

async def my_function(input: str) -> str:
    """Your custom function"""
    return f"Processed: {input}"

async def main():
    # Configure LM Studio
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="lmstudio",
            api_base="http://localhost:1234/v1",
        )
    }
    
    # Create tree
    tree = OpenAspenTree(llm_configs=llm_configs)
    
    # Add agent
    agent = tree.grow_branch(
        "my_agent",
        description="Does cool stuff",
        llm_provider="lmstudio"
    )
    
    # Add skill
    await tree.spawn_leaf(agent, "my_skill", my_function, "Description")
    
    # Use it
    await tree.index_tree()
    result = await tree.execute("Your query here")
    print(result)

asyncio.run(main())
```

---

## Troubleshooting

**Problem**: Connection refused  
**Fix**: Make sure LM Studio server is started (green "Running" indicator)

**Problem**: Slow responses  
**Fix**: Use a smaller model (7B instead of 13B) or enable GPU acceleration

**Problem**: Out of memory  
**Fix**: Use a more quantized model (Q4_K_M instead of Q8_0)

---

## Why LM Studio?

✅ **$0 cost** - Completely free  
✅ **100% private** - Data never leaves your machine  
✅ **Works offline** - No internet required  
✅ **Fast** - With GPU acceleration  

---

## Next Steps

📖 Full guide: `docs/LMSTUDIO_SETUP.md`  
🔧 Examples: `examples/lmstudio_example.py`  
💡 Mix providers: Use LM Studio for simple tasks, cloud APIs for complex ones

**You're ready to build with free, local AI! 🚀**
