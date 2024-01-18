import random
from preguntas import preguntas  # Importa la lista de preguntas desde preguntas.py
from usuarios import usuarios  # Importa la lista de usuarios desde usuarios.py

# Función para realizar el juego
def jugar_trivial():
    # Inicializar puntuaciones de los jugadores
    puntuaciones = {}

    # Solicitar a los jugadores que inicien el juego
    for jugador in range(2):
        usuario_valido = False
        while not usuario_valido:
            username = input(f"Ingrese el nombre de usuario del Jugador {jugador + 1}: ")
            password = input("Ingrese la contraseña: ")
            
            # Verificar si las credenciales son válidas
            for user in usuarios:
                if user["usuario"] == username and user["contrasenya"] == password:
                    usuario_valido = True
                    break
            
            if not usuario_valido:
                print("Nombre de usuario o contraseña incorrectos. Inténtalo de nuevo.")

        print(f"\n¡Bienvenido, {username}! Presiona Enter para comenzar el juego.\n")
        input("Presiona Enter para continuar...")

        # Seleccionar 5 preguntas aleatorias de la lista de preguntas importada
        preguntas_aleatorias = random.sample(preguntas, 5)

        print(f"\nComienza el juego para {username}.\n")

        # Inicializar puntuación del jugador
        puntuaciones[username] = 0

        for idx, pregunta in enumerate(preguntas_aleatorias, start=1):
            print(f"Pregunta {idx}: {pregunta['pregunta']}")
            for opcion in pregunta['opciones']:
                print(opcion)
            
            respuesta = input("Ingrese la letra de la respuesta correcta: ").lower()

            if respuesta == pregunta['respuesta_correcta']:
                print("¡Respuesta correcta! Ganaste 10 puntos.\n")
                puntuaciones[username] += 10
            else:
                print("Respuesta incorrecta. No ganaste puntos.\n")

        print(f"Fin del juego para {username}. Tu puntuación es: {puntuaciones[username]} puntos.\n")

    # Determinar al ganador
    ganador = max(puntuaciones, key=puntuaciones.get)
    print(f"¡El ganador es {ganador} con {puntuaciones[ganador]} puntos!")

if __name__ == "__main__":
    jugar_trivial()
