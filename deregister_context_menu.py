import win32api
import win32con

def deregister():
    try:
        win32api.RegDeleteKey(win32con.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell\\AppendFilesHere\\command')
        win32api.RegDeleteKey(win32con.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell\\AppendFilesHere')
        print("Context menu item deregistered successfully.")
    except Exception as e:
        print(f"Error deregistering context menu item: {e}")

if __name__ == "__main__":
    deregister()
