import socket
from threading import Thread
from preguntas import preguntas  # Asegúrate de que este archivo exista
from usuarios import usuarios  # Asegúrate de que este archivo exista
import random

# Configuración del servidor
host = 'localhost'
port = 9006
clientes = []

def manejar_cliente(client_socket):
    print("Manejando nuevo cliente")
    clientes.append(client_socket)

    usuario_valido = None
    while usuario_valido is None:
        client_socket.send("Ingresa tu nombre de usuario: ".encode())
        username = client_socket.recv(1024).decode()
        print(f"Nombre de usuario recibido: {username}")
        
        client_socket.send("Ingresa tu contraseña: ".encode())
        password = client_socket.recv(1024).decode()
        print(f"Contraseña recibida: [oculta por seguridad]")

        for user in usuarios:
            if user["usuario"] == username and user["contrasenya"] == password:
                usuario_valido = user
                break

        if usuario_valido is None:
            client_socket.send("Nombre de usuario o contraseña incorrectos. Inténtalo de nuevo.".encode())

    client_socket.send(f"\n¡Bienvenido, {username}! Presiona Enter cuando el otro jugador esté listo.\n".encode())

    if len(clientes) == 2:
        print("Iniciando el juego con 2 jugadores")
        jugar_trivial(clientes)

def jugar_trivial(clientes):
    preguntas_aleatorias = random.sample(preguntas, 5)

    for cliente in clientes:
        cliente.send("\nComienza el juego.\n".encode())

    puntuaciones = [0, 0]
    for ronda, pregunta in enumerate(preguntas_aleatorias, start=1):
        pregunta_texto = pregunta['pregunta']
        opciones = pregunta['opciones']
        respuesta_correcta = pregunta['respuesta_correcta']

        for cliente in clientes:
            cliente.send(f"Pregunta {ronda}: {pregunta_texto}\n".encode())
            for opcion in opciones:
                cliente.send(opcion.encode())
                cliente.send('\n'.encode())

        respuestas = [cliente.recv(1024).decode().strip().lower() for cliente in clientes]

        for i, respuesta in enumerate(respuestas):
            if respuesta == respuesta_correcta:
                puntuaciones[i] += 10
                clientes[i].send(f"Correcto! Puntos: {puntuaciones[i]}\n".encode())
            else:
                clientes[i].send(f"Incorrecto. Puntos: {puntuaciones[i]}\n".encode())

    for i, cliente in enumerate(clientes):
        cliente.send("Fin del juego.\n".encode())
        cliente.send(f"Tus puntuaciones finales son: {puntuaciones[i]} puntos.\n".encode())
        cliente.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)
print(f"Servidor en ejecución en {host}:{port}")

while len(clientes) < 2:
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida desde {addr}")
    Thread(target=manejar_cliente, args=(client_socket,)).start()
