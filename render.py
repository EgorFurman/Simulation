from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world_map import Map


class WorldMapRenderer:
    __slots__ = ('__world_map', )

    def __init__(self, world_map: "Map"):
        self.__world_map = world_map

    def render(self):
        print("┌―-―┬" + "―-―┬" * (self.__world_map.cols-2) + "―-―┐")
        for i in range(self.__world_map.rows):
            print("│ " + " │ ".join(f"{self.render_cell((i, j)):^{1}}" for j in range(self.__world_map.cols)) + " │")
            if i < self.__world_map.rows - 1:
                print("├―-―│" + "―-―│" * (self.__world_map.cols - 2) + "―-―┤")
        print("└―-―┴" + "―-―┴" * (self.__world_map.cols - 2) + "―-―┘")

    def render_cell(self, cell: tuple[int, int]) -> str:
        if self.__world_map[cell] is None:
            return '⬛'
        else:
            return self.__world_map[cell].render()
