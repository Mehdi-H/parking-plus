"""Un usecase porte une intention métier, en réaction à un event/command/input utilisateur, ..."""
from dataclasses import dataclass
from typing import List, Type

from parking_plus.cqrs import CommandHandler, Command, Event
from parking_plus.domain import DisplayPanneauRepository, BaseDeDonnéesParkingRepository


@dataclass
class OuvrirUnParkingCommand(Command):
    parking_id: str


@dataclass
class OuvrirUnParking(CommandHandler):
    displayPanneau: DisplayPanneauRepository
    baseDeDonnéesParking: BaseDeDonnéesParkingRepository

    @staticmethod
    def commande_supportée() -> Type:
        return OuvrirUnParkingCommand

    def handle(self, command: OuvrirUnParkingCommand) -> List[Event]:
        parking = self.baseDeDonnéesParking.récupérer_parking_par(command.parking_id)
        parking.ouvrir()
        nombre_de_places_disponibles = parking.nombre_de_places_disponibles_à_afficher()
        self.displayPanneau.afficher(nombre_de_places_disponibles)
        return []
