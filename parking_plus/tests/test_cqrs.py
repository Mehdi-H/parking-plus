from dataclasses import dataclass
from typing import Optional, List, Type

import pytest

from parking_plus.cqrs import Command, CommandHandler, Event, CommandDispatcher, CommandBusError


@dataclass
class UneCommande(Command):
    un_parametre: str


@dataclass
class UneAutreCommande(Command):
    pass


@dataclass
class UnEvent(Event):
    id: str


@dataclass
class UnCommandHandler(CommandHandler):
    commande_dispatchee: Optional[Command] = None

    def handle(self, command: Command) -> List[Event]:
        self.commande_dispatchee = command
        return [UnEvent('1234')]

    @staticmethod
    def commande_supportée() -> UneCommande:
        return UneCommande


@dataclass
class UnAutreCommandHandler(CommandHandler):
    commande_dispatchee: Optional[Command] = None

    def handle(self, command: Command) -> List[Event]:
        self.commande_dispatchee = command
        return [UnEvent('5678')]

    @staticmethod
    def commande_supportée() -> Type:
        return UneAutreCommande


@pytest.mark.unitaire
def test_la_commande_doit_etre_dispatch_au_bon_handler():
    # Given
    le_command_handler_qui_traite_la_commande = UnCommandHandler()
    l_autre_command_handler_qui_traite_rien = UnAutreCommandHandler()
    command_handlers = [le_command_handler_qui_traite_la_commande, l_autre_command_handler_qui_traite_rien]
    command_bus = CommandDispatcher.construire_le_bus_depuis_une_list_de_commands_handler(command_handlers)
    une_commande = UneCommande('un param')

    # When
    command_bus.dispatch(une_commande)

    # Then
    assert le_command_handler_qui_traite_la_commande.commande_dispatchee == une_commande
    assert l_autre_command_handler_qui_traite_rien.commande_dispatchee is None


@pytest.mark.unitaire
def test_quand_plusieurs_commands_handler_supportent_la_même_command_alors_une_exception_est_levée_par_le_bus():
    # Given
    un_command_handler = UnCommandHandler()
    un_autre_même_command_handler = UnCommandHandler()
    command_handlers = [un_command_handler, un_autre_même_command_handler]

    # When
    with pytest.raises(CommandBusError) as erreur_attendue:
        CommandDispatcher.construire_le_bus_depuis_une_list_de_commands_handler(command_handlers)

    # Then
    assert str(erreur_attendue.value) == "Deux command handlers supportent le même type de commande"
