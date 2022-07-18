from threading import Lock
from concurrent.futures import ThreadPoolExecutor

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
bases = {}
mines = {}
simulation_time = None

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

    ##########
    # EXTRAS #
    ##########

lock_uranium = Lock()
lock_oil = Lock()
def get_uranium_mutex():
    global lock_uranium
    return lock_uranium

def get_oil_mutex():
    global lock_oil
    return lock_oil


lock_moon = Lock()
def get_moon_mutex():
    global lock_moon
    return lock_moon


moon_resources = False
def set_moon_has_resources(has_resources):
    global moon_resources
    moon_resources = has_resources

def get_moon_has_resources():
    global moon_resources
    return moon_resources


rockets_executer = ThreadPoolExecutor()
def get_rockets_executer():
    global rockets_executer
    return rockets_executer