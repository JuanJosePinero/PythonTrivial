import socket

# Configura el socket del cliente
server_ip = '10.10.1.13'
server_port = 12321  # El mismo puerto que configuraste en el servidor

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Bucle para 5 rondas de preguntas
for ronda in range(5):
    # Recibe la pregunta y opciones del servidor
    pregunta = client_socket.recv(1024).decode()
    print(f"Ronda {ronda + 1}: {pregunta}")

    opciones = []
    for _ in range(4):
        opcion = client_socket.recv(1024).decode()
        opciones.append(opcion)
        print(opcion)

    # Envía la respuesta al servidor
    respuesta = input("Ingrese la letra de la respuesta correcta: ").strip().lower()
    client_socket.send(respuesta.encode())

    # Recibe y muestra el resultado de la ronda
    resultado_ronda = client_socket.recv(1024).decode()
    print(resultado_ronda)

# Recibe y muestra la puntuación final del cliente
puntuacion_final = client_socket.recv(1024).decode()
print(puntuacion_final)

# Cierra la conexión con el servidor
client_socket.close()
