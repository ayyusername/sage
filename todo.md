# Sage Development Todo List

## ✅ COMPLETED: Phase 1 Foundation - Step 1.1 (v1.1.0)
**Goal**: Create MCP server architecture with tiny-agents framework

### ✅ Step 1.1: MCP Server Setup (Fulfills UR-1, UR-5) - COMPLETE
- [x] **Tiny-Agents Framework Integration**
  - [x] Install `huggingface_hub[mcp]` with tiny-agents support
  - [x] Implement `sage_agent_tiny.py` using Hugging Face MCP framework
  - [x] Configure LM Studio integration via OpenAI-compatible API
  - [x] Test agent initialization and MCP server routing
- [x] **File System MCP Server Setup**
  - [x] Clone official ModelContextProtocol servers repository
  - [x] Build and configure filesystem server for recipe directory access
  - [x] Test basic file operations (read_file, list_directory)
  - [x] Verify MCP protocol communication with JSON-RPC
- [x] **Integration Testing & Documentation**
  - [x] Create comprehensive test suite (`test_*.py` files)
  - [x] Verify end-to-end pipeline: Agent → LM Studio → MCP → Files
  - [x] Set up git workflow and push to GitHub
  - [x] Document architecture and setup procedures

**Deliverables**: ✅ Working tiny-agents + MCP + LM Studio pipeline

---

## 🔄 CURRENT: Phase 1 Foundation - Step 1.2
**Goal**: Build custom Sage MCP Server with culinary intelligence tools

### Step 1.2: Recipe Processing Tools (Fulfills UR-1) - IN PROGRESS
- [ ] **Create Sage MCP Server Foundation**
  - [ ] Set up Python MCP server boilerplate using official SDK
  - [ ] Define server manifest with culinary-specific tools
  - [ ] Implement tool registration and handler framework
  - [ ] Test server startup and basic communication
- [ ] **Build analyze_recipe_content tool**
  - [ ] Create tool definition with parameters (file_path, content)
  - [ ] Implement markdown parsing for recipe components
  - [ ] Extract ingredients, instructions, prep time, equipment from text
  - [ ] Handle various markdown formatting styles (headers, lists, frontmatter)
  - [ ] Return structured recipe data for further processing
- [ ] **Build extract_culinary_tags tool**
  - [ ] Design professional culinary taxonomy (dietary, technique, time/effort, equipment, cuisine)
  - [ ] Create LLM prompting strategy for tag extraction
  - [ ] Implement model-agnostic LLM calling (LM Studio, OpenAI, Anthropic)
  - [ ] Validate tags against predefined taxonomy
  - [ ] Return confidence scores and tag justifications
- [ ] **Build format_frontmatter tool**
  - [ ] Parse existing YAML frontmatter safely
  - [ ] Merge new tags with existing metadata
  - [ ] Format enhanced frontmatter with proper YAML structure
  - [ ] Preserve existing frontmatter fields (title, date, etc.)
  - [ ] Return properly formatted markdown with enhanced frontmatter
- [ ] **Integration Testing**
  - [ ] Test Sage MCP server with tiny-agents framework
  - [ ] Verify recipe processing workflow end-to-end
  - [ ] Test with various recipe formats and edge cases
  - [ ] Performance testing for processing speed

**Target**: ✅ Custom Sage MCP server with 3 core culinary tools

---

## 🔮 PLANNED: Phase 1 Foundation - Remaining Steps

### Step 1.3: Fast Index System (Fulfills UR-7)
- [ ] Build recipe_index_manager tool
- [ ] Build search_recipes tool  
- [ ] Test index performance with <1s search target

### Step 1.4: CLI Interface (Fulfills UR-1, UR-7)
- [ ] Create command-line interface for agent
- [ ] Implement batch processing for recipe directories
- [ ] Test complete Phase 1 functionality

---

## 📋 Future Phases (Design Complete, Implementation Pending)

### Phase 2: Garden Integration (1 week)
- Garden MCP tools for harvest-aware meal planning
- Seasonal recipe matching and preservation suggestions

### Phase 3: Kanban Integration (1 week)  
- Obsidian Kanban board generation and reading
- Interactive meal planning with user adaptation

### Phase 4: Advanced Intelligence (2-3 weeks)
- Prep optimization and equipment scheduling
- Continuous learning and pattern recognition

### Phase 5: Community & Sharing (1-2 weeks)
- Recipe collection export/import
- Community-driven improvements

---

## 📊 Success Metrics Progress

### ✅ Phase 1 - Step 1.1 Success Criteria (ACHIEVED)
- ✅ **MCP Architecture**: Tiny-agents framework operational
- ✅ **File Operations**: Reading/writing recipes via MCP protocol
- ✅ **LM Studio Integration**: Local Qwen 3 8B model responding  
- ✅ **Testing Coverage**: All components verified with test suite
- ✅ **Repository**: Live on GitHub with proper workflow (v1.1.0)

### 🎯 Phase 1 - Step 1.2 Success Criteria (TARGET)
- [ ] **Custom MCP Server**: Sage server with culinary tools operational
- [ ] **Recipe Processing**: analyze_recipe_content parsing markdown recipes
- [ ] **Professional Tagging**: extract_culinary_tags with taxonomy
- [ ] **Enhanced Output**: format_frontmatter generating enriched files
- [ ] **Integration**: Sage MCP + tiny-agents + File System MCP working together

---

## 🔧 Development Notes

### Current Architecture (Step 1.1 ✅)
```
User → Tiny-Agents → LM Studio → File System MCP → Recipe Files
```

### Target Architecture (Step 1.2 🎯)
```
User → Tiny-Agents → LM Studio → [File System MCP + Sage MCP] → Enhanced Recipes
```

### Repository Status
- **Branch**: `main`
- **Version**: `v1.1.0` 
- **GitHub**: https://github.com/ayyusername/sage
- **Next Branch**: `feature/step-1.2-sage-mcp-server`

**Focus**: Ready to implement custom Sage MCP Server with culinary intelligence! 🌿