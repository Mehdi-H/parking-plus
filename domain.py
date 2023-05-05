"""Objets métiers et interfaces"""

from abc import ABC
from dataclasses import dataclass


@dataclass
class Parking:
    etat: str
    capacité: int

    def ouvrir(self):
        self.etat = "ouvert"

    @property
    def places_disponibles(self):
        if self.etat == "fermé":
            return 0
        return self.capacité

    def nombre_de_places_disponibles_à_afficher(self):
        return str(self.places_disponibles) + " pl."


class DisplayPanneauRepository(ABC):
    """🔎 DisplayPanneau est le nom du partenaire !"""
    affiché: str = ""

    def afficher(self, message: str) -> None:
        pass


class BaseDeDonnéesParkingRepository(ABC):
    def récupérer_parking_par(self, id_parking) -> Parking:
        pass
