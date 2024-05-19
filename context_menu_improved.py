import os
import sys
import logging
import tkinter as tk
from tkinter import messagebox, ttk
import configparser
import time
import win32con
import win32api
import win32gui
import win32com.client

class ContextMenuHandler:
    def __init__(self):
        self.hMenu = None
        self.logger = self.setup_logger()
        self.config = self.load_config()

    def setup_logger(self):
        logger = logging.getLogger("ContextMenuHandler")
        handler = logging.FileHandler("context_menu_handler.log", encoding='utf-8')
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
                'OutputDirectory': default_documents_dir,
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
            self.logger.debug(f"Selected files: {files}")
            if files:
                self.append_files(files)

    def get_selected_files(self):
        # Use the shell to get the selected files
        shell = win32com.client.Dispatch("Shell.Application")
        selected_files = []
        for folder in shell.Windows():
            if folder.Document.FocusedItem:
                selected_files.append(folder.Document.FocusedItem.Path)
        self.logger.debug(f"Selected files: {selected_files}")
        return selected_files

    def append_files(self, files):
        try:
            output_directory = self.config['DEFAULT']['OutputDirectory']
            self.logger.debug(f"Output directory: {output_directory}")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            output_file = os.path.join(output_directory, 'appended_files.txt')
            self.logger.debug(f"Output file path: {output_file}")

            with open(output_file, "w", encoding='utf-8') as outfile:
                for file in files:
                    self.process_file(file, outfile)

            self.logger.debug(f"Opening file in Notepad++: {output_file}")
            os.system(f'notepad++ "{output_file}"')
        except Exception as e:
            self.logger.error(f"Error appending files: {e}")
            messagebox.showerror("Error", f"Error appending files: {e}")

    def process_file(self, file, outfile):
        try:
            with open(file, "r", encoding='utf-8') as infile:
                if self.config['DEFAULT'].getboolean('IncludeTimestamp'):
                    outfile.write(f"Timestamp: {time.ctime()}\n")
                outfile.write(f"{os.path.basename(file)} content:\n")
                if self.config['DEFAULT'].getboolean('IncludeFilePath'):
                    outfile.write(f"File path: {file}\n")
                outfile.write(infile.read())
                outfile.write("\n\n")
        except Exception as e:
            self.logger.error(f"Error reading file {file}: {e}")

def register():
    handler = ContextMenuHandler()
    command = f'python "{os.path.abspath(__file__)}" %*'
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles\\command', win32con.REG_SZ, command)
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles', win32con.REG_SZ, 'Append Files')

if __name__ == "__main__":
    register()
