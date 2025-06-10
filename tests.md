# File Search Agent Test Suite

## Test-Driven Design for Step 1.2.1 Completion

**Architecture Under Test:**
- Tiny-agents framework + LM Studio + File System MCP
- 10 vegan recipe files in `/Users/josh/Rose/sage/test-recipes/`
- Available tools: `list_directory`, `read_file`, `search_files`, etc.

**Current Problems to Solve:**
1. Model doesn't read file contents (only lists files)
2. Model hallucinates non-existent files
3. Model doesn't analyze content to match user queries
4. Generic responses instead of specific file-based answers

---

## Test 1: Basic File Discovery
**Complexity:** ⭐ (Simple)
**Goal:** Verify model can list actual files without hallucination

**User Query:** "What recipe files do you have available?"

**Success Criteria:**
- ✅ Calls `list_directory` with correct path
- ✅ Returns ALL 10 actual recipe filenames
- ✅ No hallucinated/fake files mentioned
- ✅ Response format: Clear list of actual .md files

**Expected Tools Used:** `list_directory`

---

## Test 2: Specific File Content Reading
**Complexity:** ⭐⭐ (Content Access)
**Goal:** Verify model reads actual file contents when asked

**User Query:** "Show me the ingredients in the Cashew Alfredo recipe"

**Success Criteria:**
- ✅ Calls `list_directory` to find files (if needed)
- ✅ Calls `read_file` on `sample-recipe.md` 
- ✅ Returns actual ingredients: cashews, garlic, nutritional yeast, lemon, salt, pepper
- ✅ No made-up ingredients
- ✅ Response based on actual file content

**Expected Tools Used:** `list_directory`, `read_file`

---

## Test 3: Content-Based Recipe Matching
**Complexity:** ⭐⭐⭐ (Analysis & Matching)
**Goal:** Verify model reads multiple files and matches content to user criteria

**User Query:** "Find me vegan pasta recipes"

**Success Criteria:**
- ✅ Calls `list_directory` to get all files
- ✅ Calls `read_file` on multiple relevant files
- ✅ Identifies `sample-recipe.md` (Cashew Alfredo - pasta sauce)
- ✅ Identifies `pasta-aglio-e-olio.md` (Italian pasta)
- ✅ Explains WHY each recipe matches (contains pasta + vegan)
- ✅ No hallucinated recipes

**Expected Tools Used:** `list_directory`, `read_file` (multiple calls)

---

## Test 4: Comparative Analysis & Recommendation
**Complexity:** ⭐⭐⭐⭐ (Multi-file Analysis)
**Goal:** Verify model can read, compare, and recommend based on specific criteria

**User Query:** "I want to make something quick for lunch that's high in protein. What do you recommend and why?"

**Success Criteria:**
- ✅ Calls `list_directory` to survey options
- ✅ Calls `read_file` on 3+ relevant recipes
- ✅ Analyzes prep times from actual file content
- ✅ Identifies protein sources (beans, seitan, nuts) from ingredients
- ✅ Recommends specific recipes with reasoning: 
  - "Chickpea Salad (15 min, high protein from chickpeas)"
  - "Italian Broccoli Salad (quick prep, protein from almonds)"
- ✅ Explanation based on actual recipe details, not hallucination

**Expected Tools Used:** `list_directory`, `read_file` (multiple), content analysis

---

## Test 5: Complex Multi-Criteria Search & Ranking
**Complexity:** ⭐⭐⭐⭐⭐ (Advanced Tool Orchestration)
**Goal:** Verify model can perform sophisticated search with multiple filters and ranking

**User Query:** "I'm having guests over and want to impress them with something sophisticated but not too time-consuming. I have mushrooms, cashews, and nutritional yeast on hand. What are my best options, ranked by impressiveness vs. effort?"

**Success Criteria:**
- ✅ Calls `list_directory` for complete inventory
- ✅ Calls `read_file` on ALL relevant recipes (4-6 files)
- ✅ Identifies recipes containing available ingredients:
  - Cashew Alfredo (cashews, nutritional yeast)
  - Vegan Beef Wellington (mushrooms, sophisticated)
  - Vegan Caramelized Onion Dip (sophisticated appetizer)
- ✅ Analyzes complexity/time requirements from actual instructions
- ✅ Ranks recommendations with reasoning:
  1. "Vegan Beef Wellington - Most impressive but advanced difficulty"
  2. "Cashew Alfredo - Uses your ingredients, sophisticated but easier" 
  3. "Caramelized Onion Dip - Impressive appetizer, moderate effort"
- ✅ Provides specific next steps: "Would you like me to read the full Wellington recipe?"
- ✅ All analysis based on actual file content, zero hallucination

**Expected Tools Used:** `list_directory`, `read_file` (5+ calls), `search_files` (potentially), sophisticated reasoning

---

## Success Metrics

**Test 1-2:** Basic MCP tool usage (Foundation)
**Test 3-4:** Content analysis and matching (Core functionality) 
**Test 5:** Advanced orchestration (Full capability)

**Overall Success:** Pass all 5 tests consistently = Step 1.2.1 Complete ✅