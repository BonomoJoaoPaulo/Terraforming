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

    def nuke_detected(self, damage):
        if not self.is_planet_habitable():
            # Proteger com Lock para caso seja atacado nos dois polos
            globals.get_terraform_lock(self.name).acquire()
            if self.terraform - damage > 0:
                self.terraform -= damage
            else:
                self.terraform = 0
            #print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
            globals.get_terraform_lock(self.name).release()

        if self.is_planet_habitable():
            globals.remove_planet_from_list_planets_unhabitable(self.name)
            print(f"------------#) {self.terraform} (-------------")
            print(f"_-_-_-_-_-__) {self.name} (__-_-_--------__-___--_-_-_---_-___---")
            print("LISTA DE PLANETAS INABITAVEIS:\n"
            f"{globals.list_planets_unhabitable}")

    def is_planet_habitable(self):
        return self.terraform <= 0

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.create_planet_and_poles_locks(self.name)
        globals.append_in_unhabitale_planets(self.name)
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
