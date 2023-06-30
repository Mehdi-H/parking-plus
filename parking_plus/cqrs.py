import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type


class Event:
    pass


class Command(ABC):
    pass


class CommandHandler(ABC):
    def handle(self, command: Command) -> List[Event]:
        pass

    @staticmethod
    @abstractmethod
    def commande_supportée() -> Type:
        pass


class CommandBus(ABC):
    @abstractmethod
    def dispatch(self, command: Command) -> List[Event]:
        pass


@dataclass
class CommandDispatcher(CommandBus):
    command_handlers: List[CommandHandler]

    @classmethod
    def construire_le_bus_depuis_une_list_de_commands_handler(cls, command_handlers: List[
        CommandHandler]) -> "CommandDispatcher":
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


@dataclass
class CommandLoggingMiddleware(CommandBus):
    next_middleware: CommandBus

    def dispatch(self, command: Command) -> List[Event]:
        logger = logging.getLogger("command_logging_middleware")
        print(f"Une commande de type {command} est en cours de traitement")
        events = self.next_middleware.dispatch(command)
        print(
            f"Une commande de type {command} a été traitée et a produit les évènements suivants : {events}")
        return events


class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: Event):
        pass

    @staticmethod
    @abstractmethod
    def événement_abonné() -> Type:
        pass


class EventBus(ABC):
    @abstractmethod
    def dispatch(self, event: Event):
        pass


@dataclass
class EventDispatcher(EventBus):
    event_handlers: List[EventHandler]

    def dispatch(self, event: Event):
        for event_handler in self.event_handlers:
            if event_handler.événement_abonné() == event.__class__:
                event_handler.handle(event)

    @classmethod
    def construire_le_bus_depuis_une_list_de_event_handler(cls,
                                                           event_handlers: List[EventHandler]) -> "EventDispatcher":
        return EventDispatcher(event_handlers)


class EventBusError(Exception):
    pass


@dataclass
class CommandEventsDispatcher(CommandBus):
    next_command_bus: CommandBus
    event_bus: EventBus

    def dispatch(self, command: Command) -> List[Event]:
        events = self.next_command_bus.dispatch(command)
        for event in events:
            self.event_bus.dispatch(event)
        return events
