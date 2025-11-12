# Models/world.py
import random
from typing import Iterable, List, Tuple
from .Humain import Humain
from Enums.Sex import Sex
from Enums.Direction import Direction 
import sys


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
        self.humans: List[Humain] = []
        # Grille 2D : chaque case peut contenir un Humain ou None
        self.grille = [[None for _ in range(width)] for _ in range(height)]

    

    # ---------- utilitaires ----------
    def in_bounds(self, x: int, y: int) -> bool:
        """verifier si la case est dans la grille"""
        return 0 <= x < self.largeur and 0 <= y < self.hauteur


    def is_empty(self, x: int, y: int) -> bool:
        """verifier si la case est vide"""
        return self.in_bounds(x, y) and (self.grille[y][x] is None)


    def place_at(self, x: int, y: int, person: Humain) -> bool:
        """Place un humain sur (x,y) si la case est libre. Retourne True si OK."""
        if self.is_empty(x, y):
            self.grille[y][x] = person
            
             # si l'objet Humain ne possède pas ces attributs, ceci n'explose pas
            if hasattr(person, "coordoneeX"): person.coordoneeX = x
            if hasattr(person, "coordoneeY"): person.coordoneeY = y

            return True
        
        print("Impossible de placer l'humain : " + person + ", sur la case x: "+ x +", y: " + y)
        return False


    def placer_humain_aleatoire(self, humain: Humain) -> bool:
        """Place un humain sur une case libre au hasard. Retourne True si réussi."""
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

        if self.place_at(x, y, humain):
            self.humans.append(humain)
            return True
        else:
            return False
    

    # ------------------------------------------------------------
    # Crée un humain aléatoire (homme ou femme)
    # ------------------------------------------------------------
    def creer_humain_aleatoire(
        self,
        male_ratio: float,
        duree_vie_min: int,
        duree_vie_max: int,
        age_min: int,
        age_max: int,
        proba_min: float,
        proba_max: float,
    ) -> Humain:
        """Crée un humain avec des caractéristiques tirées au hasard."""
        sexe = Sex.MALE if random.random() < male_ratio else Sex.FEMALE
        age = random.randint(age_min, age_max)
        duree_vie = random.randint(duree_vie_min, duree_vie_max)
        proba_procreer = random.uniform(proba_min, proba_max)

        return Humain(
            age=age,
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
        humains_places = 0

        for _ in range(nb_humains):
            # Créer un humain avec des caractéristiques aléatoires
            h = self.creer_humain_aleatoire(
                male_ratio,
                duree_vie_min=60,
                duree_vie_max=80,
                age_min=20,
                age_max=60,
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
    
    
    
    
    def _wrap(self, x: int, y: int) -> Coord:
        """Applique l'effet torus : dépassement d'un bord -> réapparaît de l'autre côté."""
        return (x % self.largeur, y % self.hauteur)
    
    
    def deplacer(self, humain: Humain, nx: int, ny: int, grid=None, *, origine_deja_videe: bool = False) -> bool:
        if not humain.vivant:
            return False
        if grid is None:
            grid = self.grille

        nx, ny = self._wrap(nx, ny)  # torus
        ox, oy = humain.coordoneeX, humain.coordoneeY
        if ox is None or oy is None or not self.in_bounds(ox, oy):
            return False
        if grid[ny][nx] is not None:
            return False

        if not origine_deja_videe and grid[oy][ox] is humain:
            grid[oy][ox] = None

        grid[ny][nx] = humain
        humain.coordoneeX, humain.coordoneeY = nx, ny
        return True

    
    # + utilitaire
    def each_human(self):   
        for y in range(self.hauteur):
            for x in range(self.largeur):
                h = self.grille[y][x]
                if h is not None:
                    yield h


    def _to_string(self) -> str:
        """
        Construit une représentation ASCII de la grille :
        - '1' si case occupée, '0' sinon
        - '|' pour les colonnes, lignes horizontales en '-'
        """
        # ligne horizontale (—) : largeur * 4 (espaces + séparateurs) + 1 bord
        hline = "-" * (self.largeur * 4 + 1)
        lines = [hline]
        for y in range(self.hauteur):
            row_cells = []
            for x in range(self.largeur):
                row_cells.append(f" {1 if self.grille[y][x] is not None else 0} ")
            row = "|" + "|".join(row_cells) + "|"
            lines.append(row)
            lines.append(hline)
        return "\n".join(lines)
        
        
    def _vieillissement_population(self) -> List[Humain]:
        humains = list(self.each_human())
        random.shuffle(humains)
        
        alive_humans: List[Humain] = []
        for h in humains:
            h.vieillir()
            if not h.vivant:
                x, y = h.coordoneeX, h.coordoneeY
                if x is not None and y is not None and self.in_bounds(x, y) and self.grille[y][x] is h:
                    self.grille[y][x] = None
                    print("L'humain en x: " + str(x) + ", y: " + str(y) + " est mort")
                # ne pas ajouter à alive_humans -> il est mort
            else:
                alive_humans.append(h)
            
        # (optionnel) garder self.humans propre
        self.humans = [h for h in self.humans if h.vivant]
            
        return alive_humans
        
    def _vider_origine_sur_grille(self, grid, humain: Humain) -> None:
        ox, oy = humain.coordoneeX, humain.coordoneeY
        if ox is not None and oy is not None and self.in_bounds(ox, oy) and grid[oy][ox] is humain:
            grid[oy][ox] = None
        

    # ---------- tick (exemple minimal) ----------
    def tick(self) -> None:
        """
        Exemple minimal: chaque humain tente de bouger d'1 case
        dans une direction aléatoire.
        Tous les humains doivent se déplacer en meme temps.
        Pour se faire, on va créer une deuxième matrice qui va calculer le nombre de personnes qui ont décidés d'aller sur une même case.
        Nous allons donc avoir dans cette matrice et pour chaque cases, un x, un y et une liste d'humains qui souhaitent accéder à cette case.
        Dans ce cas là, un des humains sera désignés et les autres resteront immobiles. 
        Pour cela, il faut copier la matrice actuelle et prédire les mouvements en fonction des cases actuellement disponibles.
        ATTENTION : dans le cas de plusieurs personnes qui souhaitent aller sur une meme case, il ne faut pas prendre le premier humain et il a une chance sur le nombre d'huamains. il faut faire un random.choice sur la liste
        """
        
        # --- 1) Vieillissement + suppression des morts de la grille ---
        alive_humans: List[Humain] = self._vieillissement_population()
    
        if not alive_humans:
            print("Toute la population est morte.")
            sys.exit(0)
            return  # plus personne
            
        # --- 2) Intentions ---
        ordered_dirs = [
            Direction.GAUCHE, Direction.DROITE, Direction.HAUT, Direction.BAS,
            Direction.HAUT_GAUCHE, Direction.HAUT_DROITE, Direction.BAS_GAUCHE, Direction.BAS_DROITE,
            Direction.IMMOBILE
        ]

        intentions: dict[Coord, List[Humain]] = {}
        
        for h in alive_humans:
            x, y = h.coordoneeX, h.coordoneeY
            if x is None or y is None or not self.in_bounds(x, y) or self.grille[y][x] is not h:
                print("sécurité")
                continue  # sécurité

            cible: Coord | None = None
            # Mélange les directions à chaque tour pour éviter le biais
            dirs = random.sample(ordered_dirs, len(ordered_dirs))
            for d in dirs:
                if d is Direction.IMMOBILE:
                    break  # ne bouge pas 
                nx, ny = self._wrap(x + d.dx, y + d.dy)
                if self.is_empty(nx, ny):
                    cible = (nx, ny)
                    break

            if cible is not None:
                intentions.setdefault(cible, []).append(h)

        if not intentions:
            print("Toute la population est restée sur place")
            return

        # Debug intentions
        print("Intentions (cible <- nb candidats):")
        for (nx, ny), hs in intentions.items():
            print(f"Plusieurs personnes souhaitent alle sur cette case : ({nx},{ny}) <- nombres de personnes {len(hs)}")

        # --- 3) Conflits : un gagnant par case ---
        winners: dict[int, Tuple[Humain, Coord]] = {}
        for target, candidats in intentions.items():
            gagnant = random.choice(candidats)
            winners[id(gagnant)] = (gagnant, target)

        print("Winners (gagnants):")
        for _, (h, (nx, ny)) in winners.items():
            ox, oy = h.coordoneeX, h.coordoneeY
            print(f"  id={id(h)}: ({ox},{oy}) -> ({nx},{ny})")

        # --- 4) Application simultanée ---
        new_grille = [row.copy() for row in self.grille]

        # vider les origines des gagnants
        for _, (h, _) in winners.items():
            self._vider_origine_sur_grille(new_grille, h)

        # placer tous les gagnants
        for _, (h, (nx, ny)) in winners.items():
            self.deplacer(h, nx, ny, grid=new_grille, origine_deja_videe=True)

        self.grille = new_grille
        
        
