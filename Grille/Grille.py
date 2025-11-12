import pygame
import sys
import random

# --- Constantes ---
TAILLE_CASE = 50          # chaque case fait 50x50 pixels
NB_CASES = 10             # grille 10x10
LARGEUR = TAILLE_CASE * NB_CASES
HAUTEUR = TAILLE_CASE * NB_CASES

COULEUR_FOND = (107, 214, 136)
COULEUR_LIGNE = (52, 105, 66)
COULEUR_ROND = (0, 0, 0)

NB_RONDS = 18             # nombre de ronds à placer aléatoirement
RAYON_ROND = TAILLE_CASE // 3  # rayon visuel des ronds

def dessiner_grille(fenetre):
    """Dessine une grille 10x10 sur la fenêtre pygame."""
    for x in range(0, LARGEUR + 1, TAILLE_CASE):
        pygame.draw.line(fenetre, COULEUR_LIGNE, (x, 0), (x, HAUTEUR))
    for y in range(0, HAUTEUR + 1, TAILLE_CASE):
        pygame.draw.line(fenetre, COULEUR_LIGNE, (0, y), (LARGEUR, y))

def generer_positions_ronds(nb):
    """
    Retourne une liste de centres (x, y) pour nb ronds, placés
    aléatoirement dans des cases (sans doublons de case).
    """
    nb_max = NB_CASES * NB_CASES
    nb = min(nb, nb_max)

    # Liste de toutes les cases possibles (col, row)
    toutes_les_cases = [(col, row) for col in range(NB_CASES) for row in range(NB_CASES)]
    # On échantillonne sans doublon
    cases_choisies = random.sample(toutes_les_cases, nb)

    centres = []
    for col, row in cases_choisies:
        cx = col * TAILLE_CASE + TAILLE_CASE // 2
        cy = row * TAILLE_CASE + TAILLE_CASE // 2
        centres.append((cx, cy))
    return centres

def dessiner_ronds(fenetre, centres):
    """Dessine les ronds noirs aux positions données (centres en pixels)."""
    for (cx, cy) in centres:
        pygame.draw.circle(fenetre, COULEUR_ROND, (cx, cy), RAYON_ROND)

def main():
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Grille 10x10 - Ronds aléatoires")

    clock = pygame.time.Clock()

    # Génère les ronds une fois au démarrage
    centres_ronds = generer_positions_ronds(NB_RONDS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Efface l'écran
        fenetre.fill(COULEUR_FOND)

        # Dessine la grille
        dessiner_grille(fenetre)

        # Dessine les ronds
        dessiner_ronds(fenetre, centres_ronds)

        # Met à jour l'affichage
        pygame.display.flip()
        clock.tick(30)  # limite à 30 fps

if __name__ == "__main__":
    main()
