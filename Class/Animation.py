import pygame
import time

CELL_SIZE = 92
BORDER_SIZE = 10
BOARD_SIZE = CELL_SIZE * 9
ANIMATION_PIXEL = 1
STEP = 32

class Animation:
    def __init__(self, screen, images):
        self.screen = screen
        self.images = images

    def slide_animation(self, slot_instance):
        for step in range(-9 * CELL_SIZE, 1, STEP):
            self.screen.fill((192, 192, 192))
            pygame.draw.rect(self.screen, (0, 0, 0), (BORDER_SIZE - ANIMATION_PIXEL, BORDER_SIZE - ANIMATION_PIXEL, BOARD_SIZE + 2, BOARD_SIZE + 2), 1)
            for i, row in enumerate(slot_instance.board):
                for j, value in enumerate(row):
                    y_position = BORDER_SIZE + i * CELL_SIZE + step
                    if y_position < BORDER_SIZE:
                        continue
                    self.screen.blit(self.images[value], (BORDER_SIZE + j * CELL_SIZE, y_position))
            pygame.display.flip()

    def fall_down_animation(self, slot_instance):
        fall_distances = self.calculate_fall_distances(slot_instance.board)
        max_distance = max(fall_distances.values(), default=0)
        if max_distance == 0:
            print("returning")
            return
        for step in range(1, max_distance * CELL_SIZE + 1, STEP):  # Gradual steps
            self.screen.fill((192, 192, 192))
            pygame.draw.rect(self.screen, (0, 0, 0), (BORDER_SIZE - ANIMATION_PIXEL, BORDER_SIZE - ANIMATION_PIXEL, BOARD_SIZE + 2, BOARD_SIZE + 2), 1)
            for i, row in enumerate(slot_instance.board):
                for j, value in enumerate(row):
                    if value is not None:
                        y_position = BORDER_SIZE + i * CELL_SIZE
                        fall_distance = fall_distances.get((i, j), 0)
                        if fall_distance > 0:
                            y_position += min(step, fall_distance * CELL_SIZE)
                        self.screen.blit(self.images[value], (BORDER_SIZE + j * CELL_SIZE, y_position))
            pygame.display.flip()

    def animate_new_symbols(self, slot_instance, old_board):
        for step in range(-9 * CELL_SIZE, 1, STEP):
            self.screen.fill((192, 192, 192))
            pygame.draw.rect(self.screen, (0, 0, 0), (BORDER_SIZE - ANIMATION_PIXEL, BORDER_SIZE - ANIMATION_PIXEL, BOARD_SIZE + 2, BOARD_SIZE + 2), 1)
            for i, row in enumerate(slot_instance.board):
                for j, value in enumerate(row):
                    if old_board[i][j] is None and value is not None:
                        y_position = BORDER_SIZE + i * CELL_SIZE + step
                        if y_position >= BORDER_SIZE:
                            self.screen.blit(self.images[value], (BORDER_SIZE + j * CELL_SIZE, y_position))
                    else:
                        if value is not None:
                            self.screen.blit(self.images[value], (BORDER_SIZE + j * CELL_SIZE, BORDER_SIZE + i * CELL_SIZE))
            pygame.display.flip()

    def calculate_fall_distances(self, board):
        distances = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] is not None:
                    distance = 0
                    for k in range(i + 1, len(board)):
                        if board[k][j] is None:
                            distance += 1
                    distances[(i, j)] = distance
        return distances

