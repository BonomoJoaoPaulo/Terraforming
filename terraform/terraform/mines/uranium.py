from threading import Thread
from random import randint
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        # print(f"🔨 - [{self.location}] - {self.unities} uranium unities are produced.")
        pass

    def produce(self):
        if(self.unities < self.constraint):
            globals.uranium_acquire()
            self.unities+=15
            globals.uranuim_release()
            self.print_store_house()
        sleep(0.001)
        

    def run(self):
        globals.acquire_print()
        self.print_store_house()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(not globals.get_program_finish()):
            self.produce()