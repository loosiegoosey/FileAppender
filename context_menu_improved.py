import os
import sys
import logging
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import configparser
import time
import win32con
import win32api
import win32gui
import win32com.client
from win32com.shell import shell, shellcon

class ContextMenuHandler:
    def __init__(self):
        self.hMenu = None
        self.logger = self.setup_logger()
        self.config = self.load_config()

    def setup_logger(self):
        logger = logging.getLogger("ContextMenuHandler")
        handler = logging.FileHandler("context_menu_handler.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def load_config(self):
        config = configparser.ConfigParser()
        config_file = "context_menu_config.ini"
        default_documents_dir = os.path.expanduser('~\\Documents')
        if not os.path.exists(config_file):
            config['DEFAULT'] = {
                'OutputDirectory': '',
                'IncludeFilePath': 'False',
                'IncludeTimestamp': 'False'
            }
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        else:
            config.read(config_file)

        # Use default_documents_dir if OutputDirectory is not set or empty
        if not config['DEFAULT']['OutputDirectory']:
            config['DEFAULT']['OutputDirectory'] = default_documents_dir

        return config

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
            if files:
                self.append_files_with_gui(files)

    def get_selected_files(self):
        return sys.argv[1:]  # Get file paths from command-line arguments

    def show_settings_dialog(self, files):
        settings_dialog = tk.Tk()
        settings_dialog.title("Settings")

        ttk.Label(settings_dialog, text="Output Directory:").grid(column=0, row=0, padx=10, pady=5, sticky='W')
        output_dir_entry = ttk.Entry(settings_dialog, width=50)
        output_dir_entry.insert(0, self.config['DEFAULT']['OutputDirectory'])
        output_dir_entry.grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(settings_dialog, text="Include File Path:").grid(column=0, row=1, padx=10, pady=5, sticky='W')
        include_file_path = tk.BooleanVar(value=self.config['DEFAULT'].getboolean('IncludeFilePath'))
        ttk.Checkbutton(settings_dialog, variable=include_file_path).grid(column=1, row=1, padx=10, pady=5, sticky='W')

        ttk.Label(settings_dialog, text="Include Timestamp:").grid(column=0, row=2, padx=10, pady=5, sticky='W')
        include_timestamp = tk.BooleanVar(value=self.config['DEFAULT'].getboolean('IncludeTimestamp'))
        ttk.Checkbutton(settings_dialog, variable=include_timestamp).grid(column=1, row=2, padx=10, pady=5, sticky='W')

        def on_save():
            self.config['DEFAULT']['OutputDirectory'] = output_dir_entry.get()
            self.config['DEFAULT']['IncludeFilePath'] = str(include_file_path.get())
            self.config['DEFAULT']['IncludeTimestamp'] = str(include_timestamp.get())
            with open("context_menu_config.ini", 'w') as configfile:
                self.config.write(configfile)
            settings_dialog.destroy()
            self.append_files_with_gui(files)

        ttk.Button(settings_dialog, text="Save", command=on_save).grid(column=0, row=3, columnspan=2, pady=10)

        settings_dialog.mainloop()

    def append_files_with_gui(self, files):
        try:
            output_file = os.path.join(self.config['DEFAULT']['OutputDirectory'], 'appended_files.txt')

            progress = tk.Tk()
            progress.title("Appending Files")
            ttk.Label(progress, text="Appending files...").grid(column=0, row=0, padx=10, pady=10)
            pb = ttk.Progressbar(progress, orient="horizontal", mode="determinate", length=300)
            pb.grid(column=0, row=1, padx=10, pady=10)
            pb["maximum"] = len(files)
            progress.update_idletasks()

            threads = []
            for i, file in enumerate(files):
                thread = threading.Thread(target=self.process_file, args=(file, output_file, pb, i, progress))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            progress.destroy()
            os.system(f'notepad++ "{output_file}"')
        except Exception as e:
            self.logger.error(f"Error appending files: {e}")
            messagebox.showerror("Error", f"Error appending files: {e}")

    def process_file(self, file, output_file, pb, index, progress):
        retry_attempts = 3
        while retry_attempts > 0:
            try:
                with open(file, "r", encoding='utf-8') as infile:
                    with open(output_file, "a", encoding='utf-8') as outfile:
                        if self.config['DEFAULT'].getboolean('IncludeTimestamp'):
                            outfile.write(f"Timestamp: {time.ctime()}\n")
                        outfile.write(f"{os.path.basename(file)} content:\n")
                        if self.config['DEFAULT'].getboolean('IncludeFilePath'):
                            outfile.write(f"File path: {file}\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")
                pb["value"] = index + 1
                progress.update_idletasks()
                return
            except Exception as e:
                self.logger.error(f"Error reading file {file}: {e}")
                retry_attempts -= 1
                time.sleep(1)
        self.logger.error(f"Failed to read file {file} after multiple attempts")

def register():
    handler = ContextMenuHandler()
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles\\command', win32con.REG_SZ, f'python "{os.path.abspath(__file__)}" "%1"')
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles', win32con.REG_SZ, 'Append Files')

if __name__ == "__main__":
    register()
