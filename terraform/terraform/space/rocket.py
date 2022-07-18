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
            

    def nuke(self, planet):
        rocket_damage = self.damage()
        # Variaveis a receber os Locks de cada polo do planeta.
        north_lock = globals.get_north_pole_lock(planet.name)
        south_lock = globals.get_south_pole_lock(planet.name)
        # Verifica se o planeta ainda esta na lista de planetas inabitaveis.
        if planet.name.lower() in globals.list_planets_unhabitable:
            # Verifica se o polo norte esta "lockado". Se sim, a explosao ocorrera no polo sul.
            # Eh feito um acquire e depois um release no lock do polo do planeta a ser atingido.
            if north_lock.locked():
                south_lock.acquire()
                print(f"💥 - [EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
                planet.nuke_detected(rocket_damage)
                south_lock.release()
            else:
                north_lock.acquire()
                print(f"💥 - [EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
                planet.nuke_detected(rocket_damage)
                north_lock.release() 

    def voyage(self, planet):
        # Verifica se o rocket eh um LION (ja que a logica de sua viagem eh diferente dos demais).
        if self.name == "LION" :
            if not self.do_we_have_a_problem():
                with globals.resources_got_in_moon_Lock:
                    print(f"🌖 - RESOURCES LANDED IN THE MOON.")
                    globals.resources_got_in_moon_Condition.notify()
            else:
                print(f"LION da {self.name} TEVE PROBLEMAS LIBERANDO O SEMAFARO PARA ALGUEM LANCAR OUTRO LION")
                globals.handle_lion_sem.release()
        else:
            if not self.do_we_have_a_problem():
                self.simulation_time_voyage(planet)
                self.nuke(planet)

        return

    # Essa funcao eh responsavel por pegar o planeta destino do foguete.
    def get_planet_destiny(self, planets_list):
        # planets recebe as referencias de todos os planetas.
        planets = globals.get_planets_ref()
        # destiny escolhe aleatoriamente um planeta que esteja em planets_list (que no caso eh passado a lista de
        # planetas nao terraformados ainda).
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
        print(f"❌ - [GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self):
        print(f"☄ - [METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(f"❌ - [LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True
    
    def damage(self):
        return random()

    # Foi preciso uma pequena alteracao nessa funcao para o 
    # funcionamento correto do LION.

    def launch(self, base, planet):    
        if(self.successfull_launch(base)):
            print(f"📤- [{self.name} - {self.id}] launched.")
            self.voyage(planet)
        else:
            if self.name == "LION":
                print(f"LION FALHOU NO LANCAMENTO LIBERANDO O SEMAFARO PARA ALGUEM LANCAR OUTRO LION")
                globals.handle_lion_sem.release()
