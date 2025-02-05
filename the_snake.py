import random

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константа центра экрана
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цветовые константы:
BOARD_BACKGROUND_COLOR = (165, 165, 165)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Рекорд длины змейки
high_score = 0

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.
    Определяет цвет и позицию объекта, а также метод его отрисовки.
    """

    position = (0, 0)
    body_color = (0, 0, 0)

    def draw(self, position, color=None):
        """Отрисовывает одну ячейку на поле."""
        color = color if color else self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс, представляющий яблоко на игровом поле.
    Яблоко появляется в случайной позиции и может быть съедено змейкой.
    """

    def __init__(self, occupied_positions, color=APPLE_COLOR):
        self.randomize_position(occupied_positions)
        self.body_color = color

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в случайную позицию на поле."""
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break


class Snake(GameObject):
    """
    Класс, представляющий змейку.
    Змейка двигается по полю, увеличивается при поедании яблок и
    может столкнуться с самой собой.
    """

    def __init__(self, color=SNAKE_COLOR):
        self.reset()
        self.body_color = color
        self.next_direction = self.direction

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        # Начальная позиция
        self.positions = [SCREEN_CENTER]
        # Начальное направление
        self.direction = RIGHT
        # Последний сегмент змейки
        self.last = None
        # Возвращаем длину змейки
        self.length = 1

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            GameObject.draw(self, position, self.body_color)

    def update_direction(self, new_direction=None):
        """Обновляет направление змейки."""
        if new_direction:
            # Проверяем, чтобы змейка не могла развернуться назад
            if new_direction[0] != -self.direction[0]:
                self.next_direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        # Без строчки с self.next.directon при быстром нажатии вверх
        # или вниз и в противоположную сторону змейка может развернуться
        self.direction = self.next_direction
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
        if self.length < 4:  # Минимальная длина для столкновения с собой
            return False
        return self.get_head_position() in self.positions[1:]

    # Функция обработки действий пользователя
    def handle_keys(self):
        """Обрабатывает нажатия клавиш."""
        global SPEED
        key_mapping = {
            pg.K_UP: UP,
            pg.K_DOWN: DOWN,
            pg.K_LEFT: LEFT,
            pg.K_RIGHT: RIGHT
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.KEYDOWN:
                if event.key in key_mapping:
                    new_direction = key_mapping[event.key]
                    self.update_direction(new_direction)
                elif event.key == pg.K_PAGEUP:  # Увеличиваем скорость
                    SPEED += 1
                elif event.key == pg.K_PAGEDOWN:  # Уменьшаем скорость
                    SPEED = max(1, SPEED - 1)  # Минимальная скорость 1
                elif event.key == pg.K_ESCAPE:  # Выход из игры
                    pg.quit()
                    raise SystemExit


def main():
    """
    Основная функция игры.
    Инициализирует игру и запускает основной игровой цикл.
    """
    global SPEED, high_score
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов
    snake = Snake()
    apple = Apple(set(snake.positions))
    # Основной цикл
    while True:
        clock.tick(SPEED)

        # Обработка ввода пользователя
        snake.handle_keys()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.positions[0] == apple.position:
            # Увеличивает длину змейки
            snake.length += 1
            # Перемещаем яблоко с учетом занятых позиций
            apple.randomize_position(set(snake.positions))

        # Проверка столкновения с собой
        if snake.check_collision():
            # Обновляем рекорд, если текущая длина больше
            if snake.length > high_score:
                high_score = snake.length
            snake.reset()
            apple.randomize_position(set(snake.positions))

        # Обновляем заголовок с рекордом и текущей скоростью
        pg.display.set_caption(f'Змейка'
                               f' | Рекорд: {high_score} |'
                               f' Скорость: {SPEED}'
                               f' (Pg.Up +, Pg.Dn -)'
                               f' | ESC - выйти')

        # Отрисовка объектов.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(apple.position)
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
