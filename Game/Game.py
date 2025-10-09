# Models/game.py
import random
from typing import Optional
from Models.World import World

class Game:
    def __init__(self,
                 width: int,
                 height: int,
                 nb_humains: int,
                 seed: Optional[int] = 42):
        """
        Initialise la partie :
        - crée un World(width x height)
        - remplit la grille avec nb_humains
        - fixe une seed pour rendre les tests reproductibles
        """
        if seed is not None:
            random.seed(seed)

        self.world = World(width, height)
        places = self.world.remplir_grille(nb_humains, male_ratio=0.5)
        if places < nb_humains:
            print(f"⚠️ Seulement {places}/{nb_humains} humains ont pu être placés.")

    def run(self, tours: int = 4, afficher: bool = True) -> None:
        """Lance la simulation pendant `tours` ticks."""
        if afficher:
            print("=== ÉTAT INITIAL ===")
            print(self.world._to_string())
            print(f"Vivants: {sum(1 for _ in self.world.each_human())}\n")

        for t in range(1, tours + 1):

            if afficher:
                print(f"\n\n=== TOUR {t} ===")
                self.world.tick()
                print(self.world._to_string())
                vivants = sum(1 for _ in self.world.each_human())
                print(f"Vivants: {vivants}\n")


if __name__ == "__main__":
    # Petit test rapide
    game = Game(width=7, height=7, nb_humains=15, seed=125)
    game.run(tours=60, afficher=True)
