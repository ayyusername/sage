# Sage Git Workflow Framework

## Current Status ✅
- **Repository**: Initialized with `main` branch
- **Initial Commit**: Step 1.1 MCP Server Setup complete
- **Test Suite**: Comprehensive testing framework committed

## Branching Strategy

### Main Branches
- **`main`**: Production-ready code, stable releases
- **`develop`**: Integration branch for features

### Feature Branches
- **`feature/step-1.2-recipe-tools`**: Next - Sage MCP Server implementation
- **`feature/step-1.3-indexing`**: Fast index system
- **`feature/step-1.4-cli`**: Command-line interface
- **`feature/phase-2-garden`**: Garden integration
- **`feature/phase-3-kanban`**: Kanban integration

### Workflow Pattern
```bash
# For each new step/feature:
git checkout main
git pull origin main
git checkout -b feature/step-X.Y-description
# ... implement feature ...
git add .
git commit -m "Implement Step X.Y: Description"
git checkout main
git merge feature/step-X.Y-description
git tag v1.X.Y
```

## Commit Message Format

### Structure
```
<type>: <description>

<body with details>

🌿 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Types
- **feat**: New feature implementation
- **test**: Add or update tests
- **docs**: Documentation updates
- **config**: Configuration changes
- **fix**: Bug fixes
- **refactor**: Code restructuring

## Current Git State

```bash
main branch (2 commits):
├── aa2902b - Initial commit: Step 1.1 MCP Server Setup complete
└── 96c0485 - Add comprehensive testing suite for Step 1.1
```

## Next Steps

### For Step 1.2 Implementation:
```bash
git checkout -b feature/step-1.2-sage-mcp-server
# Implement recipe processing tools
git commit -m "feat: implement Sage MCP server with culinary tools"
git checkout main  
git merge feature/step-1.2-sage-mcp-server
git tag v1.2.0
```

## File Organization

### Tracked Files
- **Core**: `sage_agent_tiny.py`, configurations
- **Documentation**: `README.md`, `PRD.md`, `CLAUDE.md`
- **Tests**: All `test_*.py` files
- **Data**: `test-recipes/` sample collection

### Ignored Files (`.gitignore`)
- `mcp-servers/` (external dependency)
- `__pycache__/`, `node_modules/`
- IDE files, OS files, logs

## Remote Repository Setup (Future)

When ready to push to remote:
```bash
# Add remote origin
git remote add origin <repository-url>
git push -u origin main

# Push tags
git push --tags
```

## Release Management

### Version Tagging
- **v1.1.0**: Step 1.1 - MCP Server Setup ✅
- **v1.2.0**: Step 1.2 - Recipe Processing Tools (Next)
- **v1.3.0**: Step 1.3 - Fast Index System
- **v1.4.0**: Step 1.4 - CLI Interface
- **v2.0.0**: Phase 2 - Garden Integration
- **v3.0.0**: Phase 3 - Kanban Integration

## Best Practices

1. **Atomic Commits**: Each commit represents one logical change
2. **Descriptive Messages**: Clear what and why, not just what
3. **Feature Branches**: Isolate development work
4. **Regular Integration**: Merge to main frequently
5. **Tag Releases**: Mark stable milestones
6. **Test Before Commit**: Ensure working state

---

**Current Focus**: Ready to branch for Step 1.2 - Sage MCP Server implementation! 🌿