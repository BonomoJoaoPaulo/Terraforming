
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
        while(not globals.get_program_finish()):
            print("++++++++++++++++++++++++++++++++++++++++++++++")
            print(f"\n\n ⏳ - {self.current_time} year(s) have passed...\n\n")
            print("++++++++++++++++++++++++++++++++++++++++++")
            self.current_time+=1
            sleep(1)
        print(f"took {self.current_time} year to terraform all planets")
