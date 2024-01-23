import sys
import pygame
import csv
import trivial


pygame.font.init()

width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player")



def save_credentials(email, password):
    with open("credentials.csv", "a", newline='') as file:
        writer=csv.writer(file)
        writer.writerow([email, password])

def check_credentials(email, password):
    with open("credentials.csv", "r", newline='') as file:
        reader = csv.reader(file)
        for stored_email, stored_password in reader:
            if email == stored_email and password == stored_password:
                print("Credentials Match!")
                return True
    print("Unmatched Credentials!")
    return False

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



        # Username field (displayed after successful login)
        if login_successful:
            username_prompt = font2.render("Enter Username:", 1, (0, 0, 0))
            win.blit(username_prompt, (50, 450))
            pygame.draw.rect(win, (255, 255, 255), (280, 450, 350, 30))  # Username input box
            pygame.draw.rect(win, (0, 0, 0), (280, 450, 350, 30), 2)
            username_text = font2.render(username, True, (0, 0, 0))
            win.blit(username_text, (285, 455))

            # Draw Next button
            pygame.draw.rect(win, (0, 128, 0), next_button)  # Green button
            next_text = font2.render("Next", True, (255, 255, 255))  # White text
            win.blit(next_text, (next_button.x + (next_button.width - next_text.get_width()) // 2,
                                 next_button.y + (next_button.height - next_text.get_height()) // 2))


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
                    if not login_successful and check_credentials(email, password):
                        message = "Login successful!"
                        login_successful = True
                        active_field = "username"
                        trivial.jugar_trivial()
                        run = False
                    else:
                        message = "Invalid Credentials!"
                        email = ""
                        password = ""
                elif next_button.collidepoint(event.pos) and login_successful:
                    print(f"Username {username} saved for client window.")
                    return username  # Or handle the username as needed


            if active_field == "username" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 20:
                    username += event.unicode



    return ""  # Return empty string if login is unsuccessful


def registration():
    run = True
    clock = pygame.time.Clock()
    email = ""
    password = ""
    active_field = "email"  # Tracks which field is active, starts with email
    cursor_visible = True  # Cursor visibility flag
    last_cursor_toggle = pygame.time.get_ticks()
    cursor_interval = 500  # Cursor blink interval in milliseconds

    # Define the register button dimensions and position
    register_button = pygame.Rect(280, 400, 150, 40)  # x, y, width, height

    font1 = pygame.font.SysFont("None", 50)
    font2 = pygame.font.SysFont("None", 25)

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
                elif event.key == pygame.K_TAB:
                    # Switch active field between email and password
                    active_field = "password" if active_field == "email" else "email"
                else:
                    if active_field == "email" and len(email) < 50:
                        email += event.unicode
                    elif active_field == "password" and len(password) < 20:
                        password += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.collidepoint(event.pos):
                    save_credentials(email, password)  # Save credentials
                    print("Credentials saved")
                    run=False
                    login()
                    pygame.display.update()



if __name__ == '__main__':
    registration()
