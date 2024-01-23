import socket
import authentication  # Importa el módulo de autenticación

server_ip = '10.10.1.109'
server_port = 12322

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
print("Conectado al servidor")

client_socket.send("Conectado y listo.".encode())

authentication.registration()  # Inicia el proceso de autenticación

client_socket.close()