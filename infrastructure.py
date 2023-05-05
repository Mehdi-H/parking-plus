"""Détails d'implémentation qu'on ne voit pas voir dans le domain"""

from dataclasses import dataclass

from domain import DisplayPanneauRepository, BaseDeDonnéesParkingRepository, Parking


@dataclass
class DisplayPanneauRepositoryMock(DisplayPanneauRepository):
    message_capturé: str = ""

    def afficher(self, message: str) -> None:
        self.message_capturé = message

    def afficher_avec(self, message_attendu: str) -> bool:
        return message_attendu == self.message_capturé


class BaseDeDonnéesParkingRepositoryMock(BaseDeDonnéesParkingRepository):
    def récupérer_parking_par(self, id_parking) -> Parking:
        return Parking(etat="fermé", capacité=500)
