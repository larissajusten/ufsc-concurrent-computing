from multiprocessing import Semaphore
from threading import Lock, Condition, RLock
from concurrent.futures import ThreadPoolExecutor
'''
    A total alteração deste arquivo é permitida.
    Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
    Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las.
    Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
    um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
    muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
    global de estados da aplicação e está presente em sistemas robustos pelo mundo.
'''

    #############
    # VARIAVEIS #
    #############

release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None

'''Lock para controlar a execução da simulação (thread principal)'''
mutex_running = Lock()
mutex_running.acquire()

uranium_lock = Lock()
oil_lock = Lock()

'''Variaveis para o controle do carregamento para a Lua'''
rocket_to_moon_lock = RLock()
rocket_to_moon = False
moon_needs_resources_lock = Lock()
moon_needs_resources = [-1,-1] # Quantidade de recursos que a lua precisa [uranium, fuel], -1 = muito

'''Variaveis para o controle dos foguetes'''
rockets_executer = ThreadPoolExecutor(30)

'''Variaveis para controle da lista de planetas que precisão ser terraformados, que precisam receber foguetes'''
planets_to_terraform_lock = Lock()
planets_to_terraform = ['mars', 'io', 'ganimedes', 'europa']

'''Variaveis para controle dos depositos das bases'''
bases_dict_locks = {
    'alcantara': Lock(),
    'canaveral cape': Lock(),
    'moscow': Lock(),
    'moon': Lock(),
}

'''Variaveis para controle dos planetas que vão receber dano das ogivas'''
planets_dict_locks = {
    'mars': Lock(),
    'io': Lock(),
    'ganimedes': Lock(),
    'europa': Lock(),
}

'''Variaveis para controle dos polos dos planetas que vão receber dano das ogivas'''
max_nukes_at_time = 2

planets_dict_poles_semaphore = {
    'mars': Semaphore(value=max_nukes_at_time),
    'io': Semaphore(value=max_nukes_at_time),
    'ganimedes': Semaphore(value=max_nukes_at_time),
    'europa': Semaphore(value=max_nukes_at_time),
}


    ###################
    # METODOS DEFAULT #
    ###################


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


'''Por ser uma metodo setter seria necessario ter um parametro, não?! set_is_system_released?'''
def set_release_system():
    global release_system
    release_system = True
    wait_end() # Aguarda o termino do sistema


def get_release_system():
    global release_system
    return release_system


def set_simulation_time(time):
    global simulation_time
    simulation_time = time


def get_simulation_time():
    global simulation_time
    return simulation_time


    ##################
    # METODOS EXTRAS #
    ##################


# SIMULAÇÃO #
def wait_end():
    '''
    Espera a simulação terminar
    '''
    global mutex_running
    while mutex_running.locked():
        pass

    get_rockets_executer().shutdown()

    acquire_print()
    print("\n\n##################################### SIMULATION ENDED #####################################\n")
    print(f"Years to finish the mission: {get_simulation_time().simulation_time()}\n\n")
    release_print()
    return

def is_program_not_finished():
    global mutex_running
    if mutex_running.locked():
        return True
    return False

def stop_simulation():
    '''
    Para a simulação
    '''
    global mutex_running
    if mutex_running.locked():
        mutex_running.release()


# URANIO #
def get_uranium_lock():
    '''
    Retorna o mutex dos recursos da mina de urânio
    '''
    global uranium_lock
    return uranium_lock


# COMBUSTIVEL/PETROLEO #
def get_oil_lock():
    '''
    Retorna o mutex dos recursos da reserva de petróleo
    '''
    global oil_lock
    return oil_lock


# LUA #
def get_moon_lock():
    '''
    Retorna o mutex dos recursos da lua
    '''
    global moon_needs_resources_lock
    return moon_needs_resources_lock


def set_moon_needs_resources(uranium, fuel):
    '''
    Seta a quantidade de recursos que a lua precisa
    '''
    global moon_needs_resources
    moon_needs_resources = [uranium, fuel]


def get_moon_needs_resources():
    '''
    Retorna a quantidade de recursos que a lua precisa
    '''
    global moon_needs_resources
    return moon_needs_resources


def get_rocket_to_moon_lock():
    '''
    Retorna o mutex do foguete de carregamento para a lua
    '''
    global rocket_to_moon_lock
    return rocket_to_moon_lock


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


# FOGUETES #
def get_rockets_executer():
    '''
    Retorna o executor dos foguetes
    '''
    global rockets_executer
    return rockets_executer


# PLANETAS #
def get_planets_to_terraform_lock():
    '''
    Retorna o mutex dos planetas que ainda precisam ser terraformados
    '''
    global planets_to_terraform_lock
    return planets_to_terraform_lock


def get_planets_to_terraform():
    '''
    Retorna a lista de planetas que precisa ser terraformado
    '''
    global planets_to_terraform
    return planets_to_terraform


def set_planets_to_terraform(new_planets_to_terraform):
    '''
    Seta uma nova lista de planetas para serem terraformados
    '''
    global planets_to_terraform
    planets_to_terraform = new_planets_to_terraform


# BASES #
def get_bases_dict_locks():
    '''
    Retorna o dict que contem o lock de cada planeta que vai receber dano da ogiva
    '''
    global bases_dict_locks
    return bases_dict_locks


# PLANETAS #
def get_planets_dict_locks():
    '''
    Retorna o dict que contem o lock de cada planeta que vai receber dano da ogiva
    '''
    global planets_dict_locks
    return planets_dict_locks


def get_planets_dict_poles_semaphore():
    '''
    Retorna o dict que contem o lock de cada planeta que vai receber dano da ogiva
    '''
    global planets_dict_poles_semaphore
    return planets_dict_poles_semaphore
