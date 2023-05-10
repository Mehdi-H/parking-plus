from abc import ABC
from dataclasses import dataclass
from typing import List


class Command:
    pass


class Event:
    pass


Events = List[Event]


class CommandHandler(ABC):
    def handle(self, command: Command) -> Events:
        pass

    def commande_associee(self) -> str:
        return 'TODO'


class CommandBus(ABC):
    def dispatch(self, command: Command) -> Events:
        pass


@dataclass
class CommandDispatcher(CommandBus):
    command_handlers: List[CommandHandler]

    def dispatch(self, command: Command) -> Events:
        return None