"""Un usecase porte une intention métier, en réaction à un event/command/input utilisateur, ..."""
from dataclasses import dataclass
from typing import List, Type

from parking_plus.cqrs import CommandHandler, Command, Event, EventHandler
from parking_plus.domain import DisplayPanneauRepository, BaseDeDonnéesParkingRepository, LeParkingAÉtéOuvert


@dataclass
class OuvrirUnParkingCommand(Command):
    parking_id: str


@dataclass
class OuvrirUnParking(CommandHandler):
    baseDeDonnéesParking: BaseDeDonnéesParkingRepository

    @staticmethod
    def commande_supportée() -> Type:
        return OuvrirUnParkingCommand

    def handle(self, command: OuvrirUnParkingCommand) -> List[Event]:
        parking = self.baseDeDonnéesParking.récupérer_parking_par(command.parking_id)
        parking.ouvrir()
        self.baseDeDonnéesParking.sauvegarder(parking)
        return parking.récupérer_les_évènements_générés()


@dataclass
class AfficherLeNombreDePlacesÀLOuvertureDuParkingPolicy(EventHandler):
    @staticmethod
    def événement_abonné() -> Type:
        return LeParkingAÉtéOuvert

    displayPanneau: DisplayPanneauRepository

    def handle(self, event: LeParkingAÉtéOuvert):
        self.displayPanneau.afficher(self.nombre_de_places_disponibles_à_afficher(event.nombre_de_places_disponibles))

    @classmethod
    def nombre_de_places_disponibles_à_afficher(cls, places_disponibles):
        return str(places_disponibles) + " pl."
