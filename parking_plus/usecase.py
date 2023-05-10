"""Un usecase porte une intention métier, en réaction à un event/command/input utilisateur, ..."""
from dataclasses import dataclass

from parking_plus.domain import DisplayPanneauRepository, BaseDeDonnéesParkingRepository


@dataclass
class OuvrirUnParking:
    displayPanneau: DisplayPanneauRepository
    baseDeDonnéesParking: BaseDeDonnéesParkingRepository

    def exécuter(self, parking_id: str) -> None:
        parking = self.baseDeDonnéesParking.récupérer_parking_par(parking_id)
        parking.ouvrir()
        nombre_de_places_disponibles = parking.nombre_de_places_disponibles_à_afficher()
        self.displayPanneau.afficher(nombre_de_places_disponibles)
