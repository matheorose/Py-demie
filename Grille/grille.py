import pygame
import sys

# --- Constantes ---
TAILLE_CASE = 50          # chaque case fait 50x50 pixels
NB_CASES = 10             # grille 10x10
LARGEUR = TAILLE_CASE * NB_CASES
HAUTEUR = TAILLE_CASE * NB_CASES

COULEUR_FOND = (255, 255, 255)   # blanc
COULEUR_LIGNE = (0, 0, 0)        # noir

def dessiner_grille(fenetre):
    """Dessine une grille 10x10 sur la fenêtre pygame."""
    for x in range(0, LARGEUR, TAILLE_CASE):
        pygame.draw.line(fenetre, COULEUR_LIGNE, (x, 0), (x, HAUTEUR))
    for y in range(0, HAUTEUR, TAILLE_CASE):
        pygame.draw.line(fenetre, COULEUR_LIGNE, (0, y), (LARGEUR, y))


def main():
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Grille 10x10")

    clock = pygame.time.Clock()

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Efface l'écran
        fenetre.fill(COULEUR_FOND)

        # Dessine la grille
        dessiner_grille(fenetre)

        # Met à jour l'affichage
        pygame.display.flip()
        clock.tick(30)  # limite à 30 fps


if __name__ == "__main__":
    main()
