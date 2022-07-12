import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice

oil_mutex = Lock()
uranium_mutex = Lock()

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
    
    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")


    def refuel_oil(self, mines_resources):
        oil = mines_resources['oil_earth']

        print(oil.unities, "mine fuel")
        oil_mutex.acquire()
        self.fuel += oil.unities
        oil.unities = 0
        oil_mutex.release()
        if self.fuel > self.constraints[1]:
            self.fuel = self.constraints[1]
        self.print_space_base_info()

    def refuel_uranium(self, mines_resources):
        uranium = mines_resources['uranium_earth']

        print(uranium.unities, "mine uranium")
        uranium_mutex.acquire()
        self.uranium += uranium.unities
        uranium.unities = 0
        uranium_mutex.release()
        if self.uranium > self.constraints[0]:
            self.uranium = self.constraints[0]
        self.print_space_base_info()

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            mines_resources = globals.get_mines_ref()
            if self.fuel < self.constraints[1]:
                self.refuel_oil(mines_resources)
            if self.uranium < self.constraints[0]:
                self.refuel_uranium(mines_resources)
            

    
