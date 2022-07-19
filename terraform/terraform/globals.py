from telnetlib import SE
from threading import Condition, Lock, Semaphore

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las. 
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}

# Cada planeta tera um Lock para cada um de seus polos e outro para a terraformacao.
north_poles_locks = {}
south_poles_locks = {}
terraform_locks = {}

# Criacao de uma lista que contera todos os planetas ainda nao terraformados.
list_planets_unhabitable = []

bases = {}
mines = {}
simulation_time = None

# Criacao dos Locks para oil e uranium
oil_mutex = Lock()
oil_mutex_Condition = Condition(oil_mutex)
uranium_mutex = Lock()
uranium_mutex_Condition = Condition(uranium_mutex)

# Semaforo para uma base poder lancar o LION por vez.
handle_lion_sem = Semaphore(0)

# Booleano que diz se MOON precisa ou nao de recursos.
moon_need_resources = False

# Lock e Condition para recursos que chegam a MOON.
resources_got_in_moon_Lock = Lock()
resources_got_in_moon_Condition = Condition(resources_got_in_moon_Lock)

# Booleano para encerrar as bases quando todos planetas forem terraformados.
terraformed = False

# Lista de bases ativas.
list_activity_bases = []

def acquire_oil():
    global oil_mutex
    oil_mutex.acquire()

def release_oil():
    global oil_mutex
    oil_mutex.release()

def uranium_acquire():
    global uranium_mutex
    uranium_mutex.acquire()

def uranuim_release():
    global uranium_mutex
    uranium_mutex.release()

def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

# Funcao para criar os locks de um planetas.
def create_planet_and_poles_locks(planet_name):
    global north_poles_locks
    global south_poles_locks
    global terraform_locks

    north_poles_locks[planet_name] = Lock()
    south_poles_locks[planet_name] = Lock()
    terraform_locks[planet_name] = Lock()


def get_north_pole_lock(planet_name) -> Lock:
    global north_poles_locks
    return north_poles_locks[planet_name]

def get_south_pole_lock(planet_name) -> Lock:
    global south_poles_locks
    return south_poles_locks[planet_name]

def get_terraform_lock(planet_name) -> Lock:
    global terraform_locks
    return terraform_locks[planet_name]

# Funcao para adicionar um planeta na lista de planetas inabitaveis.
def append_in_unhabitale_planets(planet_name):
    global list_planets_unhabitable
    list_planets_unhabitable.append(planet_name.lower())

# Funcao para remover um planeta terraformado da lista de planetas inabitaveis.
def remove_planet_from_list_planets_unhabitable(planet_name):
    global list_planets_unhabitable

    if planet_name.lower() in list_planets_unhabitable:
        list_planets_unhabitable.remove(planet_name.lower())
        print(f"🌎 - [TERRAFORMED] {planet_name} was successfully terraformed.")
    if len(list_planets_unhabitable) == 0:
        print("\n\n🎉 - ALL PLANETS WERE SUCCESSFULLY TERRAFORMED!\n\n")
        set_program_finish(True)

# Isso eh usado na finalizacao das bases.
def get_unhabitable_planets():
    global list_planets_unhabitable
    return list_planets_unhabitable

# Funcao para adicionar uma base na lista de bases ativas.
def append_in_list_activity_bases(base_name):
    global list_activity_bases
    list_activity_bases.append(base_name.lower())

# Funcao para tirar uma base da lista de bases ativas (chamada na finalizacao da thread da base).
def remove_base_from_list_activity_bases(base_name):
    global list_activity_bases
    if base_name.lower() in list_activity_bases:
        list_activity_bases.remove(base_name.lower())

# Isso eh usado na finalizacao das minas de oil e uranium.
def get_activity_bases():
    global list_activity_bases
    return list_activity_bases

def set_bases_ref(all_bases):
    global bases
    bases = all_bases

def get_bases_ref():
    global bases
    return bases

def set_mines_ref(all_mines):
    global mines
    mines = all_mines

def get_mines_ref():
    global mines
    return mines

def set_release_system():
    global release_system
    release_system = True

def get_release_system():
    global release_system
    return release_system

def set_simulation_time(time):
    global simulation_time
    simulation_time = time

def get_simulation_time():
    global simulation_time
    return simulation_time

# Essa funcao sera chamada na hora de encerrar o programa.
def set_program_finish(finished):
    global terraformed
    global resources_got_in_moon_Lock
    global resources_got_in_moon_Condition

    terraformed = finished
    with resources_got_in_moon_Lock:
        resources_got_in_moon_Condition.notify_all()

def get_program_finish():
    global terraformed
    return terraformed
