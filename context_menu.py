import os
import sys
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import win32con
import win32api
import win32gui
import win32com.client
from win32com.shell import shell, shellcon

class ContextMenuHandler:
    def __init__(self):
        self.hMenu = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("ContextMenuHandler")
        handler = logging.FileHandler("context_menu_handler.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def add_context_menu_item(self, hMenu, menu_text, command_id):
        win32gui.InsertMenu(hMenu, 0, win32con.MF_BYPOSITION | win32con.MF_STRING, command_id, menu_text)
        return command_id + 1

    def query_context_menu(self, hMenu, indexMenu, idCmdFirst, idCmdLast, uFlags):
        self.hMenu = hMenu
        command_id = idCmdFirst
        command_id = self.add_context_menu_item(hMenu, "Append Files", command_id)
        return command_id - idCmdFirst

    def invoke_command(self, lpici):
        if lpici.lpVerb == 0:  # "Append Files" command id
            files = self.get_selected_files()
            self.append_files_with_gui(files)

    def get_selected_files(self):
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.Namespace(os.getcwd())
        items = folder.Items()
        selected_files = [item.Path for item in items if item.IsSelected]
        return selected_files

    def append_files_with_gui(self, files):
        try:
            root = tk.Tk()
            root.withdraw()
            output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if not output_file:
                return

            progress = tk.Tk()
            progress.title("Appending Files")
            ttk.Label(progress, text="Appending files...").grid(column=0, row=0, padx=10, pady=10)
            pb = ttk.Progressbar(progress, orient="horizontal", mode="determinate", length=300)
            pb.grid(column=0, row=1, padx=10, pady=10)
            pb["maximum"] = len(files)
            progress.update_idletasks()

            with open(output_file, "w", encoding='utf-8') as outfile:
                for i, file in enumerate(files):
                    try:
                        with open(file, "r", encoding='utf-8') as infile:
                            outfile.write(f"{os.path.basename(file)} content:\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except Exception as e:
                        self.logger.error(f"Error reading file {file}: {e}")
                        continue
                    pb["value"] = i + 1
                    progress.update_idletasks()

            progress.destroy()
            os.system(f'notepad++ {output_file}')
        except Exception as e:
            self.logger.error(f"Error appending files: {e}")
            messagebox.showerror("Error", f"Error appending files: {e}")

def register():
    handler = ContextMenuHandler()
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles\\command', win32con.REG_SZ, f'python {os.path.abspath(__file__)} %1')
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles', win32con.REG_SZ, 'Append Files')

if __name__ == "__main__":
    register()
