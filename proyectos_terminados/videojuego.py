"""
╔══════════════════════════════════════╗
║         S N A K E  R E T R O         ║
║     100% Python — sin dependencias   ║
╚══════════════════════════════════════╝
"""

import tkinter as tk
import random

# ── Configuración ──────────────────────────────────────────────
COLS, ROWS   = 25, 20          # celdas del tablero
CELL         = 28              # píxeles por celda
WIDTH        = COLS * CELL
HEIGHT       = ROWS * CELL
PANEL_H      = 70              # panel superior (score / nivel)
SPEED_INIT   = 140             # ms entre frames (menor = más rápido)
SPEED_MIN    = 55
SPEED_STEP   = 6               # ms que se restan cada 3 manzanas

# ── Paleta retro ──────────────────────────────────────────────
BG_DARK      = "#0d0f1a"
BG_GRID      = "#111627"
GRID_LINE    = "#1a2040"
SNAKE_HEAD   = "#00ff99"
SNAKE_BODY   = "#00cc77"
SNAKE_SHINE  = "#88ffcc"
APPLE_COL    = "#ff3355"
APPLE_SHINE  = "#ff88aa"
APPLE_LEAF   = "#00cc44"
TEXT_MAIN    = "#00ff99"
TEXT_DIM     = "#335544"
TEXT_WHITE   = "#e0ffe8"
TEXT_ACCENT  = "#ffdd00"
BORDER_COL   = "#00ff99"
PANEL_BG     = "#080a14"
GHOST_COL    = "#1a2a1a"


def lerp_color(c1, c2, t):
    """Interpola dos colores hex."""
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    r = int(r1 + (r2-r1)*t)
    g = int(g1 + (g2-g1)*t)
    b = int(b1 + (b2-b1)*t)
    return f"#{r:02x}{g:02x}{b:02x}"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SNAKE RETRO")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT + PANEL_H,
            bg=BG_DARK,
            highlightthickness=2,
            highlightbackground=BORDER_COL
        )
        self.canvas.pack(padx=14, pady=14)

        # Estado
        self.high_score = 0
        self._after_id = None
        self.init_game()
        self.bind_keys()
        self.draw_frame()

    # ── Inicialización ────────────────────────────────────────
    def init_game(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake      = [(cx, cy), (cx-1, cy), (cx-2, cy)]
        self.direction  = (1, 0)
        self.next_dir   = (1, 0)
        self.score      = 0
        self.level      = 1
        self.apples_eaten = 0
        self.speed      = SPEED_INIT
        self.paused     = False
        self.game_over  = False
        self.flash_tick = 0
        self.place_apple()

    def place_apple(self):
        free = [(c, r) for c in range(COLS) for r in range(ROWS)
                if (c, r) not in self.snake]
        self.apple = random.choice(free) if free else None

    # ── Controles ─────────────────────────────────────────────
    def bind_keys(self):
        binds = {
            "<Up>":    (0,-1), "<w>": (0,-1), "<W>": (0,-1),
            "<Down>":  (0, 1), "<s>": (0, 1), "<S>": (0, 1),
            "<Left>":  (-1,0), "<a>": (-1,0), "<A>": (-1,0),
            "<Right>": (1, 0), "<d>": (1, 0), "<D>": (1, 0),
        }
        for key, d in binds.items():
            self.root.bind(key, lambda e, d=d: self.set_dir(d))
        self.root.bind("<p>",      lambda e: self.toggle_pause())
        self.root.bind("<P>",      lambda e: self.toggle_pause())
        self.root.bind("<r>",      lambda e: self.restart())
        self.root.bind("<R>",      lambda e: self.restart())
        self.root.bind("<Escape>", lambda e: self.root.quit())
        self.root.bind("<q>",      lambda e: self.root.quit())

    def set_dir(self, d):
        # No permitir reversa instantánea
        if (d[0] != -self.direction[0] or d[1] != -self.direction[1]):
            self.next_dir = d

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        if not self.paused:
            self.draw_frame()

    def restart(self):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self.init_game()
        self.draw_frame()

    # ── Lógica de juego ───────────────────────────────────────
    def step(self):
        if self.paused or self.game_over:
            return
        self.direction = self.next_dir
        hx, hy = self.snake[0]
        dx, dy  = self.direction
        nx, ny  = hx + dx, hy + dy

        # Colisión pared
        if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
            self.end_game(); return

        # Colisión consigo mismo
        if (nx, ny) in self.snake:
            self.end_game(); return

        self.snake.insert(0, (nx, ny))

        # ¿Comió manzana?
        if (nx, ny) == self.apple:
            self.score        += 10 + self.level * 2
            self.apples_eaten += 1
            self.high_score    = max(self.high_score, self.score)
            if self.apples_eaten % 3 == 0:
                self.level += 1
                self.speed  = max(SPEED_MIN, self.speed - SPEED_STEP)
            self.place_apple()
        else:
            self.snake.pop()

    def end_game(self):
        self.game_over = True
        self.high_score = max(self.high_score, self.score)

    # ── Renderizado ───────────────────────────────────────────
    def draw_frame(self):
        self.canvas.delete("all")
        self.draw_panel()
        self.draw_grid()
        self.draw_apple()
        self.draw_snake()
        if self.paused:
            self.draw_overlay("PAUSA", "Presiona P para continuar")
        if self.game_over:
            self.flash_tick += 1
            self.draw_game_over()

        if not self.game_over and not self.paused:
            self.step()
        self._after_id = self.root.after(self.speed, self.draw_frame)

    def draw_panel(self):
        # Fondo panel
        self.canvas.create_rectangle(
            0, 0, WIDTH, PANEL_H,
            fill=PANEL_BG, outline=""
        )
        # Línea separadora con brillo
        self.canvas.create_line(0, PANEL_H, WIDTH, PANEL_H,
                                fill=BORDER_COL, width=2)
        self.canvas.create_line(0, PANEL_H+1, WIDTH, PANEL_H+1,
                                fill=GHOST_COL, width=1)

        # Título pequeño
        self.canvas.create_text(
            WIDTH//2, 10,
            text="◈  S N A K E  R E T R O  ◈",
            fill=TEXT_DIM, font=("Courier", 9, "bold")
        )

        # Score
        self.canvas.create_text(
            30, 38,
            text="SCORE", fill=TEXT_DIM,
            font=("Courier", 9), anchor="w"
        )
        self.canvas.create_text(
            30, 56,
            text=f"{self.score:06d}", fill=TEXT_MAIN,
            font=("Courier", 18, "bold"), anchor="w"
        )

        # High score
        self.canvas.create_text(
            WIDTH//2, 38,
            text="MEJOR", fill=TEXT_DIM,
            font=("Courier", 9)
        )
        self.canvas.create_text(
            WIDTH//2, 56,
            text=f"{self.high_score:06d}", fill=TEXT_ACCENT,
            font=("Courier", 18, "bold")
        )

        # Nivel + manzanas
        self.canvas.create_text(
            WIDTH - 30, 38,
            text=f"NIV.{self.level}", fill=TEXT_DIM,
            font=("Courier", 9), anchor="e"
        )
        apples_to_next = 3 - (self.apples_eaten % 3)
        self.canvas.create_text(
            WIDTH - 30, 56,
            text=f"🍎×{apples_to_next}", fill=APPLE_COL,
            font=("Courier", 14, "bold"), anchor="e"
        )

    def draw_grid(self):
        y0 = PANEL_H
        # Fondo del tablero
        self.canvas.create_rectangle(
            0, y0, WIDTH, HEIGHT + y0,
            fill=BG_GRID, outline=""
        )
        # Líneas de cuadrícula
        for c in range(0, COLS+1):
            x = c * CELL
            self.canvas.create_line(x, y0, x, HEIGHT+y0,
                                    fill=GRID_LINE, width=1)
        for r in range(0, ROWS+1):
            y = y0 + r * CELL
            self.canvas.create_line(0, y, WIDTH, y,
                                    fill=GRID_LINE, width=1)

    def draw_apple(self):
        if not self.apple:
            return
        c, r = self.apple
        y0 = PANEL_H
        x1 = c * CELL + 3
        y1 = y0 + r * CELL + 3
        x2 = x1 + CELL - 6
        y2 = y1 + CELL - 6
        # Sombra
        self.canvas.create_oval(x1+2, y1+2, x2+2, y2+2,
                                fill="#330011", outline="")
        # Cuerpo
        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=APPLE_COL, outline="#ff6677", width=1)
        # Brillo
        self.canvas.create_oval(x1+3, y1+3, x1+8, y1+8,
                                fill=APPLE_SHINE, outline="")
        # Hoja
        self.canvas.create_line(
            (x1+x2)//2, y1,
            (x1+x2)//2 - 4, y1 - 5,
            fill=APPLE_LEAF, width=2
        )

    def draw_snake(self):
        y0 = PANEL_H
        total = len(self.snake)
        for i, (c, r) in enumerate(self.snake):
            t   = i / max(total - 1, 1)
            col = lerp_color(SNAKE_HEAD, SNAKE_BODY, t)
            x1  = c * CELL + 2
            y1  = y0 + r * CELL + 2
            x2  = x1 + CELL - 4
            y2  = y1 + CELL - 4
            pad = min(i * 0.3, 3)

            # Sombra
            self.canvas.create_rectangle(
                x1+2+pad, y1+2+pad, x2+2-pad, y2+2-pad,
                fill="#001a0a", outline=""
            )
            # Cuerpo
            radius = 6 if i == 0 else 4
            self._rounded_rect(x1+pad, y1+pad, x2-pad, y2-pad,
                               radius, fill=col, outline="")

            if i == 0:
                # Brillo cabeza
                self.canvas.create_oval(
                    x1+5, y1+5, x1+10, y1+10,
                    fill=SNAKE_SHINE, outline=""
                )
                # Ojos según dirección
                self._draw_eyes(c, r, y0)

    def _rounded_rect(self, x1, y1, x2, y2, r, **kw):
        self.canvas.create_polygon(
            x1+r, y1,  x2-r, y1,
            x2,   y1+r, x2,  y2-r,
            x2-r, y2,  x1+r, y2,
            x1,   y2-r, x1,  y1+r,
            smooth=True, **kw
        )

    def _draw_eyes(self, c, r, y0):
        dx, dy = self.direction
        cx = c * CELL + CELL // 2
        cy = y0 + r * CELL + CELL // 2
        offsets = {
            (1,  0): [( 4, -4), ( 4,  4)],
            (-1, 0): [(-4, -4), (-4,  4)],
            (0, -1): [(-4, -4), ( 4, -4)],
            (0,  1): [(-4,  4), ( 4,  4)],
        }
        for ox, oy in offsets.get((dx, dy), [(4,-4),(4,4)]):
            self.canvas.create_oval(
                cx+ox-3, cy+oy-3, cx+ox+3, cy+oy+3,
                fill="white", outline=""
            )
            self.canvas.create_oval(
                cx+ox-1, cy+oy-1, cx+ox+1, cy+oy+1,
                fill=BG_DARK, outline=""
            )

    def draw_overlay(self, title, subtitle):
        y0 = PANEL_H
        self.canvas.create_rectangle(
            0, y0, WIDTH, HEIGHT+y0,
            fill="#000000cc", stipple="gray50", outline=""
        )
        self.canvas.create_text(
            WIDTH//2, y0 + HEIGHT//2 - 20,
            text=title, fill=TEXT_ACCENT,
            font=("Courier", 32, "bold")
        )
        self.canvas.create_text(
            WIDTH//2, y0 + HEIGHT//2 + 20,
            text=subtitle, fill=TEXT_WHITE,
            font=("Courier", 13)
        )

    def draw_game_over(self):
        y0 = PANEL_H
        # Overlay semitransparente con stipple
        self.canvas.create_rectangle(
            0, y0, WIDTH, HEIGHT+y0,
            fill=BG_DARK, stipple="gray75", outline=""
        )
        # Título parpadeante
        flash_col = TEXT_ACCENT if (self.flash_tick // 4) % 2 == 0 else APPLE_COL
        self.canvas.create_text(
            WIDTH//2, y0 + HEIGHT//2 - 55,
            text="◆ GAME OVER ◆",
            fill=flash_col, font=("Courier", 28, "bold")
        )
        # Score final
        self.canvas.create_text(
            WIDTH//2, y0 + HEIGHT//2,
            text=f"Puntuación: {self.score:,}",
            fill=TEXT_WHITE, font=("Courier", 15)
        )
        # High score
        hs_col = TEXT_ACCENT if self.score >= self.high_score and self.score > 0 else TEXT_DIM
        hs_txt = "¡NUEVO RÉCORD!" if self.score == self.high_score and self.score > 0 else f"Récord: {self.high_score:,}"
        self.canvas.create_text(
            WIDTH//2, y0 + HEIGHT//2 + 35,
            text=hs_txt, fill=hs_col,
            font=("Courier", 12, "bold")
        )
        # Instrucciones
        self.canvas.create_text(
            WIDTH//2, y0 + HEIGHT//2 + 75,
            text="[ R ] reiniciar   [ Q ] salir",
            fill=TEXT_DIM, font=("Courier", 11)
        )


# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#000000")

    # Centrar ventana
    w = WIDTH  + 28
    h = HEIGHT + PANEL_H + 28
    root.geometry(f"{w}x{h}+{(root.winfo_screenwidth()-w)//2}+{(root.winfo_screenheight()-h)//2}")

    game = SnakeGame(root)
    root.mainloop()