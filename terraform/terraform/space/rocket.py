from random import randrange, random
from secrets import choice
from time import sleep
import globals

class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0
            

    def nuke(self, planet): # Permitida a alteração
        rocket_damage = self.damage()
        globals.get_planet_semaphore(planet.name).acquire()
        north_lock = globals.get_north_pole_lock(planet.name)
        south_lock = globals.get_south_pole_lock(planet.name)
        if planet.name.lower() in globals.list_planets_unhabitable:
            if north_lock.locked():
                south_lock.acquire()
                print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
                planet.nuke_detected(rocket_damage)
                south_lock.release()
            else:
                north_lock.acquire()
                print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
                planet.nuke_detected(rocket_damage)
                north_lock.release()
        globals.get_planet_semaphore(planet.name).release()

    def voyage(self, planet): # Permitida a alteração (com ressalvas)
        
        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.

        if self.name == "LION" :
            if not self.do_we_have_a_problem():
                print("LION NAO TEVE PROBLEMA")
                # sleep(0.04)
                with globals.resources_got_in_moon_Lock:
                    print(f"RECURSOS CHEGARAM NA LUA{self.name} NOTIFY")
                    globals.resources_got_in_moon_Condition.notify()
            else:
                print(f"LION da {self.name} TEVE PROBLEMAS LIBERANDO O SEMAFARO PARA ALGUEM LANCAR OUTRO LION")
                globals.handle_lion_sem.release()
        else:
            if not self.do_we_have_a_problem():
                self.simulation_time_voyage(planet)
                self.nuke(planet)

        return

    def get_planet_destiny(self, planets_list):
        planets = globals.get_planets_ref()
        destiny = choice(planets_list)
        return planets[destiny]
    

    ####################################################
    #                   ATENÇÃO                        # 
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################
    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            sleep(2) # Marte tem uma distância aproximada de dois anos do planeta Terra.
        else:
            sleep(5) # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False
            
    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True
    
    def damage(self):
        return random() * 50

    def launch(self, base, planet):    
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)
        else:
            if self.name == "LION":
                print(f"LION FALHOU NO LANCAMENTO LIBERANDO O SEMAFARO PARA ALGUEM LANCAR OUTRO LION")
                globals.handle_lion_sem.release()
