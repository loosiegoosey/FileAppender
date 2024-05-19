import os
import sys
import logging
import configparser
import time
import win32con
import win32api

class ContextMenuHandler:
    def __init__(self):
        self.logger = self.setup_logger()
        self.config = self.load_config()

    def setup_logger(self):
        logger = logging.getLogger("ContextMenuHandler")
        handler = logging.FileHandler("context_menu_handler.log", encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
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
                    self.logger.debug(f"Processing file: {file}")
                    self.process_file(file, outfile)

            self.logger.debug(f"Opening file in Notepad++: {output_file}")
            os.system(f'notepad++ "{output_file}"')
        except Exception as e:
            self.logger.error(f"Error appending files: {e}")
            print(f"Error appending files: {e}")

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
    command = r'"C:\Users\Yuriy\Documents\GitHub\FileAppender\run_append_files.bat" %*'
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles\\command', win32con.REG_SZ, command)
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'*\\shell\\AppendFiles', win32con.REG_SZ, 'Append Files')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handler = ContextMenuHandler()
        handler.logger.debug(f"Command-line arguments: {sys.argv}")
        handler.append_files(sys.argv[1:])
    else:
        register()
