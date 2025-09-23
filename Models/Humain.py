import random
from dataclasses import dataclass
from .enums import Sex

@dataclass
class Humain:
    age: int = 0
    duree_vie: int = 80
    proba_procreer: float = 0.1
    vivant: bool = True
    sexe: Sex | None = None


