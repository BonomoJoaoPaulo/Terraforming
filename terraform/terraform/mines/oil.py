from pickle import TRUE
from threading import Thread
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class Pipeline(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_pipeline(self):
        print(f"🔨 - [{self.location}] - {self.unities} oil unities are produced.")
        pass

    def produce(self):
        if(self.unities < self.constraint):
            # Protegemos com Lock para evitar condicao de corrida (ALTERACAO PERMITIDA).
            globals.acquire_oil()
            self.unities += 17
            globals.release_oil()
            self.print_pipeline()
        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_pipeline()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        
        # Encerra as threads quando nao houver mais nenhuma base ativa.
        while(len(globals.get_activity_bases()) != 0):
            self.produce()
        
        # print adicionado para facilitar correcao e visualizacao do codigo.
        print(f"🏭 - OIL MINE FINALIZED IN {self.location}.")
