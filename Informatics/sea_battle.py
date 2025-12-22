import tkinter as tk
from tkinter import messagebox
import random

# --- Настройки ---
BOARD = 10
CELL = 30

SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
SHIP_NAMES = [
    "Линкор (4)", "Крейсер (3)", "Крейсер (3)",
    "Эсминец (2)", "Эсминец (2)", "Эсминец (2)",
    "Катер (1)", "Катер (1)", "Катер (1)", "Катер (1)"
]

# Коды клеток
EMPTY, SHIP, HIT, MISS, DEAD = 0, 1, 2, 3, 4

# Цвета
COL_EMPTY = "light blue"
COL_GRID = "black"
COL_SHIP = "blue"
COL_HOVER = "green"
COL_MISS = "white"
COL_DEAD = "darkred"

NEI8 = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)]
NEI4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def new_board():
    return [[EMPTY] * BOARD for _ in range(BOARD)]


def inb(r, c):
    return 0 <= r < BOARD and 0 <= c < BOARD


def ship_cells(board, r, c):
    """Все клетки корабля (связность по 4 сторонам), SHIP/HIT считаем частью корабля."""
    stack = [(r, c)]
    seen = set()
    cells = []
    while stack:
        rr, cc = stack.pop()
        if (rr, cc) in seen or not inb(rr, cc) or board[rr][cc] not in (SHIP, HIT):
            continue
        seen.add((rr, cc))
        cells.append((rr, cc))
        for dr, dc in NEI4:
            stack.append((rr + dr, cc + dc))
    return cells


def can_place(board, r, c, size, direction):
    coords = []
    for i in range(size):
        rr = r + i if direction == "V" else r
        cc = c + i if direction == "H" else c
        if not inb(rr, cc):
            return False
        coords.append((rr, cc))

    for rr, cc in coords:
        for dr, dc in NEI8:
            nr, nc = rr + dr, cc + dc
            if inb(nr, nc) and board[nr][nc] != EMPTY:
                return False
    return True


def place_random(board, size):
    while True:
        direction = random.choice(["H", "V"])
        r = random.randrange(BOARD)
        c = random.randrange(BOARD)
        if can_place(board, r, c, size, direction):
            for i in range(size):
                rr = r + i if direction == "V" else r
                cc = c + i if direction == "H" else c
                board[rr][cc] = SHIP
            return


def place_all_random(board):
    for s in SHIPS:
        place_random(board, s)


def count_alive_cells(board):
    return sum(cell == SHIP for row in board for cell in row)


def rect(canvas, r, c, color, **kw):
    x1, y1 = c * CELL, r * CELL
    x2, y2 = x1 + CELL, y1 + CELL
    return canvas.create_rectangle(x1, y1, x2, y2, fill=color, **kw)


def draw_hit(canvas, r, c):
    pad = 5
    x1, y1 = c * CELL + pad, r * CELL + pad
    x2, y2 = (c + 1) * CELL - pad, (r + 1) * CELL - pad
    canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
    canvas.create_line(x1, y2, x2, y1, fill="red", width=2)


def draw(canvas, board, show_ships):
    canvas.delete("all")

    # grid
    for i in range(BOARD + 1):
        x = i * CELL
        y = i * CELL
        canvas.create_line(x, 0, x, BOARD * CELL, fill=COL_GRID)
        canvas.create_line(0, y, BOARD * CELL, y, fill=COL_GRID)

    # cells
    for r in range(BOARD):
        for c in range(BOARD):
            v = board[r][c]
            if v == SHIP and show_ships:
                rect(canvas, r, c, COL_SHIP)
            elif v == MISS:
                rect(canvas, r, c, COL_MISS)
            elif v == DEAD:
                rect(canvas, r, c, COL_DEAD)
            elif v == HIT:
                draw_hit(canvas, r, c)


def maybe_destroy(board, r, c):
    cells = ship_cells(board, r, c)
    if cells and all(board[rr][cc] == HIT for rr, cc in cells):
        for rr, cc in cells:
            board[rr][cc] = DEAD
        return True
    return False


# ------------------- UI + Логика без классов -------------------

root = tk.Tk()
root.title("Морской бой")
root.geometry("1050x950")

main_frame = tk.Frame(root, bg="lightgray")
main_frame.pack(expand=True)

# Player
player_frame = tk.Frame(main_frame, bg="lightgray")
player_frame.grid(row=0, column=0, padx=50, pady=10)

tk.Label(player_frame, text="Ваша доска", font=("Arial", 14, "bold")).pack(pady=5)
current_ship_label = tk.Label(player_frame, text=f"Ставим: {SHIP_NAMES[0]}", font=("Arial", 12, "bold"))
current_ship_label.pack(pady=5)

player_canvas = tk.Canvas(
    player_frame, width=BOARD * CELL + 1, height=BOARD * CELL + 1,
    bg=COL_EMPTY, highlightthickness=0
)
player_canvas.pack(pady=5)

# Computer
computer_frame = tk.Frame(main_frame, bg="lightgray")
computer_frame.grid(row=0, column=1, padx=50, pady=10)

tk.Label(computer_frame, text="Доска компьютера", font=("Arial", 14, "bold")).pack(pady=5)

computer_canvas = tk.Canvas(
    computer_frame, width=BOARD * CELL + 1, height=BOARD * CELL + 1,
    bg=COL_EMPTY, highlightthickness=0
)
computer_canvas.pack(pady=5)

# Buttons
button_frame = tk.Frame(root, bg="lightgray")
button_frame.pack(pady=10)

# --- Состояние в одном месте ---
state = {
    "player": new_board(),
    "computer": new_board(),
    "manual_idx": 0,
    "direction": "H",
    "started": False,

    "hover": None,      # (r,c) куда можно поставить по Enter
    "mouse": (0, 0),    # последние координаты мыши
}


def update_ship_label():
    i = state["manual_idx"]
    if i >= len(SHIPS):
        current_ship_label.config(text="Все корабли размещены!")
    else:
        current_ship_label.config(text=f"Ставим: {SHIP_NAMES[i]}")


def enable_manual():
    if state["started"]:
        return
    player_canvas.bind("<Button-1>", on_player_click)


def place_ship_at(r, c):
    """Поставить текущий корабль с (r,c). True если поставили."""
    if state["started"]:
        return False
    if state["manual_idx"] >= len(SHIPS):
        messagebox.showinfo("Готово", "Все корабли размещены!")
        return False

    size = SHIPS[state["manual_idx"]]
    direction = state["direction"]

    if not can_place(state["player"], r, c, size, direction):
        return False

    for i in range(size):
        rr = r + i if direction == "V" else r
        cc = c + i if direction == "H" else c
        state["player"][rr][cc] = SHIP

    state["manual_idx"] += 1
    update_ship_label()
    draw(player_canvas, state["player"], True)
    player_canvas.delete("hover")
    state["hover"] = None
    return True


def place_from_hover():
    """Постановка по Enter в позицию зелёного силуэта."""
    if state["hover"] is None:
        return
    r, c = state["hover"]
    if not place_ship_at(r, c):
        messagebox.showwarning("Ошибка", "Невозможно разместить корабль здесь")


def on_key(event):
    key = event.keysym.lower()

    if key == "r":
        state["direction"] = "V" if state["direction"] == "H" else "H"
        # обновим силуэт после поворота
        x, y = state["mouse"]
        fake = type("E", (), {"x": x, "y": y})
        on_hover(fake)

    elif key in ("return", "kp_enter"):
        place_from_hover()


def on_hover(event):
    state["mouse"] = (event.x, event.y)
    player_canvas.delete("hover")
    state["hover"] = None

    if state["started"] or state["manual_idx"] >= len(SHIPS):
        return

    r, c = event.y // CELL, event.x // CELL
    size = SHIPS[state["manual_idx"]]

    if can_place(state["player"], r, c, size, state["direction"]):
        state["hover"] = (r, c)
        for i in range(size):
            rr = r + i if state["direction"] == "V" else r
            cc = c + i if state["direction"] == "H" else c
            rect(player_canvas, rr, cc, COL_HOVER, stipple="gray50", tags="hover")


def on_player_click(event):
    r, c = event.y // CELL, event.x // CELL
    if not place_ship_at(r, c):
        messagebox.showwarning("Ошибка", "Невозможно разместить корабль здесь")


def clear_player():
    if state["started"]:
        return
    state["player"] = new_board()
    state["manual_idx"] = 0
    state["direction"] = "H"
    state["hover"] = None
    player_canvas.delete("hover")
    update_ship_label()
    draw(player_canvas, state["player"], True)


def auto_place():
    if state["started"]:
        return
    state["player"] = new_board()
    place_all_random(state["player"])
    state["manual_idx"] = len(SHIPS)
    state["hover"] = None
    player_canvas.delete("hover")
    update_ship_label()
    draw(player_canvas, state["player"], True)


def computer_turn():
    candidates = [
        (r, c) for r in range(BOARD) for c in range(BOARD)
        if state["player"][r][c] in (EMPTY, SHIP)
    ]
    if not candidates:
        return

    r, c = random.choice(candidates)
    if state["player"][r][c] == SHIP:
        state["player"][r][c] = HIT
        destroyed = maybe_destroy(state["player"], r, c)
        draw(player_canvas, state["player"], True)

        if destroyed:
            messagebox.showinfo("Внимание!", "Компьютер уничтожил ваш корабль!")

        if count_alive_cells(state["player"]) == 0:
            messagebox.showinfo("Поражение", "Компьютер победил!")
    else:
        state["player"][r][c] = MISS
        draw(player_canvas, state["player"], True)


def on_computer_click(event):
    if not state["started"]:
        return

    r, c = event.y // CELL, event.x // CELL
    cell = state["computer"][r][c]
    if cell in (HIT, MISS, DEAD):
        return

    if cell == SHIP:
        state["computer"][r][c] = HIT
        destroyed = maybe_destroy(state["computer"], r, c)
        draw(computer_canvas, state["computer"], False)

        if destroyed:
            messagebox.showinfo("Убит!", "Вы уничтожили корабль противника!")

        if count_alive_cells(state["computer"]) == 0:
            messagebox.showinfo("Победа", "Вы победили!")
            return
    else:
        state["computer"][r][c] = MISS
        draw(computer_canvas, state["computer"], False)
        computer_turn()


def start_game():
    if state["started"]:
        return
    if state["manual_idx"] < len(SHIPS):
        messagebox.showwarning("Ошибка", "Разместите все корабли перед боем!")
        return

    state["started"] = True
    current_ship_label.config(text="Игра началась! Стреляйте по доске компьютера.")
    player_canvas.unbind("<Button-1>")
    player_canvas.delete("hover")
    state["hover"] = None
    computer_canvas.bind("<Button-1>", on_computer_click)


def new_game():
    state["started"] = False
    state["player"] = new_board()
    state["computer"] = new_board()
    place_all_random(state["computer"])

    state["manual_idx"] = 0
    state["direction"] = "H"
    state["hover"] = None
    update_ship_label()

    computer_canvas.unbind("<Button-1>")
    player_canvas.bind("<Motion>", on_hover)

    draw(player_canvas, state["player"], True)
    draw(computer_canvas, state["computer"], False)


# Buttons
tk.Button(button_frame, text="Авторазмещение", command=auto_place).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Ручное размещение", command=enable_manual).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Очистить доску", command=clear_player).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="В бой!", command=start_game).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Новая игра", command=new_game).pack(side=tk.LEFT, padx=5)

# Инструкция
instructions_frame = tk.Frame(root, bg="lightgray")
instructions_frame.pack(pady=10)

instructions_text = tk.Label(
    instructions_frame,
    text=(
        "Управление:\n"
        "- Ручная расстановка: клик по клетке\n"
        "- Поворот корабля: клавиша R\n"
        "- Поставить корабль по силуэту: Enter\n"
        "- Авторасстановка: кнопка 'Авторазмещение'\n"
        "- Очистка доски: кнопка 'Очистить доску'\n"
        "- Начало игры: кнопка 'В бой!'\n\n"
        "Обозначения:\n"
    ),
    justify=tk.LEFT,
    font=("Arial", 11),
    bg="lightgray",
)
instructions_text.pack(anchor="w")

legend = [
    ("Пустая клетка", COL_EMPTY),
    ("Ваш корабль", COL_SHIP),
    ("Силуэт текущего корабля", COL_HOVER),
    ("Попадание", "red"),
    ("Промах", COL_MISS),
    ("Уничтоженный корабль", COL_DEAD),
]
for text, color in legend:
    row = tk.Frame(instructions_frame, bg="lightgray")
    row.pack(anchor="w", pady=2)
    tk.Label(row, bg=color, width=2, height=1, relief="ridge", borderwidth=1).pack(side=tk.LEFT, padx=5)
    tk.Label(row, text=text, bg="lightgray", font=("Arial", 11)).pack(side=tk.LEFT)

# Bindings + init
player_canvas.bind("<Motion>", on_hover)
root.bind("<Key>", on_key)
new_game()
root.mainloop()
