import sys
import pygame
import csv
import trivial


pygame.font.init()
pygame.font.init()

width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player")

def main_menu():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("None", 50)

    # Definición de los botones
    login_button = pygame.Rect(280, 200, 240, 50)  # x, y, width, height
    register_button = pygame.Rect(280, 300, 240, 50)

    while run:
        clock.tick(60)
        win.fill((214, 234, 248))

        # Título
        title_text = font.render("Welcome!!", True, (0, 0, 0))
        win.blit(title_text, (width / 2 - title_text.get_width() / 2, 100))

        # Texto de los botones
        login_text = font.render("Start", True, (255, 255, 255))
        register_text = font.render("New Player", True, (255, 255, 255))

        # Dibujar botones y centrar texto
        pygame.draw.rect(win, (0, 128, 0), login_button)  # Botón verde
        win.blit(login_text, (login_button.x + (login_button.width - login_text.get_width()) // 2,
                              login_button.y + (login_button.height - login_text.get_height()) // 2))

        pygame.draw.rect(win, (0, 128, 0), register_button)  # Botón verde
        win.blit(register_text, (register_button.x + (register_button.width - register_text.get_width()) // 2,
                                 register_button.y + (register_button.height - register_text.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    user_nick = login()
                    if user_nick:  # Inicio de sesión exitoso
                        jugar_trivial(user_nick)  # Inicia el juego con el nick del usuario
                        run = False
                    else:
                        print("Invalid Credentials!")
                elif register_button.collidepoint(event.pos):
                    registration()
                    run = False




def save_credentials(email, password, nick):
    with open("credentials.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, password, nick])

def check_credentials(email, password):
    with open("credentials.csv", "r", newline='') as file:
        reader = csv.reader(file)
        for stored_email, stored_password, stored_nick in reader:
            if email == stored_email and password == stored_password:
                print("Credentials Match!")
                return True, stored_nick  # Devuelve también el nick
    
    return False, None  # Devuelve False y None si no hay coincidencia



def login():
    run = True
    clock = pygame.time.Clock()
    email = ""
    password = ""
    username=""
    active_field = "email"
    cursor_visible = True
    last_cursor_toggle = pygame.time.get_ticks()
    cursor_interval = 500
    font1 = pygame.font.SysFont("None", 50)
    font2 = pygame.font.SysFont("None", 25)
    login_button = pygame.Rect(280, 400, 150, 40)
    next_button = pygame.Rect(280, 500, 150, 40)  # Position for the Next button
    message=""
    login_successful=False

    while run:
        clock.tick(60)
        win.fill((214, 234, 248))
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle > cursor_interval:
            cursor_visible = not cursor_visible
            last_cursor_toggle = current_time

        text = font1.render("Login", 1, (0, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, 100))

        # Email field
        email_prompt = font2.render("Enter Email:", 1, (0, 0, 0))
        win.blit(email_prompt, (50, 250))
        pygame.draw.rect(win, (255, 255, 255), (280, 250, 350, 30))  # Email input box
        pygame.draw.rect(win, (0, 0, 0), (280, 250, 350, 30), 2)
        email_text = font2.render(email, True, (0, 0, 0))
        win.blit(email_text, (285, 255))

        # Draw email cursor
        if active_field == "email" and cursor_visible:
            cursor_x = 285 + email_text.get_width()
            pygame.draw.line(win, (0, 0, 0), (cursor_x, 255), (cursor_x, 275))

        # Password field
        password_prompt = font2.render("Enter Password:", 1, (0, 0, 0))
        win.blit(password_prompt, (50, 300))
        pygame.draw.rect(win, (255, 255, 255), (280, 300, 350, 30))  # Password input box
        pygame.draw.rect(win, (0, 0, 0), (280, 300, 350, 30), 2)
        password_text = font2.render("*" * len(password), 1, (0, 0, 0))
        win.blit(password_text, (285, 305))

        # Draw password cursor
        if active_field == "password" and cursor_visible:
            cursor_x = 285 + password_text.get_width()
            pygame.draw.line(win, (0, 0, 0), (cursor_x, 305), (cursor_x, 325))

        message_text = font2.render(message, True, (255, 0, 0))  # Red color for message
        win.blit(message_text, (280, 340))  # Adjust position as needed

        # Draw Login button
        pygame.draw.rect(win, (0, 128, 0), login_button)  # Green button
        login_text = font2.render("Login", True, (255, 255, 255))  # White text
        win.blit(login_text, (login_button.x + (login_button.width - login_text.get_width()) // 2,
                              login_button.y + (login_button.height - login_text.get_height()) // 2))

        message_text = font2.render(message, True, (255, 0, 0))  # Red color for message
        win.blit(message_text, (280, 340))  # Adjust position as needed

        login_successful, user_nick = check_credentials(email, password)

        # Username field (displayed after successful login)
        if login_successful:
            print(f"Login successful! Nick: {user_nick}")
            trivial.jugar_trivial(user_nick)
            return user_nick


            # Draw username cursor
            if active_field == "username" and cursor_visible:
                cursor_x = 285 + username_text.get_width()
                pygame.draw.line(win, (0, 0, 0), (cursor_x, 455), (cursor_x, 475))


            trivial.jugar_trivial()
            
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == "email" and email:
                        email = email[:-1]
                    elif active_field == "password" and password:
                        password = password[:-1]
                elif event.key == pygame.K_TAB:
                    active_field = "password" if active_field == "email" else "email"
                else:
                    if active_field == "email" and len(email) < 50:
                        email += event.unicode
                    elif active_field == "password" and len(password) < 20:
                        password += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    login_successful, user_nick = check_credentials(email, password)
                    if login_successful:
                        print(f"Login successful! Nick: {user_nick}")
                        return user_nick  # Devuelve el nick en caso de éxito
                    else:
                        message = "Invalid Credentials!"
                        email = ""
                        password = ""


            if active_field == "username" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 20:
                    username += event.unicode



    return None  # Return empty string if login is unsuccessful


def registration():
    run = True
    clock = pygame.time.Clock()
    email = ""
    password = ""
    nick = ""  # Variable para el Nick
    active_field = "email"
    cursor_visible = True
    last_cursor_toggle = pygame.time.get_ticks()
    cursor_interval = 500
    font1 = pygame.font.SysFont("None", 50)
    font2 = pygame.font.SysFont("None", 25)

    register_button = pygame.Rect(280, 450, 150, 40)  # Posición ajustada

    while run:
        clock.tick(60)
        win.fill((214, 234, 248))

        # Handle cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle > cursor_interval:
            cursor_visible = not cursor_visible
            last_cursor_toggle = current_time

        text = font1.render("Player Registration", 1, (0, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, 100))

        # Email field
        email_prompt = font2.render("Enter Email:", 1, (0, 0, 0))
        win.blit(email_prompt, (50, 250))
        pygame.draw.rect(win, (255, 255, 255), (280, 250, 350, 30))  # Email input box
        pygame.draw.rect(win, (0, 0, 0), (280, 250, 350, 30), 2)
        email_text = font2.render(email, True, (0, 0, 0))
        win.blit(email_text, (285, 255))
        # Draw email cursor
        if active_field == "email" and cursor_visible:
            cursor_x = 285 + email_text.get_width()
            pygame.draw.line(win, (0, 0, 0), (cursor_x, 255), (cursor_x, 275))

        # Password field
        password_prompt = font2.render("Enter Password:", 1, (0, 0, 0))
        win.blit(password_prompt, (50, 300))
        pygame.draw.rect(win, (255, 255, 255), (280, 300, 350, 30))  # Password input box
        pygame.draw.rect(win, (0, 0, 0), (280, 300, 350, 30), 2)
        password_text = font2.render("*" * len(password), 1, (0, 0, 0))
        win.blit(password_text, (285, 305))
        # Draw password cursor
        if active_field == "password" and cursor_visible:
            cursor_x = 285 + password_text.get_width()
            pygame.draw.line(win, (0, 0, 0), (cursor_x, 305), (cursor_x, 325))
            
        nick_prompt = font2.render("Enter Nick:", 1, (0, 0, 0))
        win.blit(nick_prompt, (50, 350))
        pygame.draw.rect(win, (255, 255, 255), (280, 350, 350, 30))  # Cuadro de texto para Nick
        pygame.draw.rect(win, (0, 0, 0), (280, 350, 350, 30), 2)
        nick_text = font2.render(nick, True, (0, 0, 0))
        win.blit(nick_text, (285, 355))
        
        if active_field == "nick" and cursor_visible:
            cursor_x = 285 + nick_text.get_width()
            pygame.draw.line(win, (0, 0, 0), (cursor_x, 355), (cursor_x, 375))

        # Register button
        pygame.draw.rect(win, (0, 128, 0), register_button)  # Green button
        register_text = font2.render("Register", True, (255, 255, 255))  # White text
        win.blit(register_text, (register_button.x + 35, register_button.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == "email" and email:
                        email = email[:-1]
                    elif active_field == "password" and password:
                        password = password[:-1]
                    elif active_field == "nick" and nick:
                        nick = nick[:-1]
                elif event.key == pygame.K_TAB:
                    # Cambio de campo activo
                    if active_field == "email":
                        active_field = "password"
                    elif active_field == "password":
                        active_field = "nick"
                    elif active_field == "nick":
                        active_field = "email"
                else:
                    if active_field == "email" and len(email) < 50:
                        email += event.unicode
                    elif active_field == "password" and len(password) < 20:
                        password += event.unicode
                    elif active_field == "nick" and len(nick) < 20:
                        nick += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.collidepoint(event.pos):
                    save_credentials(email, password, nick)  # Guardar también el Nick
                    print("Credentials saved")
                    run = False
                    login()

        pygame.display.update()        



if __name__ == '__main__':
    main_menu()
