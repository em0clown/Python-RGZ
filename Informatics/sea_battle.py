import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Морской бой")
root.geometry("900x700")

# Размеры доски
BOARD_SIZE = 10
CELL_SIZE = 30

# Цвета
COLOR_EMPTY = "light blue"
COLOR_GRID = "black"

# Создаем основную рамку
main_frame = tk.Frame(root, bg="lightgray")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Фрейм для доски игрока
player_frame = tk.Frame(main_frame, bg="lightgray")
player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

player_label = tk.Label(player_frame, text="Ваша доска", font=("Arial", 14, "bold"))
player_label.pack(pady=5)

# Холст для доски игрока
player_canvas = tk.Canvas(player_frame, width=BOARD_SIZE*CELL_SIZE+1, 
                         height=BOARD_SIZE*CELL_SIZE+1, 
                         bg=COLOR_EMPTY, highlightthickness=0)
player_canvas.pack()

# Фрейм для доски компьютера
computer_frame = tk.Frame(main_frame, bg="lightgray")
computer_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

computer_label = tk.Label(computer_frame, text="Доска компьютера", font=("Arial", 14, "bold"))
computer_label.pack(pady=5)

# Холст для доски компьютера
computer_canvas = tk.Canvas(computer_frame, width=BOARD_SIZE*CELL_SIZE+1, 
                           height=BOARD_SIZE*CELL_SIZE+1, 
                           bg=COLOR_EMPTY, highlightthickness=0)
computer_canvas.pack()

# Создаем пустые доски (списки списков)
player_board = []
computer_board = []

# Функция для создания пустой доски
def create_empty_board():
    board = []
    for _ in range(BOARD_SIZE):
        row = [0] * BOARD_SIZE  # 0 означает пустую клетку
        board.append(row)
    return board

# Функция для рисования сетки на доске
def draw_grid(canvas):
    canvas.delete("all")  # Очищаем холст
    
    # Рисуем вертикальные линии
    for i in range(BOARD_SIZE + 1):
        x = i * CELL_SIZE
        canvas.create_line(x, 0, x, BOARD_SIZE * CELL_SIZE, fill=COLOR_GRID, width=1)
    
    # Рисуем горизонтальные линии
    for i in range(BOARD_SIZE + 1):
        y = i * CELL_SIZE
        canvas.create_line(0, y, BOARD_SIZE * CELL_SIZE, y, fill=COLOR_GRID, width=1)
    
    # Рисуем номера строк и столбцов
    for i in range(BOARD_SIZE):
        # Номера строк слева
        canvas.create_text(5, i * CELL_SIZE + CELL_SIZE//2, 
                          text=str(i+1), font=("Arial", 7))
        # Буквы столбцов сверху
        canvas.create_text(i * CELL_SIZE + CELL_SIZE//2, 5,
                          text=chr(65 + i), font=("Arial", 7))

# Инициализируем доски
player_board = create_empty_board()
computer_board = create_empty_board()

# Рисуем сетки на обеих досках
draw_grid(player_canvas)
draw_grid(computer_canvas)

root.mainloop()