# Sage - Product Requirements Document

## Problem Statement
Recipe collections in Obsidian lack semantic structure needed for intelligent meal planning. Current manual tagging is inconsistent and doesn't capture professional culinary nuances needed for advanced planning, prep optimization, and garden integration.

## Target User
Vegan culinary professional with:
- Extensive ingredient/equipment knowledge
- Active garden with seasonal harvest planning
- Need for sophisticated meal planning with prep optimization
- Preference for local AI processing via LM Studio
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
**As an active planner**, I want responses within reasonable time (accepting 5-10 minute wait times for complex analysis given local processing constraints).

---

## Technical Architecture

### Core Framework Requirements
- **Tiny-Agents Framework**: REQUIRED - HuggingFace tiny-agents for LLM + MCP orchestration
- **OpenAI Client**: REQUIRED for LM Studio integration (no custom HTTP implementations)
- **File System MCP**: Official ModelContextProtocol server for file operations
- **LM Studio**: Local LLM processing (Qwen 3 8B Deepseek R1 Distilled)
- **Response Times**: 5-10 minutes acceptable for complex operations due to local processing

### Known Technical Constraints
- **LM Studio Performance**: 5-10 minute response times for complex queries (acceptable)
- **Timeout Handling**: All operations must use 10+ minute timeouts
- **Async Cleanup**: Ignore async context manager warnings during shutdown
- **MCP Communication**: Stdio-based MCP servers working with proper timeout handling

### Anti-Patterns (What NOT to Do)
- ❌ Raw HTTP calls replacing OpenAI client for production features
- ❌ Custom MCP implementations bypassing tiny-agents framework
- ❌ Abandoning standard tools due to configuration issues
- ❌ Short timeouts that interrupt legitimate slow LM Studio responses

---

## Development Pipeline

## ✅ COMPLETED: Phase 1.1 - Foundation Setup (v1.1.0)
**Status**: Production ready
**Deliverables**: Working tiny-agents + File System MCP + LM Studio pipeline

### Architecture Achieved
```
User → Tiny-Agents → LM Studio → File System MCP → Recipe Files
```

### Components Working
- ✅ Tiny-agents framework operational with proper timeouts
- ✅ File System MCP server with JSON-RPC communication
- ✅ LM Studio integration via OpenAI client
- ✅ Basic file search and listing functionality
- ✅ End-to-end testing with 10+ minute timeout handling

---

## 🔄 CURRENT: Phase 1.2 - File Search MVP
**Goal**: Working file search agent using existing File System MCP
**Timeline**: 1-2 days

### Step 1.2.1: File Search Agent (Fulfills UR-1, UR-7)
- **Build**: Working agent with File System MCP and proper timeouts
- **Implement**: Natural language recipe file search
- **Test**: Search through test-recipes directory
- **Deliver**: MVP that can find recipes by description
- **User Value**: "Find vegan pasta recipes" → lists matching files

### Step 1.2.2: Enhanced Search Interface (Fulfills UR-1)
- **Create**: Command-line interface for recipe search
- **Features**: File content search, ingredient matching
- **Polish**: Error handling and user feedback
- **User Value**: Reliable recipe discovery tool

### Success Criteria - Phase 1.2
- [ ] **Agent Search**: Natural language search through recipe files
- [ ] **Content Analysis**: Basic recipe content understanding
- [ ] **File Operations**: Read/list recipe files reliably
- [ ] **Timeout Handling**: Proper 10+ minute timeouts for all operations
- [ ] **User Interface**: Simple CLI for recipe search

---

## 🔮 PLANNED: Phase 1.3 - Custom Recipe MCP
**Goal**: Custom Sage MCP Server with culinary intelligence
**Timeline**: 3-5 days

### Step 1.3.1: Sage MCP Server Foundation
- **Build**: Python MCP server using official SDK
- **Integrate**: With tiny-agents framework
- **Test**: Server startup and communication

### Step 1.3.2: Recipe Analysis Tools
- **analyze_recipe_content**: Parse markdown recipes into structured data
- **extract_culinary_tags**: Professional taxonomy tagging via LLM
- **format_frontmatter**: Enhanced YAML frontmatter generation

### Step 1.3.3: Enhanced Recipe Processing
- **Categories**: Dietary, technique, time/effort, equipment, cuisine
- **LLM Integration**: OpenAI client for tag extraction
- **Output**: Enriched recipe files with professional metadata

### Target Architecture - Phase 1.3
```
User → Tiny-Agents → LM Studio → [File System MCP + Sage MCP] → Enhanced Recipes
```

---

## 🔮 PLANNED: Phase 1.4 - Search & Index System
**Goal**: Fast recipe search with semantic understanding
**Timeline**: 2-3 days

### Step 1.4.1: Recipe Index Manager
- **Build**: Index of processed recipes with metadata
- **Search**: Tag-based and semantic search capabilities
- **Performance**: Optimized for local processing constraints

### Step 1.4.2: Query Interface
- **CLI**: Advanced search with filtering
- **Export**: Recipe lists for meal planning
- **Testing**: Performance and accuracy validation

---

## 📋 Future Phases (Post-MVP)

### Phase 2: Garden Integration (1 week)
- Garden harvest data integration
- Seasonal recipe matching
- Harvest-aware meal planning

### Phase 3: Kanban Integration (1 week)
- Obsidian Kanban board generation
- Interactive meal planning
- User preference learning

### Phase 4: Advanced Intelligence (2-3 weeks)
- Prep optimization and scheduling
- Equipment workflow management
- Continuous learning system

### Phase 5: Community & Sharing (1-2 weeks)
- Recipe collection sharing
- Cross-platform compatibility
- Community taxonomy improvements

---

## Success Metrics

### Phase 1.2 (Current)
- ✅ Natural language file search working
- ✅ 10+ minute timeout handling
- ✅ Basic recipe discovery functionality

### Phase 1.3 (Next)
- ✅ Custom Sage MCP server operational
- ✅ Professional recipe tagging system
- ✅ Enhanced recipe metadata generation

### Phase 1.4 (Final Foundation)
- ✅ Fast recipe search and filtering
- ✅ Complete Phase 1 functionality
- ✅ Ready for advanced features

### Long-term Success
- **Phase 2**: Garden integration working, seasonal suggestions relevant
- **Phase 3**: Kanban generation functional, user adaptation evident
- **Phase 4**: Prep optimization saves measurable time
- **Phase 5**: System shared with 3+ users successfully

---

## Development Notes

### Current Status (Phase 1.1 ✅)
- Repository: https://github.com/ayyusername/sage (v1.1.0)
- Branch: `main` 
- Next: `feature/phase-1.2-file-search-mvp`

### Key Learnings
- LM Studio requires 5-10 minute timeouts for complex operations
- Tiny-agents framework works when given adequate time
- File System MCP provides solid foundation for file operations
- Async cleanup warnings are cosmetic and can be ignored

### Focus: Build working file search MVP with existing components! 🌿