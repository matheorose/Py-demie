import argparse
from typing import Optional
import tkinter as tk
from tkinter import ttk

from Enums.Sex import Sex
from Game.Game import Game
from Models.World import PopulationDead


class SimulationApp:
    """Interface Tkinter pour visualiser la simulation sans modifier sa logique."""

    CELL_SIZE = 42
    COLOR_BG = "#0f172a"
    COLOR_GRID = "#1e293b"
    COLOR_EMPTY = "#e2e8f0"
    COLOR_MALE = "#3b82f6"
    COLOR_FEMALE = "#ec4899"
    COLOR_UNKNOWN = "#94a3b8"

    def __init__(
        self,
        width: int,
        height: int,
        nb_humains: int,
        tours: int,
        interval_ms: int = 600,
        seed: Optional[int] = 125,
    ) -> None:
        self.game = Game(width=width, height=height, nb_humains=nb_humains, seed=seed)
        self.max_tours = tours
        self.interval_ms = max(50, interval_ms)
        self.current_tour = 0
        self.running = True
        self._after_id: Optional[str] = None

        self.root = tk.Tk()
        self.root.title("Py-demie - Simulation graphique")
        self.root.configure(bg=self.COLOR_BG)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.status_var = tk.StringVar()
        self.status_var.set(self._status_label())

        self._build_layout()
        self._render_initial_state()

        if self._count_alive() > 0 and self.max_tours > 0:
            self._after_id = self.root.after(self.interval_ms, self._run_next_tick)

    # ------------------------------------------------------------------ UI setup
    def _build_layout(self) -> None:
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=16)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(1, weight=1)

        canvas_width = self.game.world.largeur * self.CELL_SIZE
        canvas_height = self.game.world.hauteur * self.CELL_SIZE
        self.canvas = tk.Canvas(
            main,
            width=canvas_width,
            height=canvas_height,
            bg=self.COLOR_BG,
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 16))

        self._create_cells()

        info_frame = ttk.Frame(main)
        info_frame.grid(row=0, column=1, sticky="new")

        ttk.Label(info_frame, textvariable=self.status_var).pack(anchor="w")
        ttk.Label(info_frame, text="Couleurs des cellules :", padding=(0, 12, 0, 4)).pack(
            anchor="w"
        )
        self._build_legend(info_frame)

        log_frame = ttk.Frame(main)
        log_frame.grid(row=1, column=1, sticky="nsew")
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_frame,
            width=48,
            height=20,
            font=("Courier New", 11),
            bg="#020617",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            state="disabled",
            wrap="word",
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def _build_legend(self, parent: ttk.Frame) -> None:
        legend = ttk.Frame(parent)
        legend.pack(anchor="w", fill="x")

        for color, label in (
            (self.COLOR_MALE, "Homme"),
            (self.COLOR_FEMALE, "Femme"),
            (self.COLOR_UNKNOWN, "Sexe inconnu"),
            (self.COLOR_EMPTY, "Case vide"),
        ):
            item = ttk.Frame(legend)
            item.pack(anchor="w", pady=2, fill="x")
            swatch = tk.Canvas(item, width=18, height=18, highlightthickness=0)
            swatch.create_rectangle(0, 0, 18, 18, fill=color, outline=self.COLOR_GRID)
            swatch.pack(side="left", padx=(0, 8))
            ttk.Label(item, text=label).pack(side="left")

    def _create_cells(self) -> None:
        self._cells: dict[tuple[int, int], int] = {}
        for y in range(self.game.world.hauteur):
            for x in range(self.game.world.largeur):
                x1 = x * self.CELL_SIZE
                y1 = y * self.CELL_SIZE
                rect_id = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x1 + self.CELL_SIZE,
                    y1 + self.CELL_SIZE,
                    outline=self.COLOR_GRID,
                    width=1,
                    fill=self.COLOR_EMPTY,
                )
                self._cells[(x, y)] = rect_id

    # ---------------------------------------------------------------- Rendering
    def _render_initial_state(self) -> None:
        self._update_cells()
        vivants = self._count_alive()
        self._write_log("=== ÉTAT INITIAL ===\n")
        self._write_log(self.game.world._to_string() + "\n")
        self._write_log(f"Vivants: {vivants}\n\n")

    def _update_cells(self) -> None:
        for y in range(self.game.world.hauteur):
            for x in range(self.game.world.largeur):
                humain = self.game.world.grille[y][x]
                color = self.COLOR_EMPTY if humain is None else self._color_for_human(humain)
                self.canvas.itemconfigure(self._cells[(x, y)], fill=color)
        self.canvas.update_idletasks()

    def _color_for_human(self, humain) -> str:
        sexe = getattr(humain, "sexe", None)
        if sexe == Sex.MALE:
            return self.COLOR_MALE
        if sexe == Sex.FEMALE:
            return self.COLOR_FEMALE
        return self.COLOR_UNKNOWN

    def _status_label(self) -> str:
        return f"Tour {self.current_tour}/{self.max_tours} • Vivants: {self._count_alive()}"

    def _write_log(self, text: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # ------------------------------------------------------------- Simulation
    def _run_next_tick(self) -> None:
        if not self.running:
            return

        if self.current_tour >= self.max_tours:
            self.status_var.set("Simulation terminée")
            return

        self.current_tour += 1
        self._write_log(f"\n\n=== TOUR {self.current_tour} ===\n")

        try:
            self.game.world.tick()
        except PopulationDead:
            self._update_cells()
            self.status_var.set(f"Population éteinte au tour {self.current_tour}")
            self._write_log(self.game.world._to_string() + "\n")
            self._write_log("Vivants: 0\n")
            return

        self._update_cells()
        vivants = self._count_alive()
        self.status_var.set(self._status_label())
        self._write_log(self.game.world._to_string() + "\n")
        self._write_log(f"Vivants: {vivants}\n")

        if vivants == 0 or self.current_tour >= self.max_tours:
            return

        if self.running:
            self._after_id = self.root.after(self.interval_ms, self._run_next_tick)

    def _count_alive(self) -> int:
        return sum(1 for _ in self.game.world.each_human())

    def _on_close(self) -> None:
        self.running = False
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.root.destroy()

    def start(self) -> None:
        self.root.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Affiche la simulation Py-demie dans une fenêtre Tkinter."
    )
    parser.add_argument("--width", type=int, default=7, help="Largeur de la grille.")
    parser.add_argument("--height", type=int, default=7, help="Hauteur de la grille.")
    parser.add_argument(
        "--humains", type=int, default=15, help="Nombre d'humains à générer initialement."
    )
    parser.add_argument("--tours", type=int, default=60, help="Nombre de tours à jouer.")
    parser.add_argument(
        "--interval",
        type=int,
        default=600,
        help="Intervalle en millisecondes entre deux tours.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=125,
        help="Seed aléatoire pour reproduire les résultats.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = SimulationApp(
        width=args.width,
        height=args.height,
        nb_humains=args.humains,
        tours=args.tours,
        interval_ms=args.interval,
        seed=args.seed,
    )
    app.start()


if __name__ == "__main__":
    main()
