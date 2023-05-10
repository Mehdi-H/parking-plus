from dataclasses import dataclass

import pytest

from cqrs import Command, Events, CommandHandler, Event, CommandDispatcher


@dataclass
class UneCommande:
    un_parametre: str


@dataclass
class UnEvent(Event):
    id: str


@dataclass
class UnCommandHandler(CommandHandler):
    commande_dispatchee: Command

    def handle(self, command: Command) -> Events:
        self.commande_dispatchee = command
        return [UnEvent('1234')]


@dataclass
class UnAutreCommandHandler(CommandHandler):
    commande_dispatchee: Command

    def handle(self, command: Command) -> Events:
        self.commande_dispatchee = command
        return [UnEvent('5678')]

    def commande_associee(self) -> str:
        return ''


@pytest.mark.unitaire
def test_la_commande_doit_etre_dispatch_au_bon_handler():
    # Given
    un_command_handler = UnCommandHandler()
    un_autre_command_handler = UnAutreCommandHandler()
    command_handlers = [un_command_handler, un_autre_command_handler]
    command_bus = CommandDispatcher(command_handlers)
    une_commande = UneCommande('un param')

    # When
    command_bus.dispatch(une_commande)

    # Then
    assert un_command_handler.commande_dispatchee == une_commande

