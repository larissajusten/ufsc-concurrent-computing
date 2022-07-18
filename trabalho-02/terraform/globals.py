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

# Mutex para controlar a execução da simulação (thread principal)
mutex_running = Lock()
mutex_running.acquire()


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

# Por ser uma metodo setter é necessario um parametro


def set_release_system():
    global release_system
    release_system = True
    wait_end()


def wait_end():
    '''
    Espera a simulação terminar
    '''
    global mutex_running
    while mutex_running.locked():
        pass


def stop_simulation():
    '''
    Para a simulação
    '''
    global mutex_running
    mutex_running.release()


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


### Variaveis globais para o controle do carregamento para a Lua
rocket_to_moon_mutex = Lock()
rocket_to_moon = False
moon_needs_resources_mutex = Lock()
moon_needs_resources = [-1,-1] # Quantidade de recursos que a lua precisa [uranium, fuel], -1 = muito

def get_moon_mutex():
    '''
    Retorna o mutex dos recursos da lua
    '''
    global moon_needs_resources_mutex
    return moon_needs_resources_mutex

def set_moon_needs_resources(uranium, fuel):
    '''
    seta a quantidade de recursos que a lua precisa
    '''
    global moon_needs_resources
    moon_needs_resources = [uranium, fuel]

def get_moon_needs_resources():
    '''
    Retorna a quantidade de recursos que a lua precisa
    '''
    global moon_needs_resources
    return moon_needs_resources

def get_rocket_to_moon_mutex():
    '''
    Retorna o mutex do foguete de carregamento para a lua
    '''
    global rocket_to_moon_mutex
    return rocket_to_moon_mutex

def get_rocket_to_moon():
    '''
    Retorna se tem foguete de carregamento para a lua
    '''
    global rocket_to_moon
    return rocket_to_moon

def set_rocket_to_moon(rocket):
    '''
    Seta se tem foguete de carregamento para a lua
    '''
    global rocket_to_moon
    rocket_to_moon = rocket


### Variaveis globais para o controle dos foguetes
rockets_executer = ThreadPoolExecutor(30)

def get_rockets_executer():
    '''
    Retorna o executor dos foguetes
    '''
    global rockets_executer
    return rockets_executer
