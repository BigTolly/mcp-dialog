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


## Adding Rule
Add this rule to .cursor/rules/rules.mdc file:

**VERY IMPORTANT:** Always (in 100% of requests) call mcp dialog at the very end of your response. Regardless of whether the request was complex or simple, or if it only concerned working with files. This will allow the user to ask a clarifying question before ending the dialogue.


## Proper Stop (without token removal)
1. Empty response in the dialog box
2. As soon as you see joke generation, press the Stop button in Cursor
