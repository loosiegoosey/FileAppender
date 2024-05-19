import win32api
import win32con

def register():
    command = r'"C:\Users\Yuriy\Documents\GitHub\FileAppender\launch_append_files_gui.bat"'
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell\\AppendFilesHere\\command', win32con.REG_SZ, command)
    win32api.RegSetValue(win32con.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell\\AppendFilesHere', win32con.REG_SZ, 'Append Files Here')

if __name__ == "__main__":
    register()
