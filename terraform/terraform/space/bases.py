import globals
from threading import Thread, Lock, Condition
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
    
    def consume_resources_to_create_rocket(self, rocket_name, lock2, enough_resources_to_create_any_rocket):
        with lock2:
            print("chegou no wait")
            enough_resources_to_create_any_rocket.wait()
        print('chamou o base rocket')
        self.base_rocket_resources(rocket_name)

    def base_rocket_resources(self, rocket_name, lock1, moon_need_resources):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA' and self.fuel >= 70:
                        globals.rocket_alc_sem_full.acquire()
                        self.fuel = self.fuel - 70
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('DRAGON'))
                        globals.rocket_alc_sem_empty.release()
                    elif self.name == 'MOON':
                        if self.fuel >= 50:
                            globals.rocket_moon_sem_full.acquire()
                            self.fuel = self.fuel - 50
                            self.rockets += 1
                            self.storage_rockets.append(Rocket('DRAGON'))
                            globals.rocket_alc_sem_empty.release()
                        else:
                            with lock1:
                                moon_need_resources.notify()
                    elif self.fuel >= 100:
                        globals.rocket_capemoscow_sem_full.acquire()
                        self.fuel = self.fuel - 100
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('DRAGON'))
                        globals.rocket_capemoscow_sem_empty.release()
                        
                        
            
            case 'FALCON':
                if self.uranium > 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA' and self.fuel >= 100:
                        globals.rocket_alc_sem_full.acquire()
                        self.fuel = self.fuel - 100
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('FALCON'))
                        globals.rocket_alc_sem_empty.release()
                    elif self.name == 'MOON':
                        if self.fuel >= 90:
                            globals.rocket_moon_sem_full.acquire()
                            self.fuel = self.fuel - 90
                            self.rockets += 1
                            self.storage_rockets.append(Rocket('FALCON'))
                            globals.rocket_moon_sem_empty.release() 
                        else:
                            with lock1:
                                moon_need_resources.notify()
                    elif self.fuel >= 120:
                        globals.rocket_capemoscow_sem_full.acquire()
                        self.fuel = self.fuel - 120
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('FALCON'))
                        globals.rocket_capemoscow_sem_empty.release()

            case 'LION':
                if self.uranium > 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA'  and self.fuel > 100:
                        globals.rocket_alc_sem_full.acquire()
                        self.fuel = self.fuel - 100
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('LION'))
                        globals.rocket_alc_sem_empty.release()
                    elif self.fuel > 115:
                        globals.rocket_capemoscow_sem_full.acquire()
                        self.fuel = self.fuel - 115
                        self.rockets += 1
                        self.storage_rockets.append(Rocket('LION'))
                        globals.rocket_capemoscow_sem_empty.release()
            case _:
                print("Invalid rocket name")

    def base_launch_rocket(self):
        if self.name == 'ALCANTARA':
            #decrementar o foguete de alcantara e lancar o puta
            print(f'lancou o foguete da base {self.name}')
            globals.rocket_alc_sem_empty.acquire()
            rocket = self.storage_rockets.pop(0)
            thread = Thread(target=self.voyageController, args=(rocket,))
            thread.start()
        elif self.name == 'MOON':
            #decrementar o foguete de moon e lancar o puta
            globals.rocket_moon_sem_empty.acquire()
            rocket = self.storage_rockets.pop(0)
            thread = Thread(target=self.voyageController, args=(rocket,))
            thread.start()
        else:
            #decrementar o foguete de moscow
            globals.rocket_capemoscow_sem_empty.acquire()
            rocket = self.storage_rockets.pop(0)
            thread = Thread(target=self.voyageController, args=(rocket,))
            thread.start()

        rocket = self.storage_rockets.pop(0)
        thread = Thread(target=self.voyageController, args=(rocket,))
        thread.start()


    def voyageController(self, rocket):
        print("chamou voyage controler")
        if self.name == 'ALCANTARA':
            #decrementar o foguete de alcantara e lancar o puta
            rocket.voyage
            print(f'lancou o {rocket.name} da base {self.name}')
            self.rockets -= 1
            globals.rocket_alc_sem_full.release()
        elif self.name == 'MOON':
            #decrementar o foguete de moon e lancar o puta
            rocket.voyage
            self.rockets -= 1
            globals.rocket_moon_sem_full.release()
        else:
            #decrementar o foguete de moscow
            rocket.voyage
            self.rockets -= 1
            globals.rocket_capemoscow_sem_full.release()

    def refuel_oil(self, mines_resources):
        oil = mines_resources['oil_earth']

        print(oil.unities, "mine fuel")
        globals.acquire_oil()

        space_in_stock = self.constraints[1] - self.fuel
        consumed = min(space_in_stock, oil.unities)

        self.fuel += consumed
        oil.unities -= consumed

        globals.release_oil()

    def refuel_uranium(self, mines_resources):
        uranium = mines_resources['uranium_earth']

        print(uranium.unities, "mine uranium")
        globals.uranium_acquire()

        space_in_stock = self.constraints[0] - self.uranium
        consumed = min(space_in_stock, uranium.unities)

        self.uranium += consumed
        uranium.unities -= consumed

        globals.uranuim_release()

    def verify_resources(self):
        if self.uranium < 35:
            if self.name == "ALCANATARA":
                #condition to create DRAGON
                if self.fuel > 70:
                    return True
                else:
                    return False
            if self.name == "MOON":
                #condition to create DRAGON
                if self.fuel > 50:
                    return True
                else:
                    return False
            else:
                #condition to create DRAGON
                if self.fuel > 100:
                    return True
                else:
                    return False
        else:
            return False

    def Has_resources_to_create_falcon(self):
        if self.name == "ALCANATARA":
            #condition to create FALCON
            if self.fuel > 100:
                return True
            else:
                return False
        if self.name == "MOON":
            #condition to create FALCON
            if self.fuel > 90:
                return True
            else:
                return False
        else:
            #condition to create FALCON
            if self.fuel > 120:
                return True
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
            mines_resources = globals.get_mines_ref()

            # Verificar qual foguete a base vai criar
            # Verificar se tem recursos

            if self.name != 'MOON':
                hasResources = False
                # Consome as minas de recursos ate ter recursos suficientes

                while not self.verify_resources():
                    if self.fuel < self.constraints[1]:
                        print(f"pediu refuel f{self.name}")
                        self.refuel_oil(mines_resources)
                    if self.uranium < self.constraints[0]:
                        print(f"pediu refuel u{self.name}")
                        self.refuel_uranium(mines_resources)
            
            
            else:
                hasResources = False
                if not hasResources:
                    pass

    
            foguetes = []
            foguetes.append("DRAGON")
            if self.Has_resources_to_create_falcon():
                foguetes.append("FALCON")

            rocket_name = choice(foguetes)
            print('Chamou o consume resources')
            self.consume_resources_to_create_rocket(rocket_name)
            print('Chamou o lauch rocket')
            self.base_launch_rocket()