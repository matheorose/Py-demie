import random
from dataclasses import dataclass
from .enums import Sex

@dataclass
class Humain:
    age: int = 0
    duree_vie: int = 80
    proba_procreer: float = 0.1
    vivant: bool = True
    sexe: Sex | None = None  # ← DOIT être Sex.MALE ou Sex.FEMALE

    def vieillir(self) -> None:
        self.age += 1
        if self.age >= self.duree_vie:
            self.vivant = False

    def peut_procreer(self) -> bool:
        return self.vivant and (random.random() < max(0.0, min(1.0, self.proba_procreer)))
