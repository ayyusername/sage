# Sage 🌿

*An intelligent culinary knowledge system for professional recipe management and meal planning*

## Vision

Transform your Obsidian recipe vault into a semantically-rich knowledge base that evolves with advancing AI capabilities. Built for culinary professionals who need sophisticated meal planning, prep optimization, and equipment scheduling.

## Architecture Philosophy

**MCP-Powered Agent System**: Simple orchestrator with composable tools
- **Agent Loop**: Basic while loop routing between user, model, and MCP servers
- **File System MCP**: Official ModelContextProtocol server for all file operations
- **Sage MCP Server**: Custom culinary intelligence tools (tagging, analysis, formatting)
- **Model Agnostic**: Works with LM Studio, OpenAI, Anthropic, or any compatible LLM

**Iterative Enrichment**: Each processing pass adds deeper intelligence layers
- Pass 1: Basic taxonomic tagging via MCP tools
- Pass 2: Component decomposition through enhanced prompting
- Pass 3: Garden integration and Kanban planning
- Pass 4: Advanced optimization and learning

**Local-First**: All processing happens locally via LM Studio
**Future-Proof**: MCP architecture scales from simple tools → complex workflows

## MVP Scope

1. **MCP Server Setup**: Official File System MCP + Custom Sage MCP Server
2. **Agent Loop**: Simple orchestrator routing messages and tool calls
3. **Recipe Processing Tools**: analyze_recipe_content, extract_culinary_tags, format_frontmatter
4. **Indexing System**: Fast search via recipe_index_manager and search_recipes tools
5. **CLI Interface**: Command-line interface for batch processing and querying

## Long-term Goals

- **Garden Integration**: Harvest-aware meal planning via garden MCP tools
- **Kanban Planning**: Bidirectional meal planning through Obsidian Kanban boards
- **Prep Optimization**: Equipment scheduling and shared prep batching
- **Learning System**: Continuous adaptation to user preferences and patterns
- **Community Sharing**: Export/import recipes and templates across different tools

---

*"Because your kitchen deserves AI as sophisticated as your palate"*