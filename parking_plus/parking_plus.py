from parking_plus.cqrs import CommandBus, CommandDispatcher, CommandLoggingMiddleware, CommandEventsDispatcher, \
    EventDispatcher
from parking_plus.domain import DisplayPanneauRepository, Parking
from parking_plus.infrastructure import BaseDeDonnéesParkingRepositoryInMemory
from parking_plus.usecase import OuvrirUnParking, AfficherLeNombreDePlacesÀLOuvertureDuParkingPolicy


def créer_parking_plus_bus(display_panneau: DisplayPanneauRepository) -> CommandBus:
    base_de_données_parking = BaseDeDonnéesParkingRepositoryInMemory(Parking("fermé", 500, [], 1))
    command_handler = OuvrirUnParking(base_de_données_parking)
    command_dispatcher = CommandDispatcher.construire_le_bus_depuis_une_list_de_commands_handler([command_handler])
    logging_middleware = CommandLoggingMiddleware(command_dispatcher)
    event_dispatcher = EventDispatcher([AfficherLeNombreDePlacesÀLOuvertureDuParkingPolicy(display_panneau)])
    return CommandEventsDispatcher(logging_middleware, event_dispatcher)
