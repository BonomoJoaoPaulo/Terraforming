from threading import Thread
import globals

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform,name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self, damage, pole):
        # Proteger com Lock para caso seja atacado nos dois polos
        if pole == "north":
            globals.get_north_pole_lock(self.name).acquire()
            globals.get_planet_lock(self.name).acquire()
            self.terraform -= damage
            globals.get_planet_lock(self.name).release()
            globals.get_north_pole_lock(self.name).release()
        else:
            globals.get_south_poles_locks(self.name).acquire()
            globals.get_planets_locks(self.name).acquire()
            self.terraform -= damage
            globals.get_planets_locks(self.name).release()
            globals.get_south_poles_locks(self.name).release()

        print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.create_planet_and_poles_locks(self.name)
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
