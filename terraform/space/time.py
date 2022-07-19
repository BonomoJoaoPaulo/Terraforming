
from threading import Thread
from time import sleep

import globals

######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class SimulationTime(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.current_time = 0
    
    def simulation_time(self):
        return self.current_time
    
    def run(self):
        while(globals.get_release_system() == False):
            pass

        # Alteracao permitida para adicionar uma condicao que termine o while.
        while(not globals.get_program_finish()):
            print(f"\n\n ⏳ - {self.current_time} year(s) have passed...\n\n")
            self.current_time+=1
            sleep(1)

        # Print para visualizar mais facilmente quantos anos se passaram ao termino do programa.
        print(f"\n\n 🏅 - THE ENDURANCE PROJECT HAS FINESHED! {self.current_time} year(s) have passed.\n\n")
