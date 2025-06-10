# Sage 🌿

*An intelligent culinary knowledge system for professional recipe management and meal planning*

## 🎯 Current Status: Step 1.3 - Hallucination Prevention

**Live Repository**: https://github.com/ayyusername/sage  
**Version**: v1.3.0 - File Search Agent with Accuracy Improvements

## 🏗️ Architecture

**Tiny-Agents MCP Framework**: Hugging Face's MCP-powered agent system
- **Agent**: `sage_agent_tiny.py` - Tiny-agents orchestrator (~70 lines)
- **File System MCP**: Official ModelContextProtocol server for file operations
- **LM Studio**: Local inference via Qwen 3 8B model
- **Model Agnostic**: Works with LM Studio, OpenAI, Anthropic, or any compatible LLM

```
User → Tiny-Agents → LM Studio → File System MCP → Recipe Files
```

## ✅ What's Working

- **Tiny-Agents Integration**: Hugging Face MCP framework operational
- **File System MCP Server**: Reading/writing recipe files via MCP protocol
- **LM Studio Client**: OpenAI-compatible API integration with local model
- **Recipe Processing**: Ready for culinary intelligence tools
- **Test Suite**: Comprehensive verification of all components

## 🚀 Quick Start

### Prerequisites
- **LM Studio**: Running with loaded model on `localhost:1234`
- **Node.js**: For MCP filesystem server
- **Python 3.12+**: With `huggingface_hub[mcp]`

### Setup
```bash
git clone https://github.com/ayyusername/sage.git
cd sage
pip install -r requirements.txt

# Start the agent
python sage_agent_tiny.py
```

### Test Components
```bash
# Test MCP communication independently
python test_mcp.py

# Test complete system integration
python test_full_integration.py

# Interactive demo
python live_demo.py
```

## 📁 Project Structure

```
sage/
├── sage_agent_tiny.py          # Main tiny-agents implementation
├── sage_agent_config.json      # MCP server configuration
├── test-recipes/               # Sample recipe collection
├── test_*.py                   # Comprehensive test suite
├── PRD.md                      # Product requirements
├── GIT_WORKFLOW.md            # Development workflow
└── Documentation files
```

## 🛣️ Roadmap

### ✅ Phase 1: Foundation (Step 1.1 Complete)
- Tiny-agents MCP framework
- File System MCP server
- LM Studio integration
- Testing infrastructure

### 🔄 Next: Step 1.2 - Recipe Processing Tools
- Custom Sage MCP Server
- `analyze_recipe_content` tool
- `extract_culinary_tags` tool
- `format_frontmatter` tool

### 🔮 Future Phases
- **Phase 2**: Garden integration for harvest-aware planning
- **Phase 3**: Kanban boards for interactive meal planning  
- **Phase 4**: Prep optimization and equipment scheduling
- **Phase 5**: Community sharing and templates

## 🔧 Technical Stack

- **Agent Framework**: Hugging Face tiny-agents
- **MCP Protocol**: Model Context Protocol for tool integration
- **Local LLM**: LM Studio with Qwen 3 8B model
- **File Operations**: Official MCP filesystem server
- **Language**: Python 3.12+ with async/await
- **Testing**: Comprehensive integration test suite

## 📖 Documentation

- **[Product Requirements](PRD.md)**: Detailed specifications and user requirements
- **[Development Guidelines](DEVELOPMENT_GUIDELINES.md)**: How to maintain clean codebase
- **[Git Workflow](GIT_WORKFLOW.md)**: Development and branching strategy
- **[Agent Flowchart](agent_flowchart.md)**: Processing pipeline details
- **[Status](STATUS.md)**: Current development progress
- **[Claude Instructions](CLAUDE.md)**: Development context and guidelines

## 🧹 Maintaining Clean Codebase

To avoid file proliferation:
1. Work in feature branches for experiments
2. Run `python cleanup_codebase.py` before merging
3. Keep only one production agent file
4. See [Development Guidelines](DEVELOPMENT_GUIDELINES.md) for details

---

*"Because your kitchen deserves AI as sophisticated as your palate"* 🌿