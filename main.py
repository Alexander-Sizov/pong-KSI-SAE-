from tkinter import *
# импортируем библиотеку random
import random

# Добавляем глобальные переменные

# глобальные переменные
# настройки окна
WIDTH = 900
HEIGHT = 300

# настройки ракеток

# ширина ракетки
Racket_Width = 10
# высота ракетки
Racket_Height = 100

# настройки мяча
# Насколько будет увеличиваться скорость мяча с каждым ударом
BALL_SPEED_UP = 1.05
# Максимальная скорость мяча
BALL_MAX_SPEED = 40
# радиус мяча
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

# Счет игроков
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# Добавим глобальную переменную отвечающую за расстояние
# до правого края игрового поля
right_line_distance = WIDTH - Racket_Width


def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)


def spawn_ball():
    global BALL_X_SPEED
    # Выставляем мяч по центру
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2)
    # Задаем мячу направление в сторону проигравшего игрока,
    # но снижаем скорость до изначальной
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)


# функция отскока мяча
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    # ударили ракеткой
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED


# устанавливаем окно
root = Tk()
root.title("PythonicWay Pong")

# область анимации
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()

# элементы игрового поля

# левая линия
c.create_line(Racket_Width, 0, Racket_Width, HEIGHT, fill="white")
# правая линия
c.create_line(WIDTH - Racket_Width, 0, WIDTH - Racket_Width, HEIGHT, fill="white")
# центральная линия
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

# установка игровых объектов

# создаем мяч
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2, fill="white")

# левая ракетка
LEFT_Racket = c.create_line(Racket_Width / 2, 0, Racket_Width / 2, Racket_Height, width=Racket_Width, fill="yellow")

# правая ракетка
RIGHT_Racket = c.create_line(WIDTH - Racket_Width / 2, 0, WIDTH - Racket_Width / 2,
                          Racket_Height, width=Racket_Width, fill="yellow")

p_1_text = c.create_text(WIDTH - WIDTH / 6, Racket_Height / 4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white")

p_2_text = c.create_text(WIDTH / 6, Racket_Height / 4,
                         text=PLAYER_2_SCORE,
                         font="Arial 20",
                         fill="white")

# добавим глобальные переменные для скорости движения мяча
# по горизонтали
BALL_X_CHANGE = 20
# по вертикали
BALL_Y_CHANGE = 0


def move_ball():
    # определяем координаты сторон мяча и его центра
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    # вертикальный отскок
    # Если мы далеко от вертикальных линий - просто двигаем мяч
    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > Racket_Width:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    # Если мяч касается своей правой или левой стороной границы поля
    elif ball_right == right_line_distance or ball_left == Racket_Width:
        # Проверяем правой или левой стороны мы касаемся
        if ball_right > WIDTH / 2:
            # Если правой, то сравниваем позицию центра мяча
            # с позицией правой ракетки.
            # И если мяч в пределах ракетки делаем отскок
            if c.coords(RIGHT_Racket)[1] < ball_center < c.coords(RIGHT_Racket)[3]:
                bounce("strike")
            else:
                # Иначе игрок пропустил - тут оставим пока pass, его мы заменим на подсчет очков и респаун мячика
                update_score("left")
                spawn_ball()
        else:
            # То же самое для левого игрока
            if c.coords(LEFT_Racket)[1] < ball_center < c.coords(LEFT_Racket)[3]:
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    # Проверка ситуации, в которой мячик может вылететь за границы игрового поля.
    # В таком случае просто двигаем его к границе поля.
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + Racket_Width, BALL_Y_SPEED)
    # горизонтальный отскок
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")


# зададим глобальные переменные скорости движения ракеток
# скорось с которой будут ездить ракетки
Racket_SPEED = 20
# скорость левой платформы
LEFT_Racket_SPEED = 0
# скорость правой ракетки
RIGHT_Racket_SPEED = 0


# функция движения обеих ракеток
def move_Rackets():
    # для удобства создадим словарь, где ракетке соответствует ее скорость
    RacketS = {LEFT_Racket: LEFT_Racket_SPEED,
            RIGHT_Racket: RIGHT_Racket_SPEED}
    # перебираем ракетки
    for Racket in RacketS:
        # двигаем ракетку с заданной скоростью
        c.move(Racket, 0, RacketS[Racket])
        # если ракетка вылезает за игровое поле возвращаем ее на место
        if c.coords(Racket)[1] < 0:
            c.move(Racket, 0, -c.coords(Racket)[1])
        elif c.coords(Racket)[3] > HEIGHT:
            c.move(Racket, 0, HEIGHT - c.coords(Racket)[3])


def main():
    move_ball()
    move_Rackets()
    # вызываем саму себя каждые 10 миллисекунд
    root.after(10, main)


# Установим фокус на Canvas чтобы он реагировал на нажатия клавиш
c.focus_set()


# Напишем функцию обработки нажатия клавиш
def movement_handler(event):
    global LEFT_Racket_SPEED, RIGHT_Racket_SPEED
    if event.keysym == "w":
        LEFT_Racket_SPEED = -Racket_SPEED
    elif event.keysym == "s":
        LEFT_Racket_SPEED = Racket_SPEED
    elif event.keysym == "Up":
        RIGHT_Racket_SPEED = -Racket_SPEED
    elif event.keysym == "Down":
        RIGHT_Racket_SPEED = Racket_SPEED


# Привяжем к Canvas эту функцию
c.bind("<KeyPress>", movement_handler)


# Создадим функцию реагирования на отпускание клавиши
def stop_racket(event):
    global LEFT_Racket_SPEED, RIGHT_Racket_SPEED
    if event.keysym in "ws":
        LEFT_Racket_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_Racket_SPEED = 0


# Привяжем к Canvas эту функцию
c.bind("<KeyRelease>", stop_racket)

# запускаем движение
main()

# запускаем работу окна
root.mainloop()

