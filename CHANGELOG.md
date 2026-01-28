# Changelog

All notable changes to OpenAspen will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-27

### Added
- Initial release of OpenAspen framework
- Core tree-structured architecture (TreeNode, Branch, Leaf)
- Multi-LLM router supporting OpenAI, Anthropic, Grok, Ollama, and LM Studio
- Group RAG system with ChromaDB integration
- Intelligent query routing and execution
- CLI interface with init, run, visualize, and info commands
- FastAPI server with OpenAI-compatible endpoints
- Comprehensive test suite with pytest
- Full documentation (README, Architecture, Quick Start guides)
- Example implementations (basic, advanced, server)
- Poetry-based dependency management
- GitHub Actions CI/CD workflow
- Pre-commit hooks for code quality
- MIT License

### Features
- Async-first execution for high performance
- Smart LLM routing by cost, speed, or skill type
- Cross-agent context sharing via shared vector database
- Automatic async/sync function detection
- Parameter extraction and validation
- Execution history tracking
- Tree visualization (ASCII art)
- JSON-based tree configuration
- Environment variable support
- Type-safe with Pydantic models

### Developer Experience
- Comprehensive type hints
- Detailed docstrings
- Example code for common patterns
- Extensive test coverage
- Development setup with pre-commit hooks
- Contributing guidelines

## [Unreleased]

### Planned
- FAISS vector store support
- LangGraph integration for complex workflows
- Streaming response support
- Agent memory and conversation history
- Web UI for tree management
- Additional LLM providers (Cohere, AI21)
- Tool calling / function calling support
- Distributed execution capabilities
- Performance benchmarks
- Docker support
- Kubernetes deployment examples
