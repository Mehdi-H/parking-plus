"""Objets métiers et interfaces"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from parking_plus.cqrs import Event


@dataclass
class Parking:
    état: str
    capacité: int
    événements_générés: List[Event]
    id: int

    @classmethod
    def reconstituer(cls, état: str, capacité: int, id: int):
        return Parking(état, capacité, [], id)

    def ouvrir(self):
        self.état = "ouvert"
        self.événements_générés.append(LeParkingAÉtéOuvert(self.id, self.places_disponibles))

    @property
    def places_disponibles(self):
        if self.état == "fermé":
            return 0
        return self.capacité

    def récupérer_les_évènements_générés(self):
        return self.événements_générés


class DisplayPanneauRepository(ABC):
    """🔎 DisplayPanneau est le nom du partenaire !"""
    affiché: str = ""

    def afficher(self, message: str) -> None:
        pass


class BaseDeDonnéesParkingRepository(ABC):
    def récupérer_parking_par(self, id_parking) -> Parking:
        pass

    @abstractmethod
    def sauvegarder(self, parking: Parking):
        pass


@dataclass
class LeParkingAÉtéOuvert(Event):
    id: int
    nombre_de_places_disponibles: int
