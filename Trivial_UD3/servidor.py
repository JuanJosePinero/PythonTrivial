import socket
import threading
import json
import random

# Configuración inicial del servidor
host = 'localhost'
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Base de datos de usuarios y preguntas
usuarios_registrados = {}  # Aquí se almacenarán los usuarios y contraseñas
preguntas = []  # Aquí se cargarán las preguntas desde un archivo

# Cargar preguntas desde un archivo
def cargar_preguntas():
    global preguntas


try:
    with open('preguntas.json', 'r') as archivo:
        preguntas = json.load(archivo)
except FileNotFoundError:
    print("Archivo de preguntas no encontrado.")
    exit()


# def registrar_usuario(conn, addr):
# while True:
# conn.send("Ingrese email: ".encode())
# email = conn.recv(1024).decode()
# if email in usuarios_registrados:
# conn.send("Email ya registrado. Intente de nuevo.".encode())
# else:
# break


# conn.send("Ingrese contraseña: ".encode())
# password = conn.recv(1024).decode()
# usuarios_registrados[email] = password
# conn.send(f"Usuario registrado con éxito. Su email es {email}".encode())


def autenticar_usuario(conn, addr):
conn.send("Ingrese email: ".encode())
email = conn.recv(1024).decode()
conn.send("Ingrese contraseña: ".encode())
password = conn.recv(1024).decode()
if email in usuarios_registrados and usuarios_registrados[email] == password:
    return True
else:
    return False


def manejar_cliente(conn, addr):
print(f"Nueva conexión de {addr}")
registrado = False

while not registrado:
    conn.send("1. Registrarse\n2. Iniciar sesión\nSeleccione una opción: ".encode())
    opcion = conn.recv(1024).decode()
    
    if opcion == '1':
        registrar_usuario(conn, addr)
    elif opcion == '2':
        registrado = autenticar_usuario(conn, addr)
        if registrado:
            conn.send("Autenticación exitosa.".encode())
        else:
            conn.send("Autenticación fallida.".encode())
    else:
        conn.send("Opción no válida.".encode())

# Aquí se manejaría la lógica del juego

conn.close()
