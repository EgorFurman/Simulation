import math
import time
from abc import ABC, abstractmethod
from random import randint
from typing import Type, TYPE_CHECKING
from entities import Grass, Rock, Tree, Herbivore, Predator

if TYPE_CHECKING:
    from world_map import Map
    from resources import Resource


class Action(ABC):
    """Базовый класс для других действий."""
    @abstractmethod
    def execute(self):
        """Реализует действие в симуляции."""


class GreetingsAction(Action):
    """Класс-действие для приветствия пользователя симуляции."""

    def __init__(self):
        self.__greetings_msg = """
    *************************************************
    *                                               *
    *     Добро пожаловать в 2D симуляцию мира!     *
    *                                               *
    *    Нажмите 'Space', чтобы поставить на паузу. *
    *    Нажмите 'Enter', чтобы продолжить.         *
    *    Нажмите 'Esc', чтобы остановить.           *
    *                                               *
    *          Приятного использования!             *
    *                                               *
    *************************************************
    """

    def execute(self):
        print(self.__greetings_msg)
        time.sleep(8)


class PopulateMapAction(Action):
    """Класс-действие для населения карты симуляции сущностями."""
    slots = ('__world', '__types_multipliers')

    def __init__(self, world: "Map"):
        self.__world = world
        self.__types_multipliers: dict[str: float] = {
            'Grass': 0.2,
            'Rock': 0.09,
            'Tree': 0.09,
            'Herbivore': 0.08,
            'Predator': 0.02
        }

    def execute(self):
        for cls, multiplier in self.__types_multipliers.items():
            count = round(self.__world.rows * self.__world.cols * multiplier)

            while count:
                cell = (randint(0, self.__world.rows-1), randint(0, self.__world.cols-1))

                if self.__world[cell] is None:
                    self.__world[cell] = eval(cls)()
                    count -= 1


class MoveEntitiesAction(Action):
    """Класс-действие для обработки хода сущностей симуляции."""
    __slots__ = ('__world',)

    def __init__(self, world: "Map"):
        self.__world = world

    def execute(self):
        entities = tuple(entity for _, entity in self.__world)

        for entity in entities:
            entity.make_move()


class CleanMapAction(Action):
    """Класс-действие для отчистки симуляции от "мертвых" сущностей."""
    __slots__ = ('__world',)

    def __init__(self, world: "Map"):
        self.__world = world

    def execute(self):
        must_be_deleted = tuple(cell for cell, entity in self.__world if not entity.is_alive)

        for cell in must_be_deleted:
            del self.__world[cell]


class RestoreResourceAction(Action):
    """Класс-действие для восполнения ресурсов симуляции(добавления на карту новых)."""
    def __init__(self, world: "Map", resource_type: Type["Resource"], resource_coefficient: float):
        self.__world = world
        self.__resource_type = resource_type
        self.__resource_coefficient = resource_coefficient

    def execute(self):
        for _ in range(math.ceil(self.__world.rows*self.__world.cols*self.__resource_coefficient)):
            cell = (randint(0, self.__world.rows - 1), randint(0, self.__world.cols - 1))

            if self.__world[cell] is None:
                self.__world[cell] = self.__resource_type()

