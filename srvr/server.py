"""
Edan Jacobson
File: Technician server
"""
import os
import socket
import sys
import threading

from constants import *
from protocol import Protocol


class Server(object):
    def __init__(self, ip, port):
        """
        Constructor for server
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((ip, port))
            self.server_socket.listen(LISTEN)
        except socket.error as msg:
            print("Connection failure: %s\n terminating program" % msg)
            sys.exit(EXIT)

    @staticmethod
    def check_for_directory(user):
        """
        Method that checks if user has existing directory
        :param user:
        :return:
        """
        dir_path = os.path.join(USER_DATABASE_DIRECTORY, user)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    @staticmethod
    def receive_client_request(client_socket):
        """
        Method that receives client socket and returns what
         was received from socket
        :param client_socket:
        """
        request = Protocol.recv(client_socket).decode()
        if request == "":
            return None, None
        request_and_params = request.split(":")
        if len(request_and_params) > TWO_PARAM:
            return request_and_params[REQUEST].upper(), \
                ":".join(request_and_params[SECOND:])
        else:
            return request_and_params[REQUEST].upper(), request_and_params[SECOND]

    @staticmethod
    def send_response_to_client(response, client_socket):
        """
        Method that receives response and client socket and sends it
        :param response:
        :param client_socket: Hey ayelet
        """
        Protocol.send(client_socket, response)

    def handle_client_request(self, request, param, user):
        from methods import Methods
        """
        Method that takes request and calls on according method
        """
        try:
            return getattr(Methods, request)(param, user)
        except Exception as msg:
            print(f"Issue with processing request \n {msg}")

    def handle_clients(self):
        """
        Method that receives socket and handles clients input and desired output
        """
        done = False
        while not done:
            try:
                client_socket, address = self.server_socket.accept()
                clnt_thread = threading.Thread(target=self.handle_single_client,
                                               args=(client_socket, address))
                clnt_thread.start()
            except socket.error as socket_exception:
                raise RuntimeError("Socket error") from socket_exception
            except Exception as err:
                raise RuntimeError("General error") from err
        self.server_socket.close()

    def handle_single_client(self, client_socket, address):
        """
        Method that receives client socket and
        handles a single clients request and responses
        :param self:
        :param address:
        :param client_socket:
        """
        done = False
        request, user = self.receive_client_request(client_socket)
        self.check_for_directory(user)
        while not done:
            try:
                request, param = self.receive_client_request(client_socket)
                self.handle_client_request(request, param, user)
            except socket.error as socket_exception:
                raise RuntimeError("Socket error") from socket_exception
                done = True
            except Exception as err:
                raise RuntimeError("General error") from err
                done = True
        return False


def main():
    """Method that creates server object and runs it"""
    server = Server(SERVER_IP, PORT)
    server.handle_clients()


if __name__ == '__main__':
    main()
