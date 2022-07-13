from threading import Thread
import globals as G
from space.rocket import Rocket
#esta classe será implementada como uma thread para
#fazer os lançamentos de foguetes e esperar o tempo das viagens
#para que as threads das bases lançadoras não fiquem travadas no sleep

class Launcher(Thread):
    def __init__(self, base, planet, rocket):
        Thread.__init__(self)
        self.base = base
        self.planet = planet
        self.rocket = rocket

    def run(self):
        self.rocket.launch(self.base, self.planet)
