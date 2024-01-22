import socket
import random
from preguntas import preguntas  # Importa la lista de preguntas desde preguntas.py
from usuarios import usuarios  # Importa la lista de usuarios desde usuarios.py
from threading import Thread

# Configuración del servidor
host = '10.10.1.13'  # Dirección IP del servidor
port = 12345  # Puerto de comunicación

# Función para manejar a un jugador
# Función para manejar a un jugador
def manejar_jugador(client_socket, jugador):
    # Inicializar puntuación del jugador
    puntuacion = 0

    # Enviar mensaje de bienvenida al jugador
    client_socket.send("¡Bienvenido al Trivial! Espera a tu oponente para empezar.".encode())

    # Comenzar el juego
    for ronda in range(5):  # 5 rondas de preguntas
        pregunta_aleatoria = random.choice(preguntas)
        preguntas.remove(pregunta_aleatoria)

        # Enviar pregunta al jugador
        pregunta_texto = pregunta_aleatoria['pregunta']
        opciones = pregunta_aleatoria['opciones']
        respuesta_correcta = pregunta_aleatoria['respuesta_correcta']

        client_socket.send(f"Ronda {ronda + 1}: {pregunta_texto}\n".encode())
        for opcion in opciones:
            client_socket.send(opcion.encode())
            client_socket.send('\n'.encode())

        # Recibir respuesta del jugador
        respuesta = client_socket.recv(1024).decode().strip().lower()

        # Verificar la respuesta
        if respuesta == respuesta_correcta:
            puntuacion += 10

        # Enviar resultado de la ronda al jugador
        client_socket.send(f"Resultado de la ronda {ronda + 1}: Puntos: {puntuacion}\n".encode())

    # Enviar puntuación final al jugador
    client_socket.send(f"Fin del juego. Tu puntuación final es: {puntuacion} puntos.\n".encode())

    # Cerrar la conexión con el jugador
    client_socket.close()

    # Enviar puntuación final al jugador
    client_socket.send(f"Fin del juego. Tu puntuación final es: {puntuacion} puntos.\n".encode())

    # Cerrar la conexión con el jugador
    client_socket.close()

# Configurar el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)  # Permitir 2 conexiones (para 2 jugadores)

print(f"Servidor en ejecución en {host}:{port}")

# Esperar a que los jugadores se conecten
jugador = 1
while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida desde {addr}")
    
    # Iniciar un hilo para manejar al jugador
    Thread(target=manejar_jugador, args=(client_socket, jugador)).start()

    jugador += 1
