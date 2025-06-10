# Sage Development Notes

## IMPORTANT: Constraint Validation

**MANDATORY CHECK**: Before implementing ANY solution, verify it aligns with project constraints:

1. **MVP Focus**: Building a simple assistant that uses tools for recipe/file search examples
2. **Tool-Based Architecture**: Agent orchestrates tool calls, not custom logic
3. **MCP Integration**: Use official ModelContextProtocol servers where possible
4. **Local Processing**: LM Studio + local models, not cloud services
5. **Iterative Development**: Start simple, add complexity only when needed

**PROCESS**: For each proposed change, ask:
- Does this maintain the simple assistant + tools architecture?
- Is this the minimum viable solution for the current step?
- Does this integrate properly with MCP tools?
- Will this work reliably with local LM Studio setup?

**REJECT** solutions that violate these constraints, regardless of technical merit.

## Project Context
- User is a vegan culinary professional with extensive ingredients/equipment knowledge
- Building iterative LLM-powered recipe enrichment system
- Local processing via LM Studio (Llama 3.2 3B Instruct recommended, ~slower but better tool calling)
- Target: Obsidian vault → intelligent meal planning & prep optimization
- **Status**: Step 1.2.1 complete - file search agent working with Tests 1-3 passing

## MCP Architecture
- **File System MCP**: Official ModelContextProtocol server for file operations
  - Repository: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
  - Tools: read_file, write_file, list_directory, create_directory
- **Sage MCP Server**: Custom culinary intelligence server
  - Tools: analyze_recipe_content, extract_culinary_tags, format_frontmatter
- **Agent Loop**: Simple while loop routing user ↔ model ↔ MCP tools

## Commands to Remember
- LM Studio API: `http://localhost:1234/v1/chat/completions`
- MCP Server setup: Clone official servers repo, install filesystem server
- Processing approach: Agent orchestrates tool calls across MCP servers
- Data evolution: MCP tools → enhanced prompting → advanced workflows
- **Model Recommendation**: Use Llama 3.2 3B+ for proper MCP tool calling (qwen2.5-0.5b has compatibility issues)
- **Test Suite**: `python test_runner.py` for full validation, individual tests available

## Architecture Decisions
- Use proven MCP infrastructure instead of building from scratch
- Agent as simple orchestrator, intelligence in model + tools
- Composable tool architecture for easy extension
- Start with file operations + basic culinary tools

## Tool Selection Principles

### Prefer Standard Libraries
- ALWAYS use established, well-maintained libraries over custom implementations
- Examples: OpenAI client, requests, pandas - don't reinvent these
- If a standard tool isn't working, debug and fix it rather than replace it

### When NOT to Work Around Issues
- Don't abandon proper APIs for raw HTTP when the API should work
- Don't write custom implementations of existing functionality
- Don't sacrifice type safety, error handling, or maintainability for "quick fixes"

### Debug First, Replace Last
- When standard tools fail, assume configuration/compatibility issues first
- Only replace tools after exhausting debugging options
- Ask "What am I losing by switching?" before suggesting alternatives

### Problem-Solution Mapping

- **Prompting Issues**: Fix with better prompts, examples, or instructions
- **Logic Errors**: Fix with code changes
- **Architecture Problems**: Fix with structural changes

**RULE**: When an AI agent isn't following instructions correctly, the solution is almost always PROMPTING, not code architecture. Only suggest code changes when:
1. The prompt is already clear and specific
2. The AI physically cannot do what's requested with available tools
3. There's a genuine technical limitation

**Red Flags for Overengineering**:
- Suggesting "two-stage architecture" for instruction-following problems
- Creating new classes/files when prompts could be improved
- Building validation systems when clearer instructions would work
- Adding complexity when the AI just needs better examples

**Default Response**: "This looks like a prompting issue. Let's fix the instructions first."

### No Hacks or Workarounds

**CRITICAL**: Never use hacks, workarounds, or temporary solutions that compromise the system integrity.

**Examples of FORBIDDEN approaches**:
- Hardcoding filenames instead of fixing file path logic
- Creating manual workarounds instead of fixing underlying bugs
- Building temporary solutions that "prove" functionality without actually working
- Using tricks that make demos work but aren't real solutions

**REQUIRED**: All solutions must be rigorous, complete, and production-ready:
- Fix root causes, not symptoms
- Build solutions that scale and work in all cases
- Test thoroughly with real data, not contrived examples
- Ensure robustness and reliability over quick demos

### Specific to This Project
- OpenAI client is required for clean LM Studio integration
- MCP framework provides proper tool orchestration
- Direct HTTP calls should only be used for testing/debugging, not production