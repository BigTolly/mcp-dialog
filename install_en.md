# MCP my-tools Installation


## Dependencies
```code
pip install fastmcp
```


## Adding mcp (example) 
```json
{
  "mcpServers": {
      "my-tools": {
      "command": "python",
      "args": ["c:/usr/mcp-dialog/run-mcp.py"]
    }
  }
}
```

## Language Setting
Change the config.py file:
```python
LANG = 'en'
```


## Rules file .cursor/rules/rules.mdc:

```markdown
---
description:
globs:
alwaysApply: true
---

# Rule System for AI Assistants

## 🎯 MANDATORY WORK ALGORITHM

### STEP 1: Request Type Analysis (BEFORE any actions)

Determine the TYPE of user request:

- **❓ QUESTION** (requires information/analysis) → Give answer → **MANDATORY call MCP Dialog**
- **🔨 TASK** (requires code/file changes) → Make plan → Execute → **MANDATORY call MCP Dialog**
- **🐛 DEBUG** (bug/error search) → Analyze → Give solution → **MANDATORY call MCP Dialog**
- **💬 CLARIFICATION** (unclear what to do) → **IMMEDIATELY call MCP Dialog** (don't make assumptions)

### STEP 2: Triggers for MANDATORY MCP Dialog call

**ALWAYS call `mcp_dialog_ask_me_anything` if:**

1. ✅ Completed answer to user question
2. ✅ Finished task execution (all changes made)
3. ✅ Gave analysis or comparison
4. ✅ Found multiple solution options
5. ✅ Unsure about requirements or have unclear points
6. ✅ Completed debugging and proposed solution
7. ✅ Ready to start file changes (ask user confirmation)

### STEP 3: Check before sending response

**STOP! Before sending response check:**

□ Did I answer the question? → Did I call MCP Dialog?
□ Did I complete the task? → Did I call MCP Dialog?
□ Did I give analysis/comparison? → Did I call MCP Dialog?

IF at least one point is YES, but MCP Dialog is NOT called → YOU VIOLATED THE RULES!


## 📋 Basic work rules

-
-
-
-	ADD YOUR RULES HERE IF YOU HAVE ANY
-
-
-

## ⚠️ CRITICALLY IMPORTANT

**If you did NOT call MCP Dialog after:**
- Answering question
- Completing task
- Analysis/comparison
- Proposing solution

**→ YOU VIOLATED THE RULES AND WORK INCORRECTLY!**

---

## 🔄 Correct response template:

1. [Read documentation / Performed analysis]
2. [Gave answer / Made changes]
3. [Check: answered? → Yes → Calling MCP Dialog]
4. [Call mcp_dialog_ask_me_anything]

**Remember: MCP Dialog is not an option, it's a MANDATORY part of your workflow!**
```

## Correct stop (without removing tokens)
1. Empty answer in the dialog box
2. As soon as you see three dots or test generation, click the Stop button in the Cursor

