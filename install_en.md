# MCP my-tools Installation


## Dependencies
pip install fastmcp


## Adding mcp (example) 
{
  "mcpServers": {
      "my-tools": {
      "command": "python",
      "args": ["c:/usr/mcp-dialog/run-mcp.py"]
    }
  }
}


## Language Setting
Change the config.py file:
LANG = 'en'



## Rules file .cursor/rules/rules.mdc:

```markdown
---
description:
globs:
alwaysApply: true
---

## Basic Rules:
-
- Add your own rules here, if any.
-
## 🚨 CRITICAL RULES (preventing dialogue termination):
- You MUST NOT terminate a dialogue/request yourself until you receive explicit confirmation from the "Dialog" MCP.
- You MUST ONLY ask questions through the "Dialog" MCP. Asking questions directly or ending a task with a question is PROHIBITED.
- If requirements are unclear, use the "Dialog" MCP to clarify details.
- If there are multiple solutions, call the "Dialog" MCP, suggest your options first, and do not make a decision yourself.
- When updating a plan/strategy, use the "Dialog" MCP to ask questions; do not make a decision yourself.
- Before completing a request, you MUST call the "Dialog" MCP to receive feedback.
```

## Correct stop (without removing tokens)
1. Empty answer in the dialog box
2. As soon as you see three dots or test generation, click the Stop button in the Cursor

