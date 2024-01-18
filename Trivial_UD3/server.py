import socket
import random

# Configuración del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('tu_direccion_IP', 12345))
server.listen(4)

# Lista para almacenar las conexiones de los clientes
clientes = []

# Función para manejar a un cliente
def manejar_cliente(cliente):
    # Implementa la lógica de inicio de sesión y registro aquí
    # ...

    # Esperar a que se unan 4 jugadores
    while len(clientes) < 4:
        cliente.send("Esperando a que se unan otros jugadores...\n".encode())
    
    # Selecciona 5 preguntas aleatorias del conjunto de preguntas
    preguntas = random.sample(lista_de_preguntas, 5)

    # Implementa la lógica del juego aquí
    # ...

# Aceptar conexiones de clientes
while True:
    cliente, direccion = server.accept()
    clientes.append(cliente)
    cliente.send("¡Te has conectado al servidor!\n".encode())
    manejar_cliente(cliente)
