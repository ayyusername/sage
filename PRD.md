# Sage - Product Requirements Document

## Problem Statement
Recipe collections in Obsidian lack semantic structure needed for intelligent meal planning. Current manual tagging is inconsistent and doesn't capture professional culinary nuances needed for advanced planning, prep optimization, and garden integration.

## Target User
Vegan culinary professional with:
- Extensive ingredient/equipment knowledge
- Active garden with seasonal harvest planning
- Need for sophisticated meal planning with prep optimization
- Preference for local AI processing
- Uses Obsidian with Kanban plugin for planning
- Wants to share system with other recipe enthusiasts

## User Requirements

### UR-1: Recipe Intelligence
**As a culinary professional**, I want my recipe collection automatically tagged with professional terminology so I can quickly find recipes that match specific techniques, dietary needs, and complexity levels.

### UR-2: Garden Integration
**As a gardener-cook**, I want meal planning that considers what's harvestable from my garden so I can maximize fresh ingredients and reduce waste.

### UR-3: Interactive Planning
**As an Obsidian user**, I want meal plans generated as Kanban boards so I can interact with and modify plans in my familiar workflow.

### UR-4: Bidirectional Learning
**As a busy cook**, I want the system to learn from my planning choices and garden availability to make increasingly relevant suggestions.

### UR-5: Model Flexibility
**As a privacy-conscious user**, I want to use any LLM provider (local, OpenAI, Anthropic) without changing my workflow.

### UR-6: Shareability
**As a community member**, I want to share this system with other recipe enthusiasts regardless of their tool preferences.

### UR-7: Performance
**As an active planner**, I want near-instant responses when exploring meal options and making changes.

---

## Phase Breakdown

## Phase 1: Foundation (2-3 days)
**Goal**: Create intelligent recipe corpus with fast search capabilities

### Step 1.1: Recipe Parser (Fulfills UR-1)
- **Build**: Obsidian markdown file scanner
- **Extract**: Recipe content while preserving existing frontmatter
- **Handle**: Various markdown structures and existing tags
- **User Value**: System understands my existing recipe collection

### Step 1.2: Professional Taxonomy Engine (Fulfills UR-1)
- **Create**: LLM-powered tagging with professional culinary categories
- **Categories**: Dietary, technique, time/effort, equipment, cuisine, components
- **Model-Agnostic**: Adapter pattern for different LLM providers (Fulfills UR-5)
- **User Value**: Recipes tagged with consistent professional terminology

### Step 1.3: Fast Index System (Fulfills UR-7)
- **Build**: Multi-layer indexing (summary, semantic, relationships, seasonal)
- **Generate**: Pre-computed embeddings for similarity search
- **Maintain**: Incremental updates when recipes change
- **User Value**: Sub-second search and planning responses

### Step 1.4: Basic Query Interface (Fulfills UR-1, UR-7)
- **CLI**: Tag-based filtering and search
- **Export**: Filtered recipe lists for planning
- **Test**: Query performance and accuracy
- **User Value**: Can instantly find "quick vegan comfort food" or similar

---

## Phase 2: Garden Integration (1 week)
**Goal**: Connect meal planning with garden harvest data

### Step 2.1: Garden Data Interface (Fulfills UR-2)
- **Design**: Standard format for garden harvest calendars
- **Connect**: Integration with existing garden planning app
- **Parse**: Seasonal availability and harvest timing
- **User Value**: System knows what's ready to harvest

### Step 2.2: Seasonal Recipe Matching (Fulfills UR-2)
- **Algorithm**: Match recipes to available garden produce
- **Prioritize**: Fresh ingredients over stored/purchased
- **Suggest**: Preservation methods for surplus harvest
- **User Value**: Maximizes garden produce usage, reduces waste

### Step 2.3: Harvest-Aware Planning (Fulfills UR-2, UR-7)
- **Update**: Recipe recommendations based on garden calendar
- **Alert**: "Use tomatoes this week before over-ripening"
- **Optimize**: Meal timing around harvest schedules
- **User Value**: Seamless garden-to-table meal planning

---

## Phase 3: Kanban Integration (1 week)
**Goal**: Bidirectional meal planning through Obsidian Kanban boards

### Step 3.1: Kanban Output Generator (Fulfills UR-3)
- **Format**: Generate meal plans in Kanban markdown syntax
- **Structure**: Organized by time periods (This Week, Prep Queue, Shopping)
- **Template**: Customizable board layouts for different planning styles
- **Reference**: Consider McKay's App Template structure for future web UI (https://github.com/mckaywrigley/mckays-app-template)
- **User Value**: Meal plans appear natively in Obsidian workflow

### Step 3.2: Kanban Reader (Fulfills UR-4)
- **Parse**: User modifications to Kanban boards
- **Track**: What gets completed vs. skipped vs. moved
- **Learn**: User preferences and scheduling patterns
- **User Value**: System adapts to my actual cooking habits

### Step 3.3: Interactive Planning Loop (Fulfills UR-3, UR-4, UR-7)
- **Monitor**: Real-time Kanban board changes
- **Suggest**: Alternative recipes when items are moved/skipped
- **Update**: Plans based on garden changes and user patterns
- **User Value**: Collaborative planning with AI sous chef

---

## Phase 4: Advanced Intelligence (2-3 weeks)
**Goal**: Sophisticated meal planning with prep optimization

### Step 4.1: Prep Optimization (Fulfills UR-1, UR-4)
- **Analyze**: Shared ingredients and prep steps across recipes
- **Schedule**: Batch cooking and advance prep timing
- **Optimize**: Equipment usage and kitchen workflow
- **User Value**: Professional-level meal prep efficiency

### Step 4.2: Equipment Scheduling (Fulfills UR-1)
- **Track**: Equipment requirements and conflicts
- **Schedule**: Optimal cooking sequences
- **Suggest**: Recipe timing to avoid equipment bottlenecks
- **User Value**: Smooth kitchen operations, no equipment conflicts

### Step 4.3: Continuous Learning (Fulfills UR-4)
- **Pattern Recognition**: Seasonal preferences, cooking frequency
- **Adaptation**: Suggestions improve based on usage patterns
- **Feedback Loop**: System becomes more personalized over time
- **User Value**: Increasingly relevant and useful meal planning

---

## Phase 5: Community & Sharing (1-2 weeks)
**Goal**: Enable system sharing with broader community

### Step 5.1: Tool Agnostic Export (Fulfills UR-6)
- **Format**: Standard recipe export formats
- **Support**: Integration with other note-taking tools
- **Documentation**: Setup guides for different environments
- **User Value**: Can share system with friends using different tools

### Step 5.2: Community Features (Fulfills UR-6)
- **Recipe Sharing**: Import/export tagged recipe collections
- **Taxonomy Sharing**: Community-driven tag improvements
- **Template Sharing**: Kanban board layouts and planning styles
- **User Value**: Benefits from community knowledge and contributions

---

## Technical Requirements
- **Local-First**: All processing via local LLMs when possible
- **Model-Agnostic**: Support for multiple LLM providers
- **MCP Architecture**: Simple agent loop + composable MCP servers
- **Incremental**: Only process new/changed files
- **Backup-Safe**: Preserve existing data and enable rollback
- **Extensible**: Data structures support future enhancements
- **Fast**: Sub-second responses for interactive planning

## MCP Server Architecture
- **File System MCP Server**: Official ModelContextProtocol server for file I/O operations
  - Repository: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
  - Tools: read_file, write_file, list_directory, create_directory
- **Custom Sage MCP Server**: Culinary-specific intelligence and processing
  - Tools: analyze_recipe_content, extract_culinary_tags, format_frontmatter
- **Agent Loop**: Simple orchestrator routing between user, model, and MCP servers
  - Pattern: User message → Model analysis → Tool calls → Results → Model response

## Success Metrics
- **Phase 1**: All recipes tagged, <1s search responses
- **Phase 2**: Garden integration working, seasonal suggestions relevant
- **Phase 3**: Kanban generation/reading functional, user adaptation evident
- **Phase 4**: Prep optimization saves measurable time
- **Phase 5**: System successfully shared with at least 3 other users