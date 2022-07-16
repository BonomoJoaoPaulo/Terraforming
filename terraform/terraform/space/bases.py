import globals
from threading import Thread, Lock, Condition
from space.rocket import Rocket
from random import choice
lock = Lock()
moon_need_resources = Condition(lock)
enough_resources_to_create_any_rocket = Condition(lock)

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
    
    def consume_resources_to_create_rocket(self, rocket_name):
        enough_resources_to_create_any_rocket.wait()
        self.base_rocket_resources(rocket_name)

    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA' and self.fuel >= 70:
                        globals.alc_sem.acquire()
                        self.fuel = self.fuel - 70
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('DRAGON'))
                    elif self.name == 'MOON':
                        if self.fuel >= 50:
                            globals.moon_sem.acquire()
                            self.fuel = self.fuel - 50
                            self.rockets += 1
                            self.storage_rockets.append(Rocket('DRAGON'))
                        else:
                            moon_need_resources.notify()
                    elif self.fuel >= 100:
                        globals.capemoscow_sem.acquire()
                        self.fuel = self.fuel - 100
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('DRAGON'))
            
            case 'FALCON':
                if self.uranium > 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA' and self.fuel >= 100:
                        globals.alc_sem.acquire()
                        self.fuel = self.fuel - 100
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('FALCON'))
                    elif self.name == 'MOON':
                        if self.fuel >= 90:
                            globals.moon_sem.acquire()
                            self.fuel = self.fuel - 90
                            self.rockets += 1
                            self.storage_rockets.append(Rocket('FALCON')) 
                        else:
                            moon_need_resources.notify()
                    elif self.fuel >= 120:
                        globals.capemoscow_sem.acquire()
                        self.fuel = self.fuel - 120
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('FALCON'))

            case 'LION':
                if self.uranium > 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA'  and self.fuel > 100:
                        globals.alc_sem.acquire()
                        self.fuel = self.fuel - 100
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('LION'))
                    elif self.fuel > 115:
                        globals.capemoscow_sem.acquire()
                        self.fuel = self.fuel - 115
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('LION'))
            case _:
                print("Invalid rocket name")

    def base_launch_rocket(self):
        rocket = self.storage_rockets.pop(0)
        thread = Thread(target=self.voyageController, args=(rocket,))


    def voyageController(self, rocket):
        rocket.



    def refuel_oil(self, mines_resources):
        oil = mines_resources['oil_earth']

        print(oil.unities, "mine fuel")
        globals.acquire_oil()
        self.fuel += oil.unities
        oil.unities = 0
        globals.release_oil()
        if self.fuel > globals.able_to_start:
            enough_resources_to_create_any_rocket.notify()
        if self.fuel > self.constraints[1]:
            self.fuel = self.constraints[1]

    def refuel_uranium(self, mines_resources):
        uranium = mines_resources['uranium_earth']

        print(uranium.unities, "mine uranium")
        globals.uranium_acquire()
        self.uranium += uranium.unities
        uranium.unities = 0
        globals.uranuim_release()
        if self.uranium > self.constraints[0]:
            self.uranium = self.constraints[0]
        
    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        self.storage_rockets = []

        while(globals.get_release_system() == False):
            pass

        while(True):
            mines_resources = globals.get_mines_ref()
            if self.name != 'MOON':
                if self.fuel < self.constraints[1]:
                    self.refuel_oil(mines_resources)
                if self.uranium < self.constraints[0]:
                    self.refuel_uranium(mines_resources)
            else:
                moon_need_resources.wait()
                self.consume_resources_to_create_rocket('LION')
                #lion_rocket_thread =Thread(target=rocket_lion_thread, args=(self, Lion))
                #lion_rocket_thread.start()
                #refuel moon with resources
    
            rocket_name = choice(['FALCON', 'DRAGON'])
            self.consume_resources_to_create_rocket(rocket_name)
