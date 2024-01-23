import pygame
import random
import csv
from preguntas import preguntas  # Asegúrate de que este archivo esté correctamente importado

# Configuraciones iniciales de Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Juego Trivial')

# Colores y fuente
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 36)

# Funciones auxiliares
def draw_text(text, font, color, surface, x, y):
    max_length = 55  # Máximo número de caracteres en una línea
    if len(text) > max_length:
        # Divide el texto en dos líneas
        split_point = text.rfind(' ', 0, max_length)  # Encuentra un espacio para dividir
        if split_point == -1:  # Si no hay espacio, divide en el máximo
            split_point = max_length

        text1 = text[:split_point]
        text2 = text[split_point:].strip()

        # Renderiza y dibuja la primera línea
        textobj1 = font.render(text1, True, color)
        textrect1 = textobj1.get_rect()
        textrect1.topleft = (x, y)
        surface.blit(textobj1, textrect1)

        # Renderiza y dibuja la segunda línea
        textobj2 = font.render(text2, True, color)
        textrect2 = textobj2.get_rect()
        textrect2.topleft = (x, y + textrect1.height)  # Coloca debajo de la primera línea
        surface.blit(textobj2, textrect2)
    else:
        # Si el texto es corto, lo maneja como antes
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, BLACK, surface, x + 10, y + 10)

def is_over_button(pos, x, y, width, height):
    return x < pos[0] < x + width and y < pos[1] < y + height

# Función principal del juego
def jugar_trivial(user_nick):
    running = True
    clock = pygame.time.Clock()
    estado_juego = 'juego'
    pregunta_actual = 0
    preguntas_aleatorias = random.sample(preguntas, 5)
    puntuacion = 0
    
    mensaje_respuesta = ''
    mostrar_mensaje = False
    tiempo_mensaje = 0

    while running:
        screen.fill(WHITE)
        draw_text(f"{user_nick}", font, RED, screen, screen_width - 200, 10)
        mouse_pos = pygame.mouse.get_pos()
        tiempo_actual = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if estado_juego == 'juego' and event.type == pygame.MOUSEBUTTONDOWN:
                pregunta = preguntas_aleatorias[pregunta_actual]
                for i, opcion in enumerate(pregunta['opciones']):
                    if is_over_button(mouse_pos, 50, 150 + i * 60, 700, 50):
                        if chr(97 + i) == pregunta['respuesta_correcta']:
                            puntuacion += 10
                            mensaje_respuesta = "¡Respuesta Correcta!"
                        else:
                            mensaje_respuesta = "Incorrecto. La respuesta correcta era: " + pregunta['opciones'][ord(pregunta['respuesta_correcta']) - 97]
                        mostrar_mensaje = True
                        pygame.time.delay(1000)
                        pregunta_actual += 1
                        if pregunta_actual >= len(preguntas_aleatorias):
                            estado_juego = 'resultado'
                        break
                    
                if mostrar_mensaje:
                    tiempo_mensaje = tiempo_actual
                    
        if mostrar_mensaje and tiempo_actual - tiempo_mensaje < 2000:
            draw_text(mensaje_respuesta, font, RED, screen, 50, 120)
        else:
            mostrar_mensaje = False

        if estado_juego == 'juego':
            if pregunta_actual < len(preguntas_aleatorias):
                pregunta = preguntas_aleatorias[pregunta_actual]
                draw_text(f"Pregunta {pregunta_actual + 1}: {pregunta['pregunta']}", font, BLACK, screen, 50, 50)
                for i, opcion in enumerate(pregunta['opciones']):
                    draw_button(opcion, font, BLUE, screen, 50, 150 + i * 60, 700, 50)
            else:
                estado_juego = 'resultado'

        elif estado_juego == 'resultado':
            draw_text(f"Puntuación final: {puntuacion}", font, GREEN, screen, 50, 50)
            pygame.display.flip()
            pygame.time.delay(4000)  # Espera 2 segundos antes de cambiar al estado de mostrar puntuaciones
            estado_juego = 'mostrar_puntuaciones'

        elif estado_juego == 'mostrar_puntuaciones':
            # Guardar la puntuación en el archivo CSV
            with open('puntuaciones.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_nick, puntuacion])

            # Leer y mostrar las puntuaciones
            puntuaciones = []
            with open('puntuaciones.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    puntuaciones.append(row)

            # Mostrar las puntuaciones en la pantalla
            screen.fill(WHITE)  # Limpia la pantalla antes de mostrar las puntuaciones
            y_pos = 50
            for nick, score in puntuaciones:
                draw_text(f"{nick}: {score}", font, BLUE, screen, 50, y_pos)
                y_pos += 30

            pygame.display.flip()
            pygame.time.delay(5000)  # Espera 5 segundos antes de cerrar
            running = False  # Finaliza el juego después de mostrar las puntuaciones

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    # Guardar la puntuación en el archivo CSV
    with open('puntuaciones.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_nick, puntuacion])

    # Leer y mostrar las puntuaciones
    puntuaciones = []
    with open('puntuaciones.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            puntuaciones.append(row)

    # Mostrar las puntuaciones en la pantalla
    screen.fill(WHITE)  # Limpia la pantalla antes de mostrar las puntuaciones
    y_pos = 100
    for nick, score in puntuaciones:
        draw_text(f"{nick}: {score}", font, BLUE, screen, 50, y_pos)
        y_pos += 30

    pygame.display.flip()
    pygame.time.delay(10000)  # Espera 5 segundos antes de cerrar

    pygame.quit()


if __name__ == "__main__":
    user_nick = "UsuarioEjemplo"  # Sustituye esto con la variable real que contiene el nick del usuario
    jugar_trivial(user_nick)
