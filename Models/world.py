import random
from typing import Optional, Tuple, List, Iterable
from modele.humain import Humain
from modele.enums import Sex

Coord = Tuple[int, int]

class World:
    """
    Grille 2D (au plus un humain par case).
    step() = un 'tick' :
      1) chaque humain tente de se déplacer d'UNE case (haut/bas/gauche/droite) vers une case libre
      2) pour chaque FEMME, si un HOMME est adjacent, on tente UNE naissance
         → l'enfant est placé sur une case voisine LIBRE de la mère ; sinon pas de naissance
    """
    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        assert width > 0 and height > 0
        self.w = width
        self.h = height
        self.grid: List[List[Optional[Humain]]] = [[None for _ in range(width)] for _ in range(height)]
        if seed is not None:
            random.seed(seed)

    # ---------- utilitaires ----------
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def is_empty(self, x: int, y: int) -> bool:
        return self.in_bounds(x, y) and (self.grid[y][x] is None)

    def neighbors4(self, x: int, y: int) -> Iterable[Coord]:
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield (nx, ny)

    # ---------- placements ----------
    def place_random(self, person: Humain) -> Optional[Coord]:
        empties = [(x, y) for y in range(self.h) for x in range(self.w) if self.grid[y][x] is None]
        if not empties:
            return None
        x, y = random.choice(empties)
        self.grid[y][x] = person
        return (x, y)

    def place_at(self, x: int, y: int, person: Humain) -> bool:
        if self.is_empty(x, y):
            self.grid[y][x] = person
            return True
        return False

    def find_all(self) -> List[Tuple[Coord, Humain]]:
        res = []
        for y in range(self.h):
            for x in range(self.w):
                p = self.grid[y][x]
                if p is not None:
                    res.append(((x, y), p))
        return res

    # ---------- déplacements ----------
    def move_one_step_random(self, x: int, y: int) -> Coord:
        """Déplace d'UNE case vers une case vide aléatoire (sinon reste)."""
        person = self.grid[y][x]
        assert person is not None
        choices = [(nx, ny) for (nx, ny) in self.neighbors4(x, y) if self.grid[ny][nx] is None]
        if choices:
            nx, ny = random.choice(choices)
            self.grid[ny][nx] = person
            self.grid[y][x] = None
            return (nx, ny)
        return (x, y)

    # ---------- procréation ----------
    def try_birth_near_mother(self, mx: int, my: int, mother: Humain, father: Humain) -> bool:
        """
        Tentative de naissance :
          - probabilité = moyenne(mère.proba, père.proba)
          - placement du bébé sur une case VOISINE LIBRE de la mère
          - si aucune case libre → échec
        """
        if not (mother.vivant and father.vivant):
            return False

        p = max(0.0, min(1.0, (mother.proba_procreer + father.proba_procreer) / 2.0))
        if random.random() >= p:
            return False

        empties = [(nx, ny) for (nx, ny) in self.neighbors4(mx, my) if self.grid[ny][nx] is None]
        if not empties:
            return False

        # traits simples du bébé (peuvent être enrichis)
        sexe_bebe = Sex.MALE if random.random() < 0.5 else Sex.FEMALE
        duree = int(round((mother.duree_vie + father.duree_vie) / 2))
        proba = max(0.01, min(0.99, (mother.proba_procreer + father.proba_procreer) / 2))

        baby = Humain(age=0, duree_vie=duree, proba_procreer=proba, vivant=True, sexe=sexe_bebe)
        bx, by = random.choice(empties)
        self.grid[by][bx] = baby
        return True

    # ---------- un tick ----------
    def step(self) -> None:
        # 1) déplacements (ordre aléatoire)
        agents = self.find_all()
        random.shuffle(agents)
        for (x, y), _ in agents:
            if self.in_bounds(x, y) and self.grid[y][x] is not None:
                self.move_one_step_random(x, y)

        # 2) procréation (une tentative max par mère)
        for y in range(self.h):
            for x in range(self.w):
                mother = self.grid[y][x]
                if mother is None or mother.sexe != Sex.FEMALE or not mother.vivant:
                    continue
                # recherche d'au moins un homme vivant adjacent
                fathers = []
                for nx, ny in self.neighbors4(x, y):
                    neigh = self.grid[ny][nx]
                    if neigh is not None and neigh.sexe == Sex.MALE and neigh.vivant:
                        fathers.append(neigh)
                if not fathers:
                    continue
                father = random.choice(fathers)
                self.try_birth_near_mother(x, y, mother, father)
