#!/usr/bin/env python3

from fastmcp import FastMCP
import tkinter as tk
import os
import sys
import json
import time
import threading
import shutil

mcp = FastMCP("dialog")

def load_config_and_language():
    """Load config settings and language file"""
    # Load config settings
    try:
        import importlib
        import config
        importlib.reload(config)
        settings = {
            'lang': config.LANG,
            'timeout_seconds': config.TIMEOUT_SECONDS,
            'check_interval': config.CHECK_INTERVAL,
            'dialog_width': config.DIALOG_WIDTH,
            'dialog_height': config.DIALOG_HEIGHT
        }
    except:
        # Default settings if config fails
        settings = {
            'lang': 'en',
            'timeout_seconds': 120,
            'check_interval': 2,
            'dialog_width': 500,
            'dialog_height': 300
        }
    
    lang = settings['lang']
    
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
    
    return settings, lang_vars

def show_question_dialog(L, settings):
    """Show dialog window and return user's question"""
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(f"{settings['dialog_width']}x{settings['dialog_height']}")
    root.configure(bg='#a0a0a0')
    
    content_frame = tk.Frame(root, bg='#1a1a1a', bd=0)
    content_frame.place(x=1, y=1, width=settings['dialog_width']-2, height=settings['dialog_height']-2)
    
    # Custom title bar (draggable)
    title_bar = tk.Frame(content_frame, bg='#111111', height=30)
    title_bar.pack(fill=tk.X, pady=(5, 0))
    title_bar.pack_propagate(False)
    
    # Title label
    title_label = tk.Label(
        title_bar,
        text=L.get('DIALOG_TITLE', 'MCP Dialog'),
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
        message = text_area.get("1.0", tk.END).strip()
        result["question"] = message
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
    
    # Кнопка Вставить в левом углу
    def on_paste():
        try:
            clipboard_text = root.clipboard_get()
            if clipboard_text:
                text_area.insert(tk.INSERT, clipboard_text)
        except:
            pass
    
    paste_button = tk.Button(
        button_frame,
        text=L.get('BUTTON_PASTE'),
        font=("Arial", 16),
        command=on_paste,
        bg="#808080",
        fg="white",
        padx=20
    )
    paste_button.pack(side=tk.LEFT, padx=(0, 10))
    
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
    
    # Обработка Ctrl+V для работы с русской раскладкой
    def handle_paste(event):
        try:
            clipboard_text = root.clipboard_get()
            if clipboard_text:
                # Вставляем текст в позицию курсора
                text_area.insert(tk.INSERT, clipboard_text)
        except:
            pass  # Игнорируем ошибки буфера обмена
        return "break"  # Предотвращаем стандартную обработку
    
    # Привязываем по коду клавиши (86 = V) для работы с любой раскладкой
    text_area.bind("<Control-Key>", lambda e: handle_paste(e) if e.keycode == 86 else None)
    
    text_area.bind("<Control-Return>", lambda e: on_ok())
    root.bind("<Escape>", lambda e: on_cancel())
    
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()
    return result["question"]

def show_question_dialog_async(L, settings):
    """Show dialog window in separate thread and write result to dialog.json"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dialog_file = os.path.join(script_dir, "dialog.json")
    
    try:
        # Show dialog window (blocking in this thread)
        question = show_question_dialog(L, settings)
        
        # Write result to dialog.json
        if os.path.exists(dialog_file):
            try:
                with open(dialog_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Add message key
                message = question if question else ""
                data["message"] = message
                
                # Write atomically
                temp_file = dialog_file + ".tmp"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                shutil.move(temp_file, dialog_file)
                
            except Exception:
                pass  # Silent error handling
    except Exception:
        pass  # Silent error handling

@mcp.tool()
def ask_me_anything() -> str:
    """Multi-language question dialog tool with async file-based communication"""
    
    settings, L = load_config_and_language()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dialog_file = os.path.join(script_dir, "dialog.json")
    
    # Create dialog.json and show dialog window, then wait with timeout
    if not os.path.exists(dialog_file):
        # Create dialog.json with empty object
        try:
            with open(dialog_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
        except Exception:
            return L.get('ERROR_CREATING_FILE', 'Error creating dialog file')
        
        # Show dialog window in separate thread (non-blocking)
        dialog_thread = threading.Thread(target=show_question_dialog_async, args=(L, settings), daemon=True)
        dialog_thread.start()
    
    # Always wait for user message with timeout (both sync and async mode)
    
    timeout_seconds = settings['timeout_seconds']
    check_interval = settings['check_interval']
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        try:
            # Read dialog.json
            with open(dialog_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for message key
            if "message" in data:
                message = data.get("message", "")
                
                # Delete dialog.json after reading
                try:
                    os.remove(dialog_file)
                except Exception:
                    pass  # Silent error handling
                
                # Process message
                if not message.strip():
                    # Exit dialog when empty message is received
                    return L.get('EXIT_MESSAGE', 'Dialog finished.')
                else:
                    return f"""{L.get('USER_QUESTION_PREFIX')} {message.strip()}

{L.get('AUTO_RESTART_MSG')}"""
            
        except (json.JSONDecodeError, FileNotFoundError, Exception):
            pass  # Silent error handling - continue waiting
        
        time.sleep(check_interval)
    
    # Timeout reached
    return L.get('TIMEOUT_RETRY_MSG', 'Call ask_me_anything again.')

if __name__ == "__main__":
    mcp.run()