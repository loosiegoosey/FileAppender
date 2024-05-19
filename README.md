# File Appender

This project provides a simple GUI application that allows users to select multiple files and append their contents into a single file. The resulting file is saved in the directory where the context menu option "Append Files Here" is selected.

## Features

- Graphical User Interface (GUI) for selecting files to append.
- Context menu integration for easy access.
- Automatically cleans up temporary files created during the process.

## Prerequisites

- Python 3.x
- Tkinter library (usually included with Python)
- `win32api` and `win32con` libraries (`pywin32` package)
- Windows operating system

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/FileAppender.git
    cd FileAppender
    ```

2. **Install required Python packages:**
    ```sh
    pip install pywin32
    ```

## Files in the Project

- `append_files_gui.py`: The main Python script for the GUI.
- `launch_append_files_gui.bat`: Batch file to launch the GUI with elevated privileges.
- `register_context_menu.py`: Python script to register the context menu item.
- `deregister_context_menu.py`: Python script to deregister the context menu item.
- `register_context_menu.bat`: Batch file to register the context menu item with elevated privileges.
- `deregister_context_menu.bat`: Batch file to deregister the context menu item with elevated privileges.

## Usage

### Register the Context Menu Item

To add the "Append Files Here" option to the context menu:

1. **Run the `register_context_menu.bat` file with elevated privileges:**
    - Double-click `register_context_menu.bat`.
    - This will request administrative privileges and run the registration script.

### Use the Context Menu Item

1. **Right-click in the background of a folder in Windows Explorer.**
2. **Select "Append Files Here".**
3. **The GUI application will open, allowing you to select files to append.**
4. **The appended content will be saved to `appended_files.txt` in the selected directory.**

### Deregister the Context Menu Item

To remove the "Append Files Here" option from the context menu:

1. **Run the `deregister_context_menu.bat` file with elevated privileges:**
    - Double-click `deregister_context_menu.bat`.
    - This will request administrative privileges and run the deregistration script.

## Cleanup

The application will automatically clean up any temporary files it creates, such as `file_appender.log`.

## Troubleshooting

- If the context menu item does not appear, ensure you have run the `register_context_menu.bat` file with administrative privileges.
- If you encounter any issues, check the `file_appender.log` file for debugging information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
