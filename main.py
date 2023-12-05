import pygame
from Class.Animation import Animation
from Class.Slot import Slot
import time

CELL_SIZE = 92
BORDER_SIZE = 10
BOARD_SIZE = CELL_SIZE * 9
ANIMATION_PIXEL = 1

def load_images():
    images = {}
    for i in range(10):
        image = pygame.image.load(f'Assets/{i}.png')
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
        images[i] = image
    return images

def highlight_clusters(screen, clusters, images, board, color):
    for cluster in clusters:
        for x, y in cluster:
            if board[x][y] is not None:
                pygame.draw.rect(screen, color, (BORDER_SIZE + y * CELL_SIZE, BORDER_SIZE + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                screen.blit(images[board[x][y]], (BORDER_SIZE + y * CELL_SIZE, BORDER_SIZE + x * CELL_SIZE))

def redraw_board(screen, images, board):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value is not None:
                screen.blit(images[value], (BORDER_SIZE + j * CELL_SIZE, BORDER_SIZE + i * CELL_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (BORDER_SIZE + j * CELL_SIZE, BORDER_SIZE + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def create_button(screen, text, position):
    font = pygame.font.Font(None, 36)
    button_text = font.render(text, True, (0, 0, 0))
    button_rect = button_text.get_rect(center=position)
    pygame.draw.rect(screen, (192, 192, 192), button_rect, 0)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
    screen.blit(button_text, button_rect.topleft)

def initialize_pygame():
    pygame.init()
    screen_size = BOARD_SIZE + 2 * BORDER_SIZE
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Slot Board Visualizer")
    return screen

def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_screen(screen, images, slot_instance):
    screen.fill((192, 192, 192))
    pygame.draw.rect(screen, (0, 0, 0), (BORDER_SIZE - ANIMATION_PIXEL, BORDER_SIZE - ANIMATION_PIXEL, BOARD_SIZE + 2, BOARD_SIZE + 2), 1)
    redraw_board(screen, images, slot_instance.board)
    pygame.display.flip()

def perform_highlight_animation(screen, clusters, images, slot_instance, animation):
    for _ in range(2):
        highlight_clusters(screen, clusters, images, slot_instance.board, (255, 0, 0))
        pygame.display.flip()
        time.sleep(0.2)
        screen.fill((192, 192, 192))
        pygame.draw.rect(screen, (0, 0, 0), (BORDER_SIZE - ANIMATION_PIXEL, BORDER_SIZE - ANIMATION_PIXEL, BOARD_SIZE + 2, BOARD_SIZE + 2), 1)
        redraw_board(screen, images, slot_instance.board)
        pygame.display.flip()
        time.sleep(0.2)
    slot_instance.removeClusters()
    animation.fall_down_animation(slot_instance)
    slot_instance.boardDown()

def run_game_loop(screen, images):
    slot_instance = Slot("Nom", "Type", "Valeur")
    animation = Animation(screen, images)
    animation.slide_animation(slot_instance)
    button_text = "New Board"
    button_position = (BOARD_SIZE + BORDER_SIZE * 2, BOARD_SIZE + BORDER_SIZE)
    running = True
    while running:
        running = process_events()
        clusters = slot_instance.checkWin()
        if clusters:
            update_screen(screen, images, slot_instance)
            perform_highlight_animation(screen, clusters, images, slot_instance, animation)
            old_board = [row[:] for row in slot_instance.board]  # Copy of the current board
            slot_instance.refillBoard()
            animation.animate_new_symbols(slot_instance, old_board)  # Animate only new symbols

        create_button(screen, button_text, button_position)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_position[0] - 100, button_position[1] - 40, 200, 80)
        if button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            slot_instance = Slot("Nom", "Type", "Valeur")
            animation.slide_animation(slot_instance)
        update_screen(screen, images, slot_instance)

def main():
    screen = initialize_pygame()
    images = load_images()
    run_game_loop(screen, images)
    pygame.quit()

if __name__ == "__main__":
    main()
