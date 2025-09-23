#!/usr/bin/env python3

import sys
import os
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the main MCP server file
    mcp_file = os.path.join(script_dir, "mcp-dialog.py")
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Run the MCP server
    try:
        subprocess.run([sys.executable, mcp_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nMCP server stopped by user", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
