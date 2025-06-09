# Sage Development Todo List

## Phase 1: Foundation (2-3 days)
**Goal**: Create intelligent recipe corpus with MCP server architecture

### Step 1.1: MCP Server Setup (Fulfills UR-1, UR-5)
- [ ] Install official File System MCP Server from ModelContextProtocol
  - [ ] Clone repository: https://github.com/modelcontextprotocol/servers
  - [ ] Set up filesystem server according to documentation
  - [ ] Test basic file operations (read_file, write_file, list_directory)
  - [ ] Configure server permissions for recipe directory access
- [ ] Create basic Sage MCP Server structure
  - [ ] Set up MCP server boilerplate with Python/Node.js
  - [ ] Define server manifest with culinary-specific tools
  - [ ] Implement basic tool registration and handler framework
  - [ ] Test MCP server communication with simple echo tool

### Step 1.2: Recipe Processing Tools (Fulfills UR-1)
- [ ] Build analyze_recipe_content tool
  - [ ] Create tool definition with parameters (content, existing_tags)
  - [ ] Implement markdown parsing logic for recipe components
  - [ ] Extract ingredients, instructions, prep time, equipment from text
  - [ ] Handle various markdown formatting styles (headers, lists, frontmatter)
  - [ ] Return structured recipe data for analysis
- [ ] Build extract_culinary_tags tool  
  - [ ] Design professional culinary taxonomy (dietary, technique, time/effort, equipment, cuisine)
  - [ ] Create prompting strategy for LLM tag extraction
  - [ ] Implement model-agnostic LLM calling (support LM Studio, OpenAI, Anthropic)
  - [ ] Validate tags against predefined taxonomy
  - [ ] Return confidence scores and tag justifications
- [ ] Build format_frontmatter tool
  - [ ] Parse existing YAML frontmatter safely
  - [ ] Merge new tags with existing metadata
  - [ ] Format enhanced frontmatter with proper YAML structure
  - [ ] Preserve existing frontmatter fields (title, date, etc.)
  - [ ] Return properly formatted markdown with enhanced frontmatter

### Step 1.3: Agent Loop Implementation (Fulfills UR-1, UR-7)
- [ ] Create simple agent orchestrator
  - [ ] Implement basic while loop for message handling
  - [ ] Route user messages to appropriate LLM
  - [ ] Parse LLM responses for tool calls
  - [ ] Execute tool calls on appropriate MCP servers
  - [ ] Return tool results to LLM for continued processing
  - [ ] Send final responses back to user
- [ ] Test basic recipe processing workflow
  - [ ] Agent reads recipe file via File System MCP
  - [ ] Agent analyzes content via Sage MCP analyze_recipe_content
  - [ ] Agent extracts tags via Sage MCP extract_culinary_tags
  - [ ] Agent formats enhanced recipe via Sage MCP format_frontmatter
  - [ ] Agent writes enhanced recipe back via File System MCP
  - [ ] Verify complete processing pipeline works end-to-end

### Step 1.4: Index System (Fulfills UR-7)
- [ ] Build recipe_index_manager tool
  - [ ] Create summary index structure (recipe_id, tags, prep_time, equipment)
  - [ ] Implement index file generation and updates
  - [ ] Build incremental indexing (only update changed recipes)
  - [ ] Create index query functionality for fast lookups
  - [ ] Test index performance with <1s search target
- [ ] Build search_recipes tool
  - [ ] Implement tag-based filtering functionality
  - [ ] Support multiple tag combinations (AND, OR operations)
  - [ ] Add equipment and time-based filtering
  - [ ] Return ranked search results with relevance scores
  - [ ] Test search accuracy and performance

### Step 1.5: CLI Interface (Fulfills UR-1, UR-7)
- [ ] Create command-line interface for agent
  - [ ] Build CLI commands for recipe processing (process, search, list)
  - [ ] Implement batch processing for entire recipe directories
  - [ ] Add progress indicators for long-running operations
  - [ ] Create configuration file for MCP server endpoints
  - [ ] Add help documentation and usage examples
- [ ] Test complete Phase 1 functionality
  - [ ] Process sample recipe collection
  - [ ] Verify all recipes are tagged correctly
  - [ ] Test search functionality across different criteria
  - [ ] Measure processing speed and search performance
  - [ ] Document any issues and create bug fix todos

---

## Phase 2: Garden Integration (1 week)
**Goal**: Connect meal planning with garden harvest data

### Step 2.1: Garden MCP Tools (Fulfills UR-2)
- [ ] Build read_garden_calendar tool
  - [ ] Define standard garden data format (JSON/YAML schema)
  - [ ] Implement parser for harvest dates and quantities
  - [ ] Create seasonal availability mapping
  - [ ] Handle multiple garden locations/plots
  - [ ] Test with sample garden data
- [ ] Build match_recipes_to_harvest tool
  - [ ] Algorithm to match recipes with available garden produce
  - [ ] Prioritization logic for fresh vs stored ingredients
  - [ ] Generate harvest timing recommendations
  - [ ] Suggest preservation methods for surplus produce
  - [ ] Test seasonal recipe matching accuracy

### Step 2.2: Garden Integration Testing (Fulfills UR-2, UR-7)
- [ ] Create garden data interface for existing garden app
  - [ ] Design API or file-based integration
  - [ ] Implement data synchronization between systems
  - [ ] Test real-time garden data updates
  - [ ] Verify harvest-aware recipe recommendations
- [ ] Test end-to-end garden-to-table workflow
  - [ ] Agent reads garden calendar
  - [ ] Agent suggests recipes based on available harvest
  - [ ] Agent updates meal plans when garden data changes
  - [ ] Verify performance meets <1s response target

---

## Phase 3: Kanban Integration (1 week)
**Goal**: Bidirectional meal planning through Obsidian Kanban boards

### Step 3.1: Kanban Output Tools (Fulfills UR-3)
- [ ] Build generate_kanban_meal_plan tool
  - [ ] Study Obsidian Kanban plugin markdown syntax
  - [ ] Create board template structures (This Week, Prep Queue, Shopping)
  - [ ] Implement customizable board layouts
  - [ ] Generate meal plans in proper Kanban format
  - [ ] Test Kanban output compatibility with Obsidian
- [ ] Reference McKay's App Template for future web UI structure
  - [ ] Document Next.js patterns for Phase 5 web interface
  - [ ] Note UI component approaches (Tailwind + Shadcn)
  - [ ] Plan data flow for web interface integration

### Step 3.2: Kanban Reading Tools (Fulfills UR-4)
- [ ] Build read_kanban_modifications tool
  - [ ] Parse Kanban markdown to extract current state
  - [ ] Track changes between board generations
  - [ ] Identify completed, skipped, and moved items
  - [ ] Extract user modification patterns
  - [ ] Test adaptation to user cooking habits
- [ ] Build learn_user_preferences tool
  - [ ] Implement pattern recognition for scheduling preferences
  - [ ] Track recipe complexity preferences by day of week
  - [ ] Learn equipment usage patterns
  - [ ] Adapt future suggestions based on historical choices
  - [ ] Test continuous learning effectiveness

### Step 3.3: Interactive Planning Loop (Fulfills UR-3, UR-4, UR-7)
- [ ] Build collaborative planning workflow
  - [ ] Monitor Kanban board changes in real-time
  - [ ] Generate alternative suggestions when items are moved/skipped
  - [ ] Update plans based on garden changes and user patterns
  - [ ] Implement feedback loop for improving suggestions
  - [ ] Test collaborative AI sous chef experience

---

## Phase 4: Advanced Intelligence (2-3 weeks)
**Goal**: Sophisticated meal planning with prep optimization

### Step 4.1: Prep Optimization Tools (Fulfills UR-1, UR-4)
- [ ] Build analyze_shared_prep tool
  - [ ] Identify common ingredients across weekly recipes
  - [ ] Map shared preparation steps and techniques
  - [ ] Calculate optimal batch cooking quantities
  - [ ] Generate prep scheduling recommendations
  - [ ] Test professional-level meal prep efficiency
- [ ] Build optimize_kitchen_workflow tool
  - [ ] Analyze equipment usage patterns and conflicts
  - [ ] Generate optimal cooking sequences
  - [ ] Suggest timing to avoid equipment bottlenecks
  - [ ] Create advance prep scheduling
  - [ ] Test workflow optimization effectiveness

### Step 4.2: Learning and Adaptation (Fulfills UR-4)
- [ ] Build continuous_learning_system
  - [ ] Implement pattern recognition for seasonal preferences
  - [ ] Track cooking frequency and success rates
  - [ ] Adapt suggestions based on usage patterns
  - [ ] Create feedback loop for improving recommendations
  - [ ] Test long-term learning and personalization

---

## Phase 5: Community & Sharing (1-2 weeks)
**Goal**: Enable system sharing with broader community

### Step 5.1: Export and Sharing Tools (Fulfills UR-6)
- [ ] Build export_recipe_collection tool
  - [ ] Create standard format for tagged recipe exports
  - [ ] Support multiple output formats (JSON, YAML, Markdown)
  - [ ] Include taxonomy and indexing data
  - [ ] Generate setup instructions for other users
  - [ ] Test sharing with users of different tools
- [ ] Build community_features
  - [ ] Recipe collection import/export functionality
  - [ ] Community-driven tag improvement system
  - [ ] Kanban template sharing capabilities
  - [ ] Test community knowledge sharing

---

## Technical Infrastructure (Ongoing)

### MCP Server Development
- [ ] Set up development environment for MCP servers
- [ ] Create testing framework for MCP tool validation
- [ ] Implement error handling and logging across all tools
- [ ] Create backup and rollback mechanisms
- [ ] Document all MCP tools and their usage

### Agent Development  
- [ ] Implement robust agent loop with error recovery
- [ ] Add configuration management for multiple MCP servers
- [ ] Create logging and debugging capabilities
- [ ] Test agent performance under various load conditions
- [ ] Document agent setup and configuration

### Integration Testing
- [ ] Create end-to-end testing suite
- [ ] Test all MCP server interactions
- [ ] Validate data integrity across processing pipeline
- [ ] Performance testing for response time requirements
- [ ] Create user acceptance testing scenarios

---

## Success Metrics Tracking
- [ ] **Phase 1**: All recipes tagged via MCP architecture, <1s search responses
- [ ] **Phase 2**: Garden integration working through MCP tools, seasonal suggestions relevant
- [ ] **Phase 3**: Kanban generation/reading via MCP tools, user adaptation evident
- [ ] **Phase 4**: Prep optimization MCP tools save measurable time
- [ ] **Phase 5**: System successfully shared with at least 3 other users