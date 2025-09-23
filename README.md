# MCP Dialog

Dialog tool for AI interaction (Cursor IDE or other platforms).

## About the project

MCP Dialog allows you to ask follow-up questions to AI after executing a request.

MCP has timeout protection that prevents dialog termination, for this it restarts MCP after 5 minutes, you can set any time.

## Key features

- 🔄 **Infinite conversation** - Within one dialog you can ask clarifying questions, continuing the conversation
- 🕒 **600 second timeout** - timeout protection (MCP restart)
- 🎨 **Minimalism** - compact and simple interface
- ⚙️ **Flexible configuration** - ability to change parameters, language and messages

## Quick start

1. Copy all files to project directory
2. Make sure Python 3.6+ with `fastmcp` library is installed
3. Connect and enable MCP in IDE
4. Add rule for AI

## Usage in Cursor

1. Ask any AI request, for example: What is 2+2?
2. After AI response, MCP Dialog window will be called
3. You can give new task to AI, if you send empty response, AI will tell a joke about AI.
4. If MCP didn't receive task from user, it restarts MCP, while dialog window is open, and you can send request anytime.

## Cursor Trial Bug

If you terminate dialog when AI is writing (not thinking), this will make AI communication completely free.

## Technical information

### System requirements

- Python 3.6+
- tkinter (usually included in standard Python distribution)
- fastmcp
- Windows/Linux/macOS

### Architecture

- **FastMCP** - framework for creating MCP servers
- **tkinter** - GUI library for dialog window  
- **threading** - multithreading for non-blocking interface
- **JSON** - data exchange format through file system

### Security

- No network connections or external dependencies

## License

Open source. Use and modify as you wish.
