# Sage Development Notes

## Project Context
- User is a vegan culinary professional with extensive ingredients/equipment knowledge
- Building iterative LLM-powered recipe enrichment system
- Local processing via LM Studio (Qwen 3 8B Deepseek R1 Distilled, ~17 tok/s)
- Target: Obsidian vault → intelligent meal planning & prep optimization

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

## Architecture Decisions
- Use proven MCP infrastructure instead of building from scratch
- Agent as simple orchestrator, intelligence in model + tools
- Composable tool architecture for easy extension
- Start with file operations + basic culinary tools