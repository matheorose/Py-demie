# Models/world.py
import random
from typing import Iterable, List, Tuple
from .Humain import Humain
from Enums.Sex import Sex
from Enums.Direction import Direction 

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
        print("place_at")
        
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
        self.humans.append(humain)
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
    
    
    
    
    def _wrap(self, x: int, y: int) -> Coord:
        """Applique l'effet torus : dépassement d'un bord -> réapparaît de l'autre côté."""
        return (x % self.largeur, y % self.hauteur)
    
    
    # ---------- déplacement principal ----------
    def deplacer(self, person: Humain, direction: Direction) -> bool:
        """
        Déplace 'person' d'une case selon 'direction' (torus).
        - Si la case est occupée, essaie d'autres directions au hasard.
        - Si toutes les cases voisines sont occupées, la personne ne bouge pas.
        - Retourne True si déplacement effectué, False sinon.
        """
        # 0) vérifications de base
        if not person.vivant:
            print("la persone n'est pas vivante")
            return False
        
        x, y = person.coordoneeX, person.coordoneeY
        if x is None or y is None or not self.in_bounds(x, y) or self.grille[y][x] is not person:
            # pas sur la grille / coords incohérentes
            print("les informations d'entrées sont incohérentes")
            return False

        # 1) liste des directions candidates :
        #    - d'abord la direction demandée
        #    - puis les autres directions (aléatoires)
        all_dirs = list(Direction)
        # on exclut l'immobilité si elle existe (dx=dy=0)
        all_dirs = [d for d in all_dirs if getattr(d, "dx", d.value[0]) != 0 or getattr(d, "dy", d.value[1]) != 0]

        # place la direction demandée en tête
        others = [d for d in all_dirs if d != direction]
        random.shuffle(others)
        candidates = [direction] + others

        # 2) on essaie chaque direction candidate jusqu'à trouver une case libre
        for d in candidates:
            dx = getattr(d, "dx", d.value[0])
            dy = getattr(d, "dy", d.value[1])
            nx, ny = self._wrap(x + dx, y + dy)
            if self.is_empty(nx, ny):
                # déplacer
                self.grille[y][x] = None
                self.grille[ny][nx] = person
                person.coordoneeX = nx
                person.coordoneeY = ny
                return True

        # 3) aucune case voisine libre -> on ne bouge pas
        print("Aucune case voisine libre -> on ne bouge pas")
        return False
    
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
        

    # ---------- tick (exemple minimal) ----------
    def tick(self) -> None:
        """
        Exemple minimal: chaque humain tente de bouger d'1 case
        dans une direction aléatoire.
        (Tu pourras ensuite y ajouter vieillissement, rencontres, procréation…)
        """
        humains = list(self.each_human())
        random.shuffle(humains)
        
        for h in self.humans:
            # vieillir avant ou après selon ta logique
            h.vieillir()
            if not h.vivant:
                # libère la case si mort
                x, y = h.coordoneeX, h.coordoneeY
                self.grille[y][x] = None
                print("L'humain en x: " + x + ", y: " + y + " est mort")
                continue
            
            # tentative de déplacement
            dir_rand = random.choice([
                d for d in Direction
                if (getattr(d, "dx", d.value[0]) != 0 or getattr(d, "dy", d.value[1]) != 0)
            ])
            self.deplacer(h, dir_rand)
