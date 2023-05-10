from parking_plus.cqrs import CommandBus, CommandDispatcher, CommandLoggingMiddleware
from parking_plus.domain import DisplayPanneauRepository
from parking_plus.infrastructure import BaseDeDonnéesParkingRepositoryInMemory
from parking_plus.usecase import OuvrirUnParking


def créer_parking_plus_bus(display_panneau: DisplayPanneauRepository) -> CommandBus:
    base_de_données_parking = BaseDeDonnéesParkingRepositoryInMemory()
    command_handler = OuvrirUnParking(display_panneau, base_de_données_parking)
    command_dispatcher = CommandDispatcher.construire_le_bus_depuis_une_list_de_commands_handler([command_handler])
    return CommandLoggingMiddleware(command_dispatcher)
