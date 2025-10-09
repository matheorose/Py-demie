import random
from dataclasses import dataclass
from Enums.Sex import Sex

@dataclass
class Humain:
    age: int = 1
    duree_vie: int = 80
    proba_procreer: float = 0.3
    vivant: bool = True
    sexe: Sex | None = None  # ← DOIT être Sex.MALE ou Sex.FEMALE

    coordoneeX: int | None = None     
    coordoneeY: int | None = None 

    def vieillir(self) -> None:
        self.age += 1
        if self.age >= self.duree_vie:
            self.vivant = False

    def peut_procreer(self) -> bool:
        if ((self.age <18) and (self.age > 60)): 
            return False
        
        return self.vivant and (random.random() < max(0.0, min(1.0, self.proba_procreer)))
    
    
