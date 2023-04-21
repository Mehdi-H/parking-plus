from dataclasses import dataclass


@dataclass
class Ecran:
    affiché: str = ""


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


def test_fonctionnel():
    # Given le parking est fermé à la circulation
    ecran = Ecran()

    # When on ouvre le parking
    Parking(etat="fermé").ouvrir()

    # Then l'écran affiche "200 pl."
    assert ecran.affiché == "200 pl."


def test_quand_le_parking_est_ouvert_et_vide_alors_le_nombre_de_place_disponible_est_200():
    # Given le parking est fermé à la circulation
    parking = Parking(etat="fermé", capacité=200)

    # When on ouvre le parking
    parking.ouvrir()

    # Then le parking a 200 places disponibles
    assert parking.places_disponibles == 200

def test_quand_le_parking_est_ferme():
    # Given When le parking est fermé à la circulation
    parking = Parking(etat="fermé", capacité=200)

    # Then le parking a 200 places disponibles
    assert parking.places_disponibles == 0
def test_quand_le_parking_de_500_places_est_ouvert_et_vide_alors_il_y_a_500_places_disponible():
    # Given le parking est fermé à la circulation
    parking = Parking(etat="fermé", capacité=500)

    # When
    parking.ouvrir()

    # Then le parking a 200 places disponibles
    assert parking.places_disponibles == 500
