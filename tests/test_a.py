from dataclasses import dataclass
from abc import ABC

import pytest


class DisplayPanneau(ABC):
    affiché: str = ""

    def afficher(self, message: str) -> None:
        pass


@dataclass
class DisplayPanneauMock(DisplayPanneau):
    message_capturé: str = ""

    def afficher(self, message: str) -> None:
        self.message_capturé = message

    def afficher_avec(self, message_attendu: str) -> bool:
        return message_attendu == self.message_capturé


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


class BaseDeDonnéesParking(ABC):
    def récupérer_parking_par_id(self, id_parking) -> Parking:
        pass


class BaseDeDonnéesParkingMock(BaseDeDonnéesParking):
    def récupérer_parking_par_id(self, id_parking) -> Parking:
        return Parking(etat="fermé", capacité=500)


@dataclass
class OuvrirUnParking:
    ecran: DisplayPanneau
    baseDeDonnéesParking: BaseDeDonnéesParking

    def executer(self):
        parking = self.baseDeDonnéesParking.récupérer_parking_par_id("toto")
        parking.ouvrir()
        nombre_de_places_disponibles = parking.nombre_de_places_disponibles_à_afficher()
        self.ecran.afficher(nombre_de_places_disponibles)


@pytest.mark.fonctionnel
def test_quand_on_ouvre_un_parking_alors_il_affiche_sa_capacité_maximale():
    # Given le parking est fermé à la circulation
    ecran = DisplayPanneauMock()
    capacité_maximale = 200

    # When on ouvre le parking
    Parking(etat="fermé", capacité=capacité_maximale).ouvrir()

    # Then l'écran affiche "200 pl."
    assert ecran.affiché == f"{capacité_maximale} pl."


@pytest.mark.unitaire
def test_quand_le_parking_est_ouvert_et_vide_alors_le_nombre_de_place_disponible_est_200():
    # Given le parking est fermé à la circulation
    parking = Parking(etat="fermé", capacité=200)

    # When on ouvre le parking
    parking.ouvrir()

    # Then le parking a 200 places disponibles
    assert parking.places_disponibles == 200


@pytest.mark.unitaire
def test_quand_le_parking_est_ferme_alors_le_nombre_de_place_disponible_est_0():
    # Given When le parking est fermé à la circulation
    parking = Parking(etat="fermé", capacité=200)

    # Then le parking a 200 places disponibles
    assert parking.places_disponibles == 0


@pytest.mark.unitaire
def test_quand_le_parking_de_500_places_est_ouvert_et_vide_alors_il_y_a_500_places_disponible():
    # Given le parking est fermé à la circulation
    parking = Parking(etat="fermé", capacité=500)

    # When
    parking.ouvrir()

    # Then le parking a 200 places disponibles
    assert parking.places_disponibles == 500


def test_quand_le_parking_est_ouvert_on_notifie_display_panneau_du_nombre_de_places_disponibles_à_afficher():
    # Given un parking
    display_panneau = DisplayPanneauMock()

    # when ouvrir
    OuvrirUnParking(display_panneau, BaseDeDonnéesParkingMock()).executer()

    # then DisplayPanneau a été appelé avec ...
    assert display_panneau.afficher_avec("500 pl.")
