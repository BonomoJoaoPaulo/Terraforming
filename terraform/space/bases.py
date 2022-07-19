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
    

    #quando o create_rocket eh chamada com certeza a base tem recursos para criar o foguete
    def create_rocket(self, rocket_name):
        #decrementa a quantidade de combustivel relativo a cada foguete em cada base
        if rocket_name == "DRAGON":
            self.uranium = self.uranium - 35
            if self.name == 'ALCANTARA':
                #verifica se a base tem espaco para criar mais um foguete 
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 70
                    self.rockets += 1
                    #coloca o foguete criado em uma lista 
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
            self.uranium = self.uranium - 75
            if self.name == "ALCANTARA" and self.constraints[2] >= self.rockets:
                self.fuel = self.fuel - 220
                self.rockets += 1
                self.storage_rockets.append(Rocket('LION'))

            else:
                if self.constraints[2] >= self.rockets:
                    self.fuel = self.fuel - 235
                    self.rockets += 1
                    self.storage_rockets.append(Rocket('LION'))
        else:
            print("Erro")
        
    #tira um foguete da lista de foguetes da base e cria um thread para cada foguete 
    def base_launch_rocket(self):
        rocket = self.storage_rockets.pop(0)
        self.rockets -= 1
        if rocket.name == "LION":
            thread = Thread(target=self.LionvoyageController, args=(rocket,))
            thread.start()    
        else:
            thread = Thread(target=self.voyageController, args=(rocket,))
            thread.start()

    def LionvoyageController(self,rocket):
        #lanca o lion para a lua
        rocket.launch(self, "MOON")

    def voyageController(self, rocket):
        #primeiro verifica se ainda existem planetas a serem terraformados, escolhe aleatoriamente um desses planetas e lanca o foguete
        if len(globals.list_planets_unhabitable) != 0:
            planet_to_go = rocket.get_planet_destiny(globals.get_unhabitable_planets())    
            rocket.launch(self,planet_to_go)

    #refuel de combustivel na base, protegendo a variavel global que todas as bases acessam com mutex para nao haver condicao de corrida
    def refuel_oil(self, mines_resources):
        oil = mines_resources['oil_earth']

        globals.acquire_oil()
        space_in_stock = self.constraints[1] - self.fuel
        consumed = min(space_in_stock, oil.unities)

        self.fuel += consumed
        oil.unities -= consumed

        globals.release_oil()

    #refuel de urranium na base, protegendo a variavel global que todas as bases acessam com mutex para nao haver condicao de corrida
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
        globals.append_in_list_activity_bases(self.name)

        self.storage_rockets = []
        while(globals.get_release_system() == False):
            pass

        while not globals.get_program_finish():
            self.print_space_base_info()
            mines_resources = globals.get_mines_ref()

            if self.name != 'MOON':
                #semafaro que deixa somente uma base enviar o lion pra lua por iteracao do while
                acquired = globals.handle_lion_sem.acquire(blocking=False)

                #caso nao for a base que enviara o lion
                if not acquired:
                    while not self.Has_resources_to_create_falcon():
                        # Consome as minas de recursos ate ter recursos suficientes para criar ou o falcon ou o dragon
                        self.refuel_oil(mines_resources)
                        self.refuel_uranium(mines_resources)
                #caso for a base que envia o lion
                else:
                    while not self.Has_resources_to_create_lion():
                        #Consome das minas de recursos ate ter recursos para criar e carregar o lion
                        self.refuel_oil(mines_resources)
                        self.refuel_uranium(mines_resources)

                    #Criando e lancando o lion
                    self.create_rocket('LION')
                    self.base_launch_rocket()
                    continue
            
            #Thread da Lua
            else:
                #se a lua nao tiver recursos para criar o dragon e o falcon
                if not self.Moon_has_resources_to_attack():
                    # Pede para uma das bases enviar o lion dando release no semafaro 
                    globals.handle_lion_sem.release()
                    with globals.resources_got_in_moon_Lock:
                        # Espera que os recursos do lion cheguem na lua para abastecer a base
                        globals.resources_got_in_moon_Condition.wait()
                        fuel = self.constraints[1] - self.fuel
                        uranium = self.constraints[0] - self.uranium
                        #Logica para a lua nao abastecer mais do que sua capacidade
                        self.fuel += min(fuel, 120)
                        self.uranium += min(uranium,75)
                        self.print_space_base_info()

            #lista de foguetes de ataque
            foguetes = ["FALCON", "DRAGON"]
            #Cria aleatoriamente o foguete e lanca
            rocket_name = choice(foguetes)
            self.create_rocket(rocket_name)
            self.base_launch_rocket()

        globals.remove_base_from_list_activity_bases(self.name)
        print(f"🔭 - BASE {self.name} FINALIZED.")

    def Moon_has_resources_to_attack(self):
        if self.uranium < 35 or self.fuel < 90 :
            return False
        
        else:
            return True
