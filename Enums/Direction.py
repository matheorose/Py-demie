from enum import Enum

class Direction(Enum):
    IMMOBILE      = (0, 0)
    GAUCHE        = (-1, 0)
    DROITE        = (1, 0)
    HAUT          = (0, -1)
    BAS           = (0, 1)
    HAUT_GAUCHE   = (-1, -1)
    HAUT_DROITE   = (1, -1)
    BAS_GAUCHE    = (-1, 1)
    BAS_DROITE    = (1, 1)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]
