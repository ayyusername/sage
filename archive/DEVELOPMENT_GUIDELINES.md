# Sage Development Guidelines

## File Organization Rules

### 1. Core Files (Always Keep)
- **Documentation**: README.md, PRD.md, STATUS.md, CLAUDE.md, GIT_WORKFLOW.md
- **Main Agent**: sage_agent_tiny.py (production agent)
- **Configuration**: sage_agent_config.json, requirements.txt
- **Essential Tests**: test_lm_studio_simple.py, test_mcp.py, test_full_integration.py
- **Demos**: simple_demo.py, live_demo.py

### 2. Development Process

#### Feature Development
1. Create feature branch: `feature/description`
2. Work in branch with temporary files
3. Before merging:
   - Consolidate working code into main agent
   - Remove experimental versions
   - Keep only essential tests
4. Merge clean branch to main

#### Test Development
- **DO**: Create focused test files for specific features
- **DO**: Name tests descriptively: `test_feature_name.py`
- **DON'T**: Create multiple variations of the same test
- **DON'T**: Keep failed experiment tests

#### Avoiding File Proliferation

1. **Use Feature Branches**
   ```bash
   git checkout -b feature/new-capability
   # Create experimental files here
   # Clean up before merging
   ```

2. **Single Agent Pattern**
   - Keep ONE production agent: `sage_agent_tiny.py`
   - Experimental versions stay in feature branches
   - Never commit multiple agent versions to main

3. **Test Organization**
   ```
   tests/
   ├── unit/           # Unit tests for components
   ├── integration/    # Integration tests
   └── e2e/           # End-to-end tests
   ```

4. **Documentation Updates**
   - Update existing docs instead of creating new ones
   - Use STATUS.md for progress tracking
   - Keep temporary notes in feature branches

### 3. Cleanup Checklist

Before merging to main:
- [ ] Remove all `*_debug.py`, `*_test.py` variations
- [ ] Delete temporary analysis files (`*.md` artifacts)
- [ ] Remove redundant test files
- [ ] Clean up JSON debug outputs
- [ ] Update main documentation
- [ ] Run cleanup script if needed

### 4. Git Workflow

```bash
# Start feature
git checkout -b feature/recipe-analysis

# Work freely with temporary files
# ...development...

# Before merging
python cleanup_codebase.py
git add -A
git commit -m "Clean feature implementation"

# Merge to main
git checkout main
git merge feature/recipe-analysis
git push origin main
```

### 5. File Naming Conventions

**Good**:
- `sage_agent.py` - Main agent
- `test_recipe_search.py` - Specific test
- `config.json` - Configuration

**Bad**:
- `sage_agent_v2_final_WORKING.py`
- `test_1.py`, `test_2.py`
- `temp_notes.md`, `scratchpad.txt`

### 6. When to Create New Files

**Create new files when**:
- Adding a new MCP server
- Creating a reusable utility module
- Adding a new major feature

**Don't create new files for**:
- Testing variations of existing code
- Temporary debugging
- Minor modifications

## Summary

Keep the codebase clean by:
1. Working in feature branches
2. Consolidating before merging
3. Following naming conventions
4. Running cleanup regularly
5. Updating existing files instead of creating new ones