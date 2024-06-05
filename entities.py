from __future__ import annotations
from abc import ABC, abstractmethod
from random import choice
from typing import Optional, Union, TYPE_CHECKING
from resources import Resource
from bfs_search import bfs

if TYPE_CHECKING:
    from world_map import Map


class Entity(ABC):
    """Базовый абстрактный класс для остальных сущностей симуляции."""
    def __init__(self, cell: Optional[tuple[int, int]] = None, world_map: Optional[Map] = None):
        self.__cell = cell
        self.__world_map = world_map
        self.__is_alive = True

    @property
    def cell(self):
        return self.__cell

    @cell.setter
    def cell(self, cell):
        self.__cell = cell

    @property
    def world_map(self):
        return self.__world_map

    @world_map.setter
    def world_map(self, world_map):
        self.__world_map = world_map

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("Атрибут is_alive должен быть представлен логическим значением(True/False).")
        self.__is_alive = value

    @abstractmethod
    def make_move(self):
        """Определяет поведение существа во время выполнения симуляции."""

    @abstractmethod
    def render(self):
        """Отрисовывает объект."""


class Terrain(Entity, ABC):
    """Базовый абстрактный класс для объектов-окружения симуляции."""
    pass


class Grass(Terrain, Resource):
    def make_move(self):
        pass

    def render(self):
        return '🌾'


class Rock(Terrain):
    def make_move(self):
        pass

    def render(self):
        return '⛰️'


class Tree(Terrain):
    def make_move(self):
        pass

    def render(self):
        return '🌱'


class Creature(Entity, ABC):
    """Базовый абстрактный класс для объектов-существ симуляции."""
    def __init__(
        self, cell: Optional[tuple[int, int]], world_map: Optional[Map], health: int, speed: int, food_type: type[Resource]
    ):
        super().__init__(cell=cell, world_map=world_map)
        self.__health = health
        self.__speed = speed
        self.__food_type = food_type

    def __get_to_resource_path(self) -> Union[list[tuple[int, int], ...], list]:
        return bfs(cell=self.cell, goal=self.food_type, world_map=self.world_map)

    def __get_target_cell(self, path: Union[list[tuple[int, int], ...], list]) -> tuple[int, int]:
        if len(path) <= self.speed:
            return path[-1]
        return path[self.speed-1]

    def _try_move_to_resource(self) -> bool:
        path = self.__get_to_resource_path()
        if path:
            self.world_map.move_entity(from_cell=self.cell, to_cell=self.__get_target_cell(path[:-1]))
            return True
        return False

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, health: int) -> None:
        if health <= 0:
            self.is_alive = False
            return
        self.__health = health

    @property
    def speed(self):
        return self.__speed

    @property
    def food_type(self):
        return self.__food_type


class Herbivore(Creature, Resource):
    HEALTH_RANGE = range(2, 6)
    SPEED_RANGE = range(3, 8)

    def __init__(
        self, cell: Optional[tuple[int, int]] = None, world_map: Optional["Map"] = None,
        health: int = choice(HEALTH_RANGE), speed: int = choice(SPEED_RANGE), food_type: type[Resource] = Grass,
    ):

        super().__init__(cell=cell, world_map=world_map, health=health, speed=speed, food_type=food_type)

    def render(self):
        return '🐇'

    def make_move(self) -> None:
        if self.is_alive:
            if self._try_absorb_resource():
                return
            if self._try_move_to_resource():
                return

    def _try_absorb_resource(self) -> bool:
        neighbors = self.world_map.get_neighbors(cell=self.cell)

        for neighbor in neighbors:
            if isinstance(self.world_map[neighbor], self.food_type):
                self.__eat(neighbor)
                return True
        return False

    def __eat(self, target: tuple[int, int]) -> None:
        self.world_map[target].is_alive = False


class Predator(Creature):
    HEALTH_RANGE = range(4, 9)
    SPEED_RANGE = range(5, 12)
    ATTACK_POWER_RANGE = range(4, 7)

    def __init__(
        self, cell: Optional[tuple[int, int]] = None, world_map: Optional["Map"] = None,
        health: int = choice(HEALTH_RANGE), speed: int = choice(SPEED_RANGE),
        food_type: type[Resource] = Herbivore, attack_power: int = choice(ATTACK_POWER_RANGE)
    ):

        super().__init__(cell, world_map, health, speed, food_type)
        self.__attack_power = attack_power

    def render(self):
        return '🐺'

    def make_move(self) -> None:
        if self.is_alive:
            if self._try_attack_herbivore():
                return
            if self._try_move_to_resource():
                return

    def _try_attack_herbivore(self):
        neighbors = self.world_map.get_neighbors(cell=self.cell)

        for neighbor in neighbors:
            if isinstance(self.world_map[neighbor], self.food_type):
                self.__attack(neighbor)
                return True
        return False

    def __attack(self, target: tuple[int, int]) -> None:
        self.world_map[target].health -= self.__attack_power

    @property
    def attack_power(self):
        return self.__attack_power
