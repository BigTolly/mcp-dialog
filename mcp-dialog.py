#!/usr/bin/env python3

from fastmcp import FastMCP
from datetime import datetime
import tkinter as tk
import os
import sys

mcp = FastMCP("dialog")

def load_language():
    """Load language file based on config"""
    try:
        import importlib
        import config
        importlib.reload(config)
        lang = config.LANG
    except:
        lang = 'en'
    
    lang_file = f"lang.{lang}"
    lang_path = os.path.join(os.path.dirname(__file__), lang_file)
    
    if not os.path.exists(lang_path):
        print(f"Language file {lang_file} not found, falling back to English", file=sys.stderr)
        lang_file = "lang.en"
        lang_path = os.path.join(os.path.dirname(__file__), lang_file)
    
    lang_vars = {}
    if os.path.exists(lang_path):
        try:
            with open(lang_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ' = ' in line:
                            key, value = line.split(' = ', 1)
                            if value.startswith('"') and value.endswith('"'):
                                processed_value = value[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
                                lang_vars[key] = processed_value
                            else:
                                lang_vars[key] = value.strip('"')
        except Exception as e:
            print(f"Error loading language file: {e}", file=sys.stderr)
    
    return lang_vars

@mcp.tool()
def ask_me_anything() -> str:
    """Multi-language question dialog tool"""
    
    L = load_language()
    
    def show_question_dialog():
        root = tk.Tk()
        root.overrideredirect(True)
        root.geometry("500x300")
        root.configure(bg='#a0a0a0')
        
        content_frame = tk.Frame(root, bg='#1a1a1a', bd=0)
        content_frame.place(x=1, y=1, width=498, height=298)
        
        # Custom title bar (draggable)
        title_bar = tk.Frame(content_frame, bg='#111111', height=30)
        title_bar.pack(fill=tk.X, pady=(5, 0))
        title_bar.pack_propagate(False)
        
        # Title label
        title_label = tk.Label(
            title_bar,
            text="MCP Dialog",
            font=("Arial", 12),
            bg='#111111',
            fg='#a0a0a0'
        )
        title_label.pack(pady=5)
        
        # Make title bar draggable
        def start_move(event):
            root.x = event.x_root
            root.y = event.y_root
        
        def on_move(event):
            deltax = event.x_root - root.x
            deltay = event.y_root - root.y
            x = root.winfo_x() + deltax
            y = root.winfo_y() + deltay
            root.geometry(f"+{x}+{y}")
            root.x = event.x_root
            root.y = event.y_root
        
        # Bind dragging to title bar and label
        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", on_move)
        title_label.bind("<Button-1>", start_move)
        title_label.bind("<B1-Motion>", on_move)
        
        # Main frame
        main_frame = tk.Frame(content_frame, padx=20, pady=10, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(
            main_frame, 
            text=L.get('DIALOG_QUESTION'),
            font=("Arial", 16),
            justify=tk.LEFT,
            bg='#1a1a1a',
            fg='#a0a0a0'
        )
        label.pack(pady=(0, 10))
        
        text_area = tk.Text(
            main_frame,
            height=4,
            width=50,
            font=("Arial", 16),
            wrap=tk.WORD,
            bg='#2c2c2c',
            fg='#ffffff',
            insertbackground='#ffffff',
            padx=10,
            pady=5,
            relief='flat',
            bd=0
        )
        text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        def steal_focus():
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except:
                pass
            
            root.attributes('-topmost', True)
            root.lift()
            root.focus_force()
            root.grab_set()
            text_area.focus_force()
            text_area.focus_set()
            
            try:
                import ctypes
                hwnd = root.winfo_id()
                ctypes.windll.user32.FlashWindow(hwnd, True)
            except:
                pass
        
        steal_focus()
        root.after(100, steal_focus)
        root.after(300, steal_focus)
        root.after(1000, steal_focus)
        
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        result = {"question": None}
        
        def on_ok():
            result["question"] = text_area.get("1.0", tk.END).strip()
            try:
                root.grab_release()
            except:
                pass
            root.destroy()
        
        def on_cancel():
            result["question"] = None
            try:
                root.grab_release()
            except:
                pass
            root.destroy()
        
        ok_button = tk.Button(
            button_frame,
            text=L.get('BUTTON_OK'),
            font=("Arial", 16),
            command=on_ok,
            bg="#5cb85c",
            fg="white",
            padx=20
        )
        ok_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Info label instead of cancel button
        info_label = tk.Label(
            button_frame,
            text=L.get('INFO_EMPTY_EXIT'),
            font=("Arial", 12),
            bg='#1a1a1a',
            fg='#808080'
        )
        info_label.pack(side=tk.RIGHT, pady=(5, 0))
        
        text_area.bind("<Control-Return>", lambda e: on_ok())
        root.bind("<Escape>", lambda e: on_cancel())
        
        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_width()) // 2
        y = (root.winfo_screenheight() - root.winfo_height()) // 2
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        return result["question"]
    
    question = show_question_dialog()
    
    if not question or not question.strip():
        # Generate AI request for joke generation
        return f"""{L.get('USER_QUESTION_PREFIX')} {L.get('DEFAULT_JOKE_REQUEST')}

{L.get('AUTO_RESTART_MSG')}
    """
    
    # Just return the question for AI to process
    return f"""{L.get('USER_QUESTION_PREFIX')} {question.strip()}

{L.get('AUTO_RESTART_MSG')}
    """

if __name__ == "__main__":
    mcp.run()