# LM Studio Setup Guide for OpenAspen

## Overview

LM Studio is a free, local LLM runner that allows you to run models on your own hardware without any API costs. OpenAspen has built-in support for LM Studio.

## Prerequisites

1. **LM Studio installed** - Download from [lmstudio.ai](https://lmstudio.ai)
2. **A model downloaded** - Any GGUF model (Llama, Mistral, etc.)
3. **Sufficient RAM** - Depends on model size (8GB+ recommended)

## Setup Steps

### 1. Install and Launch LM Studio

1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai)
2. Install and launch the application
3. Download a model (recommended: `TheBloke/Mistral-7B-Instruct-v0.2-GGUF` or similar)

### 2. Start the Local Server

In LM Studio:
1. Click on the **"Local Server"** tab (left sidebar)
2. Select your downloaded model from the dropdown
3. Click **"Start Server"**
4. Verify it shows: `Server running on http://localhost:1234`

### 3. Configure OpenAspen

OpenAspen is pre-configured to work with LM Studio's default settings:

```python
from openaspen.llm.providers import create_llm_config

llm_configs = {
    "lmstudio": create_llm_config(
        provider="lmstudio",
        model="local-model",  # Uses whatever model is loaded
        api_base="http://localhost:1234/v1",
        temperature=0.7,
        max_tokens=2000,
    )
}
```

### 4. Run the Example

```bash
# Make sure LM Studio server is running first!
source venv/bin/activate.fish
python examples/lmstudio_example.py
```

## Configuration Options

### Default Configuration

```python
{
    "provider": "lmstudio",
    "model": "local-model",
    "api_base": "http://localhost:1234/v1",
    "cost_per_1k_tokens": 0.0,  # Free!
    "speed_score": 0.5,
    "temperature": 0.7,
    "max_tokens": 2000
}
```

### Custom Port

If you changed LM Studio's port:

```python
llm_configs = {
    "lmstudio": create_llm_config(
        provider="lmstudio",
        api_base="http://localhost:YOUR_PORT/v1",
    )
}
```

### Multiple Models

You can run multiple instances of LM Studio on different ports:

```python
llm_configs = {
    "lmstudio_fast": create_llm_config(
        provider="lmstudio",
        api_base="http://localhost:1234/v1",
        metadata={"purpose": "quick responses"}
    ),
    "lmstudio_smart": create_llm_config(
        provider="lmstudio",
        api_base="http://localhost:1235/v1",
        metadata={"purpose": "complex reasoning"}
    )
}
```

## Recommended Models

### For General Use (7B-13B parameters)
- **Mistral-7B-Instruct** - Fast, capable, good for most tasks
- **Llama-2-13B-Chat** - Balanced performance
- **Zephyr-7B-Beta** - Good instruction following

### For Coding (7B-34B parameters)
- **CodeLlama-13B-Instruct** - Specialized for code
- **Phind-CodeLlama-34B** - Excellent for programming
- **DeepSeek-Coder-33B** - Strong coding abilities

### For Reasoning (13B-70B parameters)
- **Mixtral-8x7B-Instruct** - Excellent reasoning
- **Llama-2-70B-Chat** - High quality responses (needs 48GB+ RAM)

## Performance Tips

### 1. Model Size vs Speed
- **7B models**: Fast, good for simple tasks
- **13B models**: Balanced, recommended for most use cases
- **34B+ models**: Slower but more capable

### 2. Quantization
- **Q4_K_M**: Good balance (recommended)
- **Q5_K_M**: Better quality, slightly slower
- **Q8_0**: Highest quality, slowest

### 3. Context Length
- Keep `max_tokens` reasonable (1000-2000)
- Larger context = slower responses

### 4. Hardware
- **CPU**: Works but slow
- **GPU (NVIDIA)**: Much faster with CUDA
- **GPU (Apple Silicon)**: Fast with Metal acceleration

## Troubleshooting

### Server Not Starting

**Problem**: LM Studio server won't start
**Solutions**:
- Check if port 1234 is already in use
- Try a different port in LM Studio settings
- Restart LM Studio

### Connection Refused

**Problem**: `Connection refused to http://localhost:1234`
**Solutions**:
```bash
# Check if server is running
curl http://localhost:1234/v1/models

# Should return list of loaded models
```

### Slow Responses

**Problem**: Responses take too long
**Solutions**:
- Use a smaller model (7B instead of 13B)
- Use more aggressive quantization (Q4 instead of Q8)
- Reduce `max_tokens`
- Enable GPU acceleration in LM Studio settings

### Out of Memory

**Problem**: Model won't load or crashes
**Solutions**:
- Use a smaller model
- Use more aggressive quantization
- Close other applications
- Check LM Studio's memory settings

## Example: Full Integration

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config


async def analyze_code(code: str) -> dict:
    """Analyze code and provide feedback"""
    return {
        "code": code,
        "analysis": "Code analysis would go here",
        "suggestions": ["Use type hints", "Add docstrings"]
    }


async def main():
    # Configure LM Studio
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="lmstudio",
            model="codellama-13b",  # Example: code-focused model
            api_base="http://localhost:1234/v1",
            temperature=0.3,  # Lower for code generation
            max_tokens=2000,
        )
    }
    
    # Create tree
    tree = OpenAspenTree(llm_configs=llm_configs, name="CodeAssistant")
    
    # Add coding agent
    code_agent = tree.grow_branch(
        "code_assistant",
        description="Helps with code analysis and generation",
        llm_provider="lmstudio",
        system_prompt="You are an expert programmer. Provide clear, concise code help."
    )
    
    # Add skill
    await tree.spawn_leaf(
        code_agent,
        "analyze_code",
        analyze_code,
        "Analyze code and provide improvement suggestions"
    )
    
    # Index and use
    await tree.index_tree()
    result = await tree.execute("Analyze this Python function for improvements")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

## Advantages of LM Studio

✅ **Free** - No API costs  
✅ **Private** - Data stays on your machine  
✅ **Offline** - Works without internet  
✅ **Fast** - With GPU acceleration  
✅ **Flexible** - Use any GGUF model  

## Comparison with Cloud LLMs

| Feature | LM Studio | OpenAI | Anthropic |
|---------|-----------|--------|-----------|
| Cost | Free | $0.01-0.06/1K tokens | $0.015-0.075/1K tokens |
| Privacy | 100% Local | Cloud | Cloud |
| Speed | Fast (with GPU) | Very Fast | Fast |
| Quality | Good (depends on model) | Excellent | Excellent |
| Setup | Requires download | API key only | API key only |

## Best Practices

1. **Start Small**: Test with a 7B model first
2. **Monitor Resources**: Watch RAM/GPU usage
3. **Optimize Settings**: Tune temperature and max_tokens
4. **Cache Models**: Keep frequently used models downloaded
5. **Mix Providers**: Use LM Studio for simple tasks, cloud APIs for complex ones

## Hybrid Setup Example

Use LM Studio for cheap/simple tasks, cloud APIs for complex ones:

```python
llm_configs = {
    "lmstudio": create_llm_config(
        provider="lmstudio",
        api_base="http://localhost:1234/v1",
    ),
    "openai": create_llm_config(
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4-turbo-preview",
    )
}

# Simple agent uses free local model
simple_agent = tree.grow_branch(
    "simple_tasks",
    llm_provider="lmstudio"
)

# Complex agent uses powerful cloud model
complex_agent = tree.grow_branch(
    "complex_reasoning",
    llm_provider="openai"
)
```

## Resources

- **LM Studio**: [lmstudio.ai](https://lmstudio.ai)
- **Model Hub**: [huggingface.co](https://huggingface.co/models?library=gguf)
- **GGUF Models**: Search for "GGUF" on Hugging Face
- **TheBloke**: [huggingface.co/TheBloke](https://huggingface.co/TheBloke) - Great quantized models

---

**Ready to use free, local AI with OpenAspen! 🚀**
