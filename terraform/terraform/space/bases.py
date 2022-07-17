from time import sleep
import globals
from threading import Thread
from space.rocket import Rocket
from random import choice

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
    


    def create_rocket(self, rocket_name):
        if rocket_name == "DRAGON":
            self.uranium = self.uranium - 35
            if self.name == 'ALCANTARA':
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 70
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('DRAGON'))
            elif self.name == 'MOON':
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 50
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('DRAGON'))
            else:
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 100
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('DRAGON'))    
            
        elif rocket_name == "FALCON":
            self.uranium = self.uranium - 35
            if self.name == 'ALCANTARA':
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 100
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('FALCON'))
            elif self.name == 'MOON':
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 90
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('FALCON'))

            else:
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 120
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('FALCON'))

        elif rocket_name == "LION":
            self.uranium = self.uranium - 35
            if self.constraints[2] >= self.rockets:
                self.fuel = self.fuel - 100
                self.rockets += 1
                self.storage_rockets.append(Rocket('LION'))

            else:
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 115
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('LION'))
        else:
            print("Erro")
        

    def base_launch_rocket(self):
        rocket = self.storage_rockets.pop(0)
        self.rockets -= 1
        thread = Thread(target=self.voyageController, args=(rocket,))
        thread.start()

    def voyageController(self, rocket):
        print(f"Launching Rocket {rocket.name}")
        print(rocket)
        planet_to_go = rocket.get_planet_destiny()
        print(planet_to_go)
        rocket.launch(self,planet_to_go)

    def refuel_oil(self, mines_resources):
        oil = mines_resources['oil_earth']

        globals.acquire_oil()
        space_in_stock = self.constraints[1] - self.fuel
        consumed = min(space_in_stock, oil.unities)

        self.fuel += consumed
        oil.unities -= consumed

        globals.release_oil()

    def refuel_uranium(self, mines_resources):
        uranium = mines_resources['uranium_earth']

        globals.uranium_acquire()
        space_in_stock = self.constraints[0] - self.uranium
        consumed = min(space_in_stock, uranium.unities)

        self.uranium += consumed
        uranium.unities -= consumed

        globals.uranuim_release()

    def verify_resources(self):
        if self.uranium >= 35:
            if self.name == "ALCANTARA":
                #condition to create DRAGON
                if self.fuel >= 70:
                    return True
                else:
                    return False
            if self.name == "MOON":
                #condition to create DRAGON
                if self.fuel >= 50:
                    return True
                else:
                    return False
            else:
                #condition to create DRAGON
                if self.fuel >= 100:
                    return True
                else:
                    return False
        else:
            return False

    def Has_resources_to_create_falcon(self):
        if self.name == "ALCANTARA":
            #condition to create FALCON
            if self.fuel >= 100:
                return True
            else:
                return False
        if self.name == "MOON":
            #condition to create FALCON
            if self.fuel >= 90:
                return True
            else:
                return False
        else:
            #condition to create FALCON
            if self.fuel >= 120:
                return True
            else:
                return False

    def Moon_has_resources_to_dragon(self):
        if self.fuel >= 50:
            return True
    
    def Moon_has_resources_to_falcon(self):
        if self.fuel >= 90:
            return True

    def Has_resources_to_create_lion(self):
        if self.uranium >= 75:
            if self.name == "ALCANTARA":
                #condition to create LION
                if self.fuel >= 220:
                    return True
                else:
                    return False
            else:
                #condition to create LION
                if self.fuel >= 235:
                    return True
                else:
                    return False
        else:
            return False

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        self.storage_rockets = []
        while(globals.get_release_system() == False):
            pass

        while(True):
            self.print_space_base_info()
            mines_resources = globals.get_mines_ref()

            if self.name != 'MOON':
                acquired = globals.handle_lion_sem.acquire(blocking=False)

                # Consome as minas de recursos ate ter recursos suficientes
                if not acquired:
                    while not self.Has_resources_to_create_falcon():
                        self.refuel_oil(mines_resources)
                        self.refuel_uranium(mines_resources)

                    # self.print_space_base_info()
                else:
                    while not self.Has_resources_to_create_lion():
                        self.refuel_oil(mines_resources)
                        self.refuel_uranium(mines_resources)

                    self.create_rocket('LION')
                    self.base_launch_rocket()
                    # Se foguete nao chegar na Lua, liberar o mutex para outra base tentar enviar o Lion
                    continue
            
            else:
                if not self.Moon_has_resources_to_attack():
                    # Pede para uma base enviar Lion
                    globals.handle_lion_sem.release()
                    with globals.resources_got_in_moon_Lock:
                        globals.resources_got_in_moon_Condition.wait()

                # Notificar a Lua que chegou recursos

            foguetes = ["FALCON", "DRAGON"]

            rocket_name = choice(foguetes)
            self.create_rocket(rocket_name)
            self.base_launch_rocket()

    def Moon_has_resources_to_attack(self):
        if self.uranium < 35:
            return False
        
        if self.fuel < 50:
            return False
        
        return True