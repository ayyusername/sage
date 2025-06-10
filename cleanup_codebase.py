#!/usr/bin/env python3
"""
Sage Codebase Cleanup Script
Removes development/test files while preserving core functionality
"""

import os
import shutil
from pathlib import Path

# Files to keep (core functionality)
KEEP_FILES = {
    # Core documentation
    "README.md",
    "PRD.md",
    "STATUS.md",
    "CLAUDE.md",
    "GIT_WORKFLOW.md",
    "agent_flowchart.md",
    
    # Core agent files (based on USAGE.md)
    "sage_agent_tiny.py",  # Current main agent
    "requirements.txt",
    "sage_agent_config.json",
    
    # Essential test files
    "test_mcp.py",  # Tests MCP server communication
    "test_full_integration.py",  # Complete system integration test
    "simple_demo.py",
    "live_demo.py",
    
    # Cleanup scripts
    "cleanup_codebase.py",
}

# Directories to keep
KEEP_DIRS = {
    "mcp-servers",
    "test-recipes",  # Keep one sample recipe
    ".git",
    "__pycache__",
}

# Files to definitely remove (development artifacts)
REMOVE_PATTERNS = [
    # Development versions of agent
    "sage_agent_accurate.py",
    "sage_agent_clean.py", 
    "sage_agent_debug.py",
    "sage_agent_final.py",
    "sage_agent_production.py",
    "sage_agent_simple.py",
    "sage_agent_working.py",
    
    # Test variations
    "test_*_only.py",
    "test_comprehensive.py",
    "test_edge_chaos.py",
    "test_extraction.py",
    "test_file_*.py",
    "test_flexible_agent.py",
    "test_focused.py",
    "test_long_timeout.py",
    "test_minimal.py",
    "test_obsidian_*.py",
    "test_prompt_*.py",
    "test_real_*.py",
    "test_runner.py",
    "test_simple_file_search.py",
    "test_single.py",
    "test_surgical.py",
    "test_vault_*.py",
    "test_verification.py",
    "test_agent_only.py",
    "test_tiny_agent.py",
    
    # Development tools
    "debug_*.json",
    "debug_viewer.html",
    "generate_debug_log.py",
    "prompt_tester.py",
    "quick_test.py",
    "run_final_tests.py",
    
    # Demo/showcase files
    "demo.py",
    "showcase.py",
    "interactive_file_search.py",
    "proper_file_search.py",
    "flexible_chat.py",
    
    # Web interface (not part of MVP)
    "web_server.py",
    "web_ui.html",
    
    # Documentation artifacts
    "HALLUCINATION_ANALYSIS.md",
    "SOLUTIONS_SUMMARY.md", 
    "STEP_1.2.1_COMPLETE.md",
    "tests.md",
    "scratchpad.md",
    "promptpad.md",
    "todo.md",  # Keep main TODO in PRD
    "USAGE.md",  # Integrate into README
    
    # Scripts
    "clean_start_sage.sh",
    "start_sage_agent.sh",
    
    # JSON artifacts
    "latest_debug.json",
]

def should_remove(filepath):
    """Check if file should be removed"""
    name = os.path.basename(filepath)
    
    # Keep essential files
    if name in KEEP_FILES:
        return False
        
    # Check removal patterns
    for pattern in REMOVE_PATTERNS:
        if pattern.endswith("*"):
            if name.startswith(pattern[:-1]):
                return True
        elif "*" in pattern:
            prefix, suffix = pattern.split("*")
            if name.startswith(prefix) and name.endswith(suffix):
                return True
        elif name == pattern:
            return True
            
    return False

def cleanup_test_recipes():
    """Keep only one sample recipe"""
    recipes_dir = Path("test-recipes")
    if recipes_dir.exists():
        recipes = list(recipes_dir.glob("*.md"))
        if len(recipes) > 1:
            # Keep sample-recipe.md as the example
            for recipe in recipes:
                if recipe.name != "sample-recipe.md":
                    print(f"  Removing extra recipe: {recipe.name}")
                    recipe.unlink()

def main():
    """Run cleanup"""
    print("Sage Codebase Cleanup")
    print("=" * 50)
    
    removed_count = 0
    
    # Clean root directory files
    print("\nCleaning root directory files...")
    for item in os.listdir("."):
        if os.path.isfile(item) and should_remove(item):
            print(f"  Removing: {item}")
            os.remove(item)
            removed_count += 1
    
    # Clean test recipes (keep only sample)
    print("\nCleaning test recipes...")
    cleanup_test_recipes()
    
    print(f"\nCleanup complete! Removed {removed_count} files.")
    print("\nCore files preserved:")
    for item in sorted(os.listdir(".")):
        if os.path.isfile(item) and item in KEEP_FILES:
            print(f"  ✓ {item}")

if __name__ == "__main__":
    main()