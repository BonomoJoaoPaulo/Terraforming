from threading import Thread
import globals as G
from space.rocket import Rocket
#esta classe será implementada como uma thread para
#fazer os lançamentos de foguetes e esperar o tempo das viagens
#para que as threads das bases lançadoras não fiquem travadas no sleep

class Launcher(Thread):
    def __init__(self, rocket_name):
        Thread.__init__(self)
        self.rocket = rocket_name

    def run(self):
        Rocket(self.rocket)
