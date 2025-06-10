# How to Use Sage (v1.1.0)

## Current Capabilities ✅

Sage v1.1.0 provides:
- **File System Operations** via MCP protocol
- **LM Studio Integration** for local AI processing
- **Recipe File Access** through tiny-agents framework

## Prerequisites

1. **LM Studio Running**
   - Load Qwen 3 8B model (or any compatible model)
   - Ensure server running on `localhost:1234`
   - Verify "Status: Running" in LM Studio interface

2. **Python Environment**
   ```bash
   pip install -r requirements.txt
   # Installs: huggingface_hub[mcp], openai, requests
   ```

3. **Node.js** (for MCP filesystem server)

## Quick Start

### 1. Test Components
```bash
# Test LM Studio connectivity
python test_lm_studio_simple.py

# Test MCP filesystem operations
python test_mcp.py

# Test complete integration
python simple_demo.py
```

### 2. Interactive Agent (Current State)
```bash
python sage_agent_tiny.py
```

**What happens:**
- Sage agent initializes with tiny-agents framework
- Connects to LM Studio and MCP filesystem server
- Ready to chat about recipes using available tools

## What You Can Do Right Now

### Basic File Operations
```
User: "What recipe files are available?"
Sage: [Uses list_directory tool to show files in test-recipes/]

User: "Read the sample recipe file"
Sage: [Uses read_file tool to display sample-recipe.md content]

User: "What ingredients does the cashew alfredo recipe use?"
Sage: [Reads file and analyzes ingredients using LM Studio]
```

### Recipe Analysis (via LM Studio)
```
User: "What dietary restrictions does this recipe meet?"
Sage: [Analyzes recipe content and identifies vegan, dairy-free, etc.]

User: "What cooking techniques are used in this recipe?"
Sage: [Identifies blending, soaking, etc. from instructions]

User: "How long does this recipe take to make?"
Sage: [Extracts and analyzes prep/cook times]
```

## Current Limitations

### What Works:
- ✅ Reading existing recipe files
- ✅ Basic recipe analysis via LM Studio
- ✅ File listing and navigation
- ✅ General culinary questions and advice

### What's Missing (Step 1.2):
- ❌ **Professional Tagging** - No systematic culinary taxonomy
- ❌ **Enhanced Frontmatter** - Can't add structured metadata to files
- ❌ **Recipe Parsing** - No structured ingredient/instruction extraction
- ❌ **Batch Processing** - Can't process multiple recipes at once

## Example Session

```bash
$ python sage_agent_tiny.py

🌿 Sage Agent (Tiny-Agents Powered)
Type 'quit' to exit
--------------------------------------------------
🌿 Sage Agent initialized with tiny-agents framework

User: What recipes do I have?
Sage: I'll check your recipe collection for you.
[Uses list_directory tool]
I found 1 recipe file: sample-recipe.md

User: Tell me about the cashew alfredo recipe
Sage: Let me read that recipe for you.
[Uses read_file tool, then analyzes with LM Studio]
This is a vegan cashew alfredo recipe that serves as a dairy-free pasta sauce. 
Key features:
- Vegan and dairy-free
- 15-minute prep time
- Uses cashews as cream base
- Simple blending technique
- Nutritional yeast for umami flavor

User: What cooking equipment do I need?
Sage: Based on the recipe, you'll need:
- Blender (for cashews and liquid ingredients)
- Measuring cups
- Basic prep tools for garlic and lemon
The recipe is designed to be simple with minimal equipment requirements.

User: quit
🌿 Sage Agent stopped
```

## Troubleshooting

### LM Studio Not Responding
```bash
# Check LM Studio is running
curl http://localhost:1234/v1/models

# Test direct connection
python test_lm_studio_simple.py
```

### MCP Server Issues
```bash
# Test MCP communication
python test_mcp.py

# Check filesystem server manually
node mcp-servers/src/filesystem/dist/index.js test-recipes
```

### Agent Hanging
- Current async streaming has timing issues
- Use Ctrl+C to exit
- Individual tests work more reliably than full agent

## Next Steps

**Step 1.2 will add:**
- Professional culinary tagging system
- Structured recipe data extraction
- Enhanced frontmatter generation
- Batch recipe processing
- Improved error handling

**For now**: Use Sage for recipe reading, basic analysis, and culinary consultation with your existing recipe files! 🌿