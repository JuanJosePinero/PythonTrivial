import socket

server_ip = 'localhost'
server_port = 9006

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
print("Conectado al servidor")

client_socket.send("Conectado y listo.".encode())

for ronda in range(5):
    pregunta = client_socket.recv(1024).decode()
    print(f"Ronda {ronda + 1}: {pregunta}")

    opciones = []
    for _ in range(4):
        opcion = client_socket.recv(1024).decode()
        opciones.append(opcion)
        print(opcion)

    client_socket.send("Pregunta recibida. Listo para responder.".encode())
    client_socket.recv(1024).decode()

    respuesta = input("Ingrese la letra de la respuesta correcta: ").strip().lower()
    client_socket.send(respuesta.encode())

    resultado_ronda = client_socket.recv(1024).decode()
    print(resultado_ronda)

puntuacion_final = client_socket.recv(1024).decode()
print(puntuacion_final)

client_socket.close()
