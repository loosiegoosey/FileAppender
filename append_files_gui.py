import os
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import configparser
import time

class FileAppenderApp:
    def __init__(self, root, initial_dir):
        self.root = root
        self.initial_dir = initial_dir
        self.setup_logger()
        self.load_config()
        self.create_widgets()

    def setup_logger(self):
        self.logger = logging.getLogger("FileAppenderApp")
        handler = logging.FileHandler("file_appender.log", encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def load_config(self):
        self.config = configparser.ConfigParser()
        config_file = "context_menu_config.ini"
        default_documents_dir = os.path.expanduser('~\\Documents')
        if not os.path.exists(config_file):
            self.config['DEFAULT'] = {
                'OutputDirectory': default_documents_dir,
                'IncludeFilePath': 'False',
                'IncludeTimestamp': 'False'
            }
            with open(config_file, 'w') as configfile:
                self.config.write(configfile)
        else:
            self.config.read(config_file)

        # Use default_documents_dir if OutputDirectory is not set or empty
        if not self.config['DEFAULT']['OutputDirectory']:
            self.config['DEFAULT']['OutputDirectory'] = default_documents_dir

    def create_widgets(self):
        self.root.title("Append Files")
        self.select_button = tk.Button(self.root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=20)
        self.append_button = tk.Button(self.root, text="Append Files", command=self.append_files, state=tk.DISABLED)
        self.append_button.pack(pady=20)
        self.selected_files = []

    def select_files(self):
        files = filedialog.askopenfilenames(initialdir=self.initial_dir, title="Select Files to Append")
        if files:
            self.selected_files = files
            self.append_button.config(state=tk.NORMAL)
            self.logger.debug(f"Selected files: {self.selected_files}")

    def append_files(self):
        try:
            output_directory = self.initial_dir
            self.logger.debug(f"Output directory: {output_directory}")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            output_file = os.path.join(output_directory, 'appended_files.txt')
            self.logger.debug(f"Output file path: {output_file}")

            with open(output_file, "w", encoding='utf-8') as outfile:
                for file in self.selected_files:
                    self.logger.debug(f"Processing file: {file}")
                    self.process_file(file, outfile)

            self.logger.debug(f"Opening file in Notepad++: {output_file}")
            os.system(f'notepad++ "{output_file}"')
            messagebox.showinfo("Success", f"Files have been appended to {output_file}")
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

def main():
    initial_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~')
    root = tk.Tk()
    app = FileAppenderApp(root, initial_dir)
    root.mainloop()

if __name__ == "__main__":
    main()
