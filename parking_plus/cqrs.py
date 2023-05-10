from abc import ABC
from dataclasses import dataclass
from typing import List


class Event:
    pass


class Command(ABC):
    pass


class CommandHandler(ABC):
    def handle(self, command: Command) -> List[Event]:
        pass

    @staticmethod
    def commande_supportée() -> Command:
        pass


class CommandBus(ABC):
    def dispatch(self, command: Command) -> List[Event]:
        pass


class CommandDispatcher:
    pass


@dataclass
class CommandDispatcher(CommandBus):
    command_handlers: List[CommandHandler]

    @classmethod
    def construire_le_bus_depuis_une_list_de_commands_handler(cls, command_handlers: List[
        CommandHandler]) -> CommandDispatcher:
        commandes_supportées = set([command_handler.commande_supportée() for command_handler in command_handlers])
        if len(commandes_supportées) != len(command_handlers):
            raise CommandBusError("Deux command handlers supportent le même type de commande")

        return CommandDispatcher(command_handlers)

    def dispatch(self, command: Command) -> List[Event]:
        for command_handler in self.command_handlers:
            if command_handler.commande_supportée() == command.__class__:
                return command_handler.handle(command)


class CommandBusError(Exception):
    pass
