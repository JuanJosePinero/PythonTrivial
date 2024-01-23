import socket
import random
from preguntas import preguntas  # Importa la lista de preguntas desde preguntas.py
from usuarios import usuarios  # Importa la lista de usuarios desde usuarios.py
from threading import Thread

# Configuración del servidor
host = '10.10.1.13'  # Dirección IP del servidor
port = 12322  # Puerto de comunicación

# Lista de clientes conectados
clientes = []

# Función para manejar a un cliente
def manejar_cliente(client_socket):
    # Agregar el cliente a la lista
    clientes.append(client_socket)

    # Iniciar sesión de usuario
    usuario_valido = None
    while usuario_valido is None:
        # Solicitar nombre de usuario y contraseña
        client_socket.send("Ingresa tu nombre de usuario: ".encode())
        username = client_socket.recv(1024).decode()
        client_socket.send("Ingresa tu contraseña: ".encode())
        password = client_socket.recv(1024).decode()

        # Verificar si las credenciales son válidas
        for user in usuarios:
            if user["usuario"] == username and user["contrasenya"] == password:
                usuario_valido = user
                break

        if usuario_valido is None:
            client_socket.send("Nombre de usuario o contraseña incorrectos. Inténtalo de nuevo.".encode())

    client_socket.send(f"\n¡Bienvenido, {username}! Presiona Enter cuando el otro jugador esté listo.\n".encode())

    # Esperar a que ambos jugadores estén listos
    if len(clientes) == 2:
        for cliente in clientes:
            cliente.send("Ambos jugadores están listos. Presiona Enter para comenzar el juego.".encode())
        
        # Iniciar el juego
        jugar_trivial(clientes)

# Función para jugar el Trivial
def jugar_trivial(clientes):
    # Seleccionar 5 preguntas aleatorias de la lista de preguntas
    preguntas_aleatorias = random.sample(preguntas, 5)

    for cliente in clientes:
        cliente.send("\nComienza el juego.\n".encode())

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

        puntuaciones = [10 if respuesta == respuesta_correcta else 0 for respuesta in respuestas]

        for i, cliente in enumerate(clientes):
            cliente.send(f"Resultado de la ronda {ronda}: Puntos: {puntuaciones[i]}\n".encode())

    puntuaciones_finales = {cliente.getpeername(): sum(puntuaciones) for cliente, puntuacion in zip(clientes, puntuaciones)}

    for cliente in clientes:
        cliente.send("Fin del juego.\n".encode())
        cliente.send(f"Tus puntuaciones finales son: {puntuaciones_finales[cliente.getpeername()]} puntos.\n".encode())

    # Cerrar la conexión con los clientes
    for cliente in clientes:
        cliente.close()

# Configurar el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)  # Permitir 2 conexiones (para 2 jugadores)

print(f"Servidor en ejecución en {host}:{port}")

# Esperar a que los jugadores se conecten
while len(clientes) < 2:
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida desde {addr}")

    # Iniciar un hilo para manejar al cliente
    Thread(target=manejar_cliente, args=(client_socket,)).start()