# Sage 🌿

*An intelligent culinary assistant for vegan recipe management and meal planning*

## 🚀 Quick Start

### Prerequisites
- **LM Studio**: Running with model loaded on `localhost:1234`
- **Python 3.12+**: With OpenAI client library

### Setup
```bash
git clone <your-repository-url>
cd sage
pip install -r requirements.txt

# Start the agent
python sage_agent.py
```

### Test the System
```bash
# Test all functionality
python test_clean_agent.py

# Test MCP communication (debugging)
python test_mcp.py
```

## 🛠️ LM Studio Configuration

1. **Download and install** [LM Studio](https://lmstudio.ai/)
2. **Load a model**: Llama 3.2 3B Instruct or similar
3. **Start local server**: Settings → Server → Start Server
4. **Verify endpoint**: http://localhost:1234/v1 should be accessible

## 📁 Project Structure

```
sage/
├── sage_agent.py              # Main agent (working implementation)
├── test_clean_agent.py        # Test all 5 capability levels
├── test-recipes/              # Sample recipe data
│   └── sample-recipe.md       # Cashew Alfredo test recipe
├── CLAUDE.md                  # Development context for AI assistance
└── archive/                   # Old documentation files
```

## 🎯 What It Does

**Current Capabilities** (All Working):
1. **File Discovery**: Lists available recipe files
2. **Content Reading**: Reads specific recipe files 
3. **Recipe Search**: Finds recipes matching criteria
4. **Smart Analysis**: Multi-criteria recommendations
5. **Expert Analysis**: Ingredient matching with actual file contents

**Example Usage**:
```
User: What recipes are available?
Sage: I have the Cashew Alfredo recipe available in sample-recipe.md

User: What can I make with cashews and nutritional yeast?
Sage: You can make the Cashew Alfredo! It uses 1 cup raw cashews and 1/2 cup nutritional yeast...
```

## 🔧 Technical Architecture

- **Agent**: Direct OpenAI client for LM Studio integration
- **File Operations**: Python file I/O (no external dependencies)
- **Accuracy Controls**: Strict prompts prevent hallucination
- **Local Processing**: All via LM Studio, no cloud services

## 🐛 Troubleshooting

### "No response received"
- Check LM Studio is running on localhost:1234
- Verify model is loaded in LM Studio
- Try increasing timeout settings

### Tool execution errors
- File paths must be absolute
- Check test-recipes/ directory exists
- Verify file permissions

## 📊 Development Status

**Current Phase**: Step 1.3 COMPLETED ✅
- Working file search agent
- Hallucination prevention solved
- All 5 capability levels functional

**Next Phase**: Add more test recipes and extend functionality

---

*For development context and guidelines, see [CLAUDE.md](CLAUDE.md)*