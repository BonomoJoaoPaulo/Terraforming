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
            # Protegemos com Lock para caso seja atacado nos dois polos (evitando condicao de corrida).
            globals.get_terraform_lock(self.name).acquire()
            # Verifica se o dano causado deixara o valor negativo (impedindo que isso aconteca).
            if self.terraform - damage > 0:
                self.terraform -= damage
            else:
                self.terraform = 0
            print(f"⚠ - [NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
            # Libera o Lock.
            globals.get_terraform_lock(self.name).release()
        # Verifica se o planeta esta habitavel ou nao. Caso esteja,
        # retira-o da lista de planetas inabitaveis.
        if self.is_planet_habitable():
            globals.remove_planet_from_list_planets_unhabitable(self.name)

    # Criamos essa funcao apenas para verificar se o planeta esta habitavel ou nao.
    def is_planet_habitable(self):
        return self.terraform <= 0

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        # Cria os locks proprios daquele planeta.
        globals.create_planet_and_poles_locks(self.name)
        # Adiciona o planeta na lista de planetas inabitaveis.
        globals.append_in_unhabitale_planets(self.name)
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
