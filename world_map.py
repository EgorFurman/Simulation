from typing import Union, Optional
from entities import Entity


class MapAccessError(Exception):
    """Базовый класс для других исключений."""
    pass


class InvalidKeyTypeError(MapAccessError):
    """Возбуждается, когда ключ не является кортежем."""
    def __init__(self, key):
        self.message = f"Неверный формат ключа: {key}. Ключ должен быть кортежем."
        super().__init__(self.message)


class InvalidKeyFormatError(MapAccessError):
    """Возбуждается, когда ключ не является кортежем из двух целых чисел."""
    def __init__(self, key):
        self.message = f"Неверный формат ключа: {key}. Ключ должен быть кортежем из двух чисел."
        super().__init__(self.message)


class InvalidIndexError(MapAccessError):
    """Возбуждается, когда переданы индексы выходящие за диапазон допустимых значений карты."""
    def __init__(self, key, rows, cols):
        self.message = f"Неверные индексы: {key}. Допустимые индексы должны находиться в пределах (0, 0) и ({rows-1}, {cols-1})"
        super().__init__(self.message)


class InvalidKeyLengthError(MapAccessError):
    """Возбуждается, когда ключ состоит более чем из двух элементов."""
    def __init__(self, key):
        self.message = f"Неверная длина ключа: {key}. Ключ должен состоять из двух элементов."
        super().__init__(self.message)


class NotEmptyCellAssignError(MapAccessError):
    """Возбуждается при попытке присвоить значение непустой клетке."""
    def __init__(self, key):
        self.message = f"Ошибка при попытке присвоить значение ячейке {key}. Указанная клетка уже занята."
        super().__init__(self.message)


class Map:
    """Класс представляющий собой коллекцию для хранения сущностей симуляции и их расположения."""
    __slots__ = ('__rows', '__cols', '__map')

    def __init__(self, rows: int = 10, cols: int = 10):
        self.__rows = rows
        self.__cols = cols

        self.__map: dict[tuple[int, int], ...] = {}

    def __setitem__(self, key: tuple[int, int], value: Entity) -> None:
        self.__validate_key(key=key)

        if self.__map.get(key, None):
            raise NotEmptyCellAssignError(key=key)

        self.__validate_value(value=value)

        value.cell, value.world_map = key, self
        self.__map[key] = value

    def __getitem__(self, item: tuple[int, int]) -> Optional[Entity]:
        self.__validate_key(key=item)
        return self.__map.get(item, None)

    def __delitem__(self, key: tuple[int, int]) -> None:
        self.__validate_key(key=key)
        self.__map.pop(key, None)

    def __iter__(self):
        for cell, value in self.__map.items():
            yield cell, value

    def get_neighbors(self, cell: tuple[int, int]) -> Union[set[tuple[int, int], ...], set]:
        res = set()

        x, y = cell

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                res.add((new_x, new_y))

        return res

    def move_entity(self, from_cell: tuple[int, int], to_cell: tuple[int, int]):
        entity = self[from_cell]

        del self[from_cell]
        self[to_cell] = entity

    def __validate_key(self, key: tuple[int, int]) -> None:
        if not isinstance(key, tuple):
            raise InvalidKeyTypeError(key=key)
        if len(key) != 2:
            raise InvalidKeyLengthError(key=key)
        if not all(type(index) is int for index in key):
            raise InvalidKeyLengthError(key=key)
        x, y = key
        if not (0 <= x < self.rows and 0 <= y < self.cols):
            raise InvalidIndexError(key=key, rows=self.rows, cols=self.cols)

    @staticmethod
    def __validate_value(value) -> None:
        if not isinstance(value, Entity):
            raise TypeError("Клетки карты должны быть представлены объектами одного из подклассов класса Entity.")

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols
