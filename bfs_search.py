
from queue import Queue
from typing import Union, Type, TYPE_CHECKING


if TYPE_CHECKING:
    from resources import Resource
    from world_map import Map


def bfs(cell: tuple[int, int], goal: Type["Resource"], world_map: "Map") -> Union[list[tuple[int, int], ...], list]:
    visited = set()

    queue = Queue()
    queue.put((cell, []))

    while not queue.empty():
        cell, path = queue.get()

        if isinstance(world_map[cell], goal):
            return path

        for neighbor_cell in world_map.get_neighbors(cell):
            if neighbor_cell not in visited and (world_map[neighbor_cell] is None or isinstance(world_map[neighbor_cell], goal)):
                visited.add(neighbor_cell)
                new_path = path + [neighbor_cell]

                queue.put((neighbor_cell, new_path))

    return []
