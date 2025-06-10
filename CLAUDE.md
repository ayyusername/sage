# Sage Development Notes

## Project Context
**Sage** is a culinary AI assistant for vegan recipe management and meal planning.

**User Profile**: Vegan culinary professional with extensive ingredient/equipment knowledge, active garden, preference for local AI processing.

**Current Status**: Step 1.3 COMPLETED - Working file search agent with hallucination prevention solved.

## Technical Architecture

### Core Stack
- **Agent**: sage_agent.py (direct OpenAI client implementation)
- **LLM**: LM Studio local models (5-10 min response times acceptable)
- **File Operations**: Direct Python file I/O (no MCP framework)
- **Test Recipe Data**: test-recipes/sample-recipe.md (Cashew Alfredo)

### CRITICAL Architecture Decisions
1. **Use Direct File Operations** - Not MCP framework (sage_agent.py vs sage_agent_tiny.py)
2. **OpenAI Client Required** - For clean LM Studio integration  
3. **Strict Accuracy Controls** - System prompts prevent hallucination
4. **Local Processing Only** - No cloud services, all via LM Studio
5. **Simple Agent Loop** - Orchestrates tool calls, intelligence in tools + model

### Technical Constraints
- **Response Times**: 5-10 minutes acceptable for complex operations
- **Timeout Handling**: Use 10+ minute timeouts for all LM Studio calls
- **Async Warnings**: Ignore async context manager warnings during shutdown
- **Model Recommendations**: Llama 3.2 3B+ for proper tool calling

## Commands to Remember

### Development
```bash
# Test the working agent
python sage_agent.py

# Test specific functionality  
python test_clean_agent.py

# Test raw MCP communication (debugging only)
python test_mcp.py
```

### LM Studio Setup
- Base URL: http://localhost:1234/v1
- API Key: "lm-studio" 
- Recommended Model: Llama 3.2 3B Instruct or higher
- Ensure LM Studio is running before testing

## Code Style & Patterns

### File Organization
- **ONE agent file**: sage_agent.py (production)
- **Focused tests**: test_clean_agent.py, test_mcp.py
- **Clean commits**: Remove experimental files before merging
- **Use .gitignore**: For mcp-servers/, __pycache__, etc.

### Agent Implementation Pattern
```python
class SageAgent:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        
    async def chat(self, message: str) -> str:
        # 1. Gather file information automatically
        # 2. Add context to system prompt  
        # 3. Call LLM with strict accuracy controls
        # 4. Return only factual responses based on file data
```

### Error Handling
- **Tool failures**: Graceful degradation to simpler methods
- **LM Studio timeouts**: Use 10+ minute timeouts
- **File operations**: Always preserve original content
- **Hallucination prevention**: Strict system prompts + real data only

## Current Capability Levels (All Working)

1. **File Discovery**: Lists available recipe files
2. **Content Reading**: Reads specific recipe files 
3. **Recipe Search**: Finds recipes matching criteria
4. **Smart Analysis**: Multi-criteria recommendations
5. **Expert Analysis**: Ingredient matching with actual file contents

## Development Workflow

### Git Workflow
```bash
# Feature development
git checkout -b feature/description
# ... develop ...
git checkout main
git merge feature/description
git tag v1.X.Y
```

### Commit Format
```
<type>: <description>

<body with details>

🌿 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Before Merging
- [ ] Remove experimental files
- [ ] Test with python sage_agent.py
- [ ] Verify all 5 capability levels working
- [ ] Clean commit history

## Problem-Solution Mapping

### Agent Issues → Prompting Fixes
- **Hallucination**: Strict system prompts + real data only
- **Tool calling**: Pattern matching + automatic tool execution
- **Accuracy**: "ONLY use information from Tool Results" in prompts

### When NOT to Change Architecture
- Don't abandon OpenAI client for raw HTTP
- Don't create multiple agent versions  
- Don't build custom MCP when direct file ops work
- Don't add complexity when prompts can be improved

## Testing Strategy

### Essential Tests
1. **test_clean_agent.py**: All 5 capability levels
2. **test_mcp.py**: Raw MCP communication (debugging)
3. **Manual testing**: python sage_agent.py with real queries

### Test Data
- **test-recipes/sample-recipe.md**: Cashew Alfredo recipe
- Use this real data for accuracy testing
- Don't create mock data - use actual file contents

## Next Development Phase

### Immediate Priorities
- Add more test recipes for broader functionality
- Implement ingredient-based recipe search
- Add recipe metadata extraction

### Architecture Extensions
- Additional file operations (write, create)
- Recipe analysis tools
- Search and indexing capabilities

### Future Phases
- Garden integration (seasonal planning)
- Kanban board generation (Obsidian integration)
- Prep optimization and workflow management

## Debugging Common Issues

### "No response received"
- Check LM Studio is running on localhost:1234
- Verify model is loaded in LM Studio
- Increase timeout settings

### Tool execution errors
- File paths must be absolute
- Check test-recipes/ directory exists
- Verify file permissions

### Hallucination problems
- Strengthen system prompts
- Add "ONLY use Tool Results" instructions
- Provide real file data in context

---

**Remember**: Keep it simple. Direct file operations work. Focus on prompting over architecture changes. Test with real data.