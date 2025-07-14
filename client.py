import tkinter as tk


import socket

 # Helper function to send requests to the server
def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5000))
    client_socket.send(request.encode())
    response = client_socket.recv(4096).decode()
    client_socket.close()
    return response


 