import pytest

from domain import Parking
from infrastructure import DisplayPanneauRepositoryMock, BaseDeDonnéesParkingRepositoryMock
from usecase import OuvrirUnParking


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


@pytest.mark.functional
def test_quand_le_parking_est_ouvert_on_notifie_display_panneau_du_nombre_de_places_disponibles_à_afficher():
    # Given
    display_panneau = DisplayPanneauRepositoryMock()

    # When
    OuvrirUnParking(
        display_panneau,
        BaseDeDonnéesParkingRepositoryMock()
    ).exécuter("toto")

    # Then
    assert display_panneau.afficher_avec("500 pl.")
