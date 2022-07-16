from random import randrange, random
from time import sleep
import globals as G

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
        north_pole = random.randint(0,2)

        if north_pole:
<<<<<<< HEAD
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")

            planet.nuke_detected(rocket_damage, "north")
        else:    
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")

            planet.nuke_detected(rocket_damage, "south")
=======
            G.get_north_pole_lock(planet.name).acquire()
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")

            G.planet_lock.acquire()
            planet.nuke_detected(rocket_damage)
            G.planet_lock.release()

            G.get_north_pole_lock(planet.name).release()

        else:
            G.get_south_pole_lock(planet.name).acquire()    
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")

            G.planet_lock.acquire()
            planet.nuke_detected(rocket_damage)
            G.planet_lock.release()

            G.get_south_pole_lock(planet.name).release() 

>>>>>>> 31571c1422ac08647f3a6898836adaf025da9936

    
    def voyage(self, planet): # Permitida a alteração (com ressalvas)

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.
        self.simulation_time_voyage(planet)
        failure =  self.do_we_have_a_problem()
        if not failure:
            self.nuke(planet)

        return



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
        return random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)        
