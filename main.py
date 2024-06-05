import threading
import time
import keyboard
import actions
from entities import Grass, Herbivore
from world_map import Map
from render import WorldMapRenderer


class Simulation:
    def __init__(self, rows: int = 5, cols: int = 12):
        self.__paused = False
        self.__running = False
        self.__step_counter = 0

        self.world = Map(rows, cols)
        self.renderer = WorldMapRenderer(world_map=self.world)

        self.init_actions = (
            actions.GreetingsAction(),
            actions.PopulateMapAction(world=self.world),
        )

        self.turn_actions = (
            actions.MoveEntitiesAction(world=self.world),
            actions.CleanMapAction(world=self.world),
            actions.RestoreResourceAction(world=self.world, resource_type=Grass, resource_coefficient=0.04),
            actions.RestoreResourceAction(world=self.world, resource_type=Herbivore, resource_coefficient=0.01)
        )

    def next_turn(self) -> None:
        for action in self.turn_actions:
            action.execute()
            self.__step_counter += 1
        self.renderer.render()
        time.sleep(2)

    def run_simulation(self) -> None:
        while self.__running:
            if self.__paused:
                continue
            self.next_turn()

    def start_simulation(self) -> None:
        if not self.__running:
            self.initialize_simulation()
            self.__running = True

        simulation_run = threading.Thread(target=self.run_simulation)
        enter_handler = threading.Thread(target=self.resume_simulation)
        pause_handler = threading.Thread(target=self.pause_simulation)
        escape_handler = threading.Thread(target=self.stop_simulation)

        pause_handler.start()
        enter_handler.start()
        escape_handler.start()
        simulation_run.start()

        escape_handler.join()
        pause_handler.join()
        enter_handler.join()
        simulation_run.join()

    def resume_simulation(self) -> None:
        while self.__running:
            keyboard.wait('enter')
            self.__paused = False

    def pause_simulation(self) -> None:
        while self.__running:
            keyboard.wait('space')
            self.__paused = True

    def stop_simulation(self) -> None:
        while self.__running:
            keyboard.wait('escape')
            self.__running = False
            exit()

    def initialize_simulation(self):
        for action in self.init_actions:
            action.execute()

    @property
    def step_counter(self):
        return self.__step_counter


if __name__ == '__main__':
    simulation = Simulation()
    simulation.start_simulation()
