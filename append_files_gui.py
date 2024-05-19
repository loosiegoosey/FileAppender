import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import time
from tkinter import ttk

class FileAppenderApp:
    def __init__(self, root, initial_dir):
        self.root = root
        self.initial_dir = initial_dir
        self.selected_files = []
        self.setup_logger()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_logger(self):
        self.logger = logging.getLogger("FileAppenderApp")
        handler = logging.FileHandler("file_appender.log", encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.log_handler = handler

    def create_widgets(self):
        self.root.title("Append Files")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12))
        style.configure('TLabel', font=('Helvetica', 12))
        
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = ttk.Label(main_frame, text="Select files to append:")
        self.label.pack(pady=10)

        self.select_button = ttk.Button(main_frame, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=10)

        self.files_frame = ttk.Frame(main_frame)
        self.files_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.files_listbox = tk.Listbox(self.files_frame, height=10, width=80)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.files_frame, orient=tk.HORIZONTAL, command=self.files_listbox.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.files_listbox.config(xscrollcommand=self.scrollbar.set)

        self.append_button = ttk.Button(main_frame, text="Append Files", command=self.append_files, state=tk.DISABLED)
        self.append_button.pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(initialdir=self.initial_dir, title="Select Files to Append")
        if files:
            self.selected_files = files
            self.files_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.files_listbox.insert(tk.END, file)
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

            messagebox.showinfo("Success", f"Files have been appended to {output_file}")

        except Exception as e:
            self.logger.error(f"Error appending files: {e}")
            messagebox.showerror("Error", f"Error appending files: {e}")

    def process_file(self, file, outfile):
        try:
            with open(file, "r", encoding='utf-8') as infile:
                outfile.write(f"{os.path.basename(file)} content:\n")
                outfile.write(infile.read())
                outfile.write("\n\n")
        except Exception as e:
            self.logger.error(f"Error reading file {file}: {e}")

    def on_closing(self):
        try:
            # Close the logger handlers to release the log file
            self.logger.removeHandler(self.log_handler)
            self.log_handler.close()
            
            log_file = "file_appender.log"
            if os.path.exists(log_file):
                os.remove(log_file)
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
        self.root.destroy()

def main():
    initial_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~')
    root = tk.Tk()
    app = FileAppenderApp(root, initial_dir)
    root.mainloop()

if __name__ == "__main__":
    main()
