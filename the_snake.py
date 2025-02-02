
import random

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.
    Определяет цвет и позицию объекта, а также метод его отрисовки.
    """

    def __init__(self, body_color=(0, 0, 0)):
        self.body_color = body_color
        self.position = (0, 0)

    def draw(self):
        """Заготовка объекта для отрисовки на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс, представляющий яблоко на игровом поле.
    Яблоко появляется в случайной позиции и может быть съедено змейкой.
    """

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.respawn()
        # Метод draw класса Apple
        super().draw()

    def respawn(self):
        """Перемещает яблоко в случайную позицию на поле."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """
    Класс, представляющий змейку.
    Змейка двигается по полю, увеличивается при поедании яблок и
    может столкнуться с самой собой.
    """

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.length = 2

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        # Начальная позиция
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Начальное направление
        self.direction = RIGHT
        # Следующее направление
        self.next_direction = None
        # Последний сегмент змейки
        self.last = None
        # Возвращаем длину змейки
        self.length = 2

    # Метод draw класса Snake
    def draw(self):
        """Отрисовка объекта змейка на экране."""
        for segment in self.positions[:-1]:
            self.position = segment
            super().draw()

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.positions.insert(0, (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        ))
        if len(self.positions) > self.length:
            self.positions.pop()

    def check_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        return self.positions[0] in self.positions[1:]


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция игры.
    Инициализирует игру и запускает основной игровой цикл.
    """

    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов
    snake = Snake()
    apple = Apple()
    # Основной цикл
    while True:
        clock.tick(SPEED)

        # Обработка ввода пользователя
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.positions[0] == apple.position:
            apple.respawn()
            # Увеличиваем длину змейки
            snake.length += 1

        # Проверка столкновения с собой
        if snake.check_collision():
            snake.reset()
            apple.respawn()

        # Отрисовка объектов.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
