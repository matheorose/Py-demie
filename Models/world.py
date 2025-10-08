# Models/world.py
import random
from typing import Tuple
from .Humain import Humain
from ..Enums.Sex import Sex

Coord = Tuple[int, int]

class World:
    """
    Grille 2D (au plus un humain par case).
    - __init__(w, h, seed): crée la matrice w×h remplie de None
    - populate_random(n, male_ratio): place n humains sur des cases vides aléatoires
    - tick(): à compléter plus tard (déplacements, rencontres, etc.)
    """

    def __init__(self, width: int, height: int):
        """Crée une grille vide de taille (width x height)."""
        print("init")
        self.largeur = width
        self.hauteur = height
        # Grille 2D : chaque case peut contenir un Humain ou None
        self.grille = [[None for _ in range(width)] for _ in range(height)]

    

    # ---------- utilitaires ----------
    def in_bounds(self, x: int, y: int) -> bool:
        """verifier si la case est dans la grille"""
        return 0 <= x < self.largeur and 0 <= y < self.hauteur

    def is_empty(self, x: int, y: int) -> bool:
        """verifier si la case est vide"""
        return self.in_bounds(x, y) and (self.grid[y][x] is None)

    def place_at(self, x: int, y: int, person: Humain) -> bool:
        """Place un humain sur (x,y) si la case est libre. Retourne True si OK."""
        print("place_at")
        if self.is_empty((x, y) and (self.in_bounds(x, y))):
            self.grid[y][x] = person
            person.coordoneeY = y
            person.coordoneeX = x
            return True
        print("Impossible de placer l'humain : " + person + ", sur la case x: "+ x +", y: " + y)
        return False

    def placer_humain_aleatoire(self, humain: Humain) -> bool:
        """Place un humain sur une case libre au hasard. Retourne True si réussi."""
        print("placer_humain_aleatoire")
        cases_vides = [
            (x, y)
            for y in range(self.hauteur)
            for x in range(self.largeur)
            if self.grille[y][x] is None
        ]

        if not cases_vides:
            print("Il n'y a plus de places dans la grille")
            return False  # plus de place disponible

        x, y = random.choice(cases_vides)
        self.grille[y][x] = humain
        humain.coordoneeX = x
        humain.coordoneeY = y
        return True
    

    # ------------------------------------------------------------
    # Crée un humain aléatoire (homme ou femme)
    # ------------------------------------------------------------
    def creer_humain_aleatoire(
        self,
        male_ratio: float,
        duree_vie_min: int,
        duree_vie_max: int,
        proba_min: float,
        proba_max: float,
    ) -> Humain:
        """Crée un humain avec des caractéristiques tirées au hasard."""
        print("creer_humain_aleatoire")
        sexe = Sex.MALE if random.random() < male_ratio else Sex.FEMALE
        duree_vie = random.randint(duree_vie_min, duree_vie_max)
        proba_procreer = random.uniform(proba_min, proba_max)

        return Humain(
            age=0,
            duree_vie=duree_vie,
            proba_procreer=proba_procreer,
            vivant=True,
            sexe=sexe,
        )
    

    # ------------------------------------------------------------
    # Remplit la grille avec des humains placés aléatoirement
    # ------------------------------------------------------------
    def remplir_grille(self, nb_humains: int, male_ratio: float = 0.5) -> int:
        """
        Ajoute nb_humains sur la grille à des positions aléatoires.
        Retourne le nombre d'humains effectivement placés.
        """
        print("remplir_grille")
        humains_places = 0

        for _ in range(nb_humains):
            # Créer un humain avec des caractéristiques aléatoires
            h = self.creer_humain_aleatoire(
                male_ratio,
                duree_vie_min=60,
                duree_vie_max=90,
                proba_min=0.05,
                proba_max=0.30,
            )

            # Tenter de le placer sur la grille
            if self.placer_humain_aleatoire(h):
                humains_places += 1
            else:
                print("La grille est pleine")
                break  # grille pleine

        return humains_places

    # ---------- tick (à coder plus tard) ----------
    def tick(self) -> None:
        """Un pas de simulation (déplacements, rencontres, naissances...). À implémenter ensuite."""
        print("tick")
        return None
