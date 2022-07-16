import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
    
    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")


    def refuel_oil(self):
        mines = globals.get_mines_ref()
        oil = mines['oil_earth']

        lock_o.acquire()
        if oil.unities > 0 and self.fuel < self.constraints[1]:
            if self.name != 'MOON':
                oil_refuel = oil.unities
                self.fuel += oil_refuel
                oil.unities = oil.unities - oil_refuel
        lock_o.release()

        if self.name != 'MOON' and (self.fuel > 0 or self.uranium > 0):
            self.print_space_base_info()

    def refuel_uranium(self):
        mines = globals.get_mines_ref()
        uranium = mines['uranium_earth']

        lock_u.acquire()
        if uranium.unities > 0 and self.uranium < self.constraints[0]:
            # Se o base não for a Base lunar = self >> Alcantara / Moscou / CANAVERAL
            if self.name != 'MOON':
                uranium_refuel = uranium.unities
                self.uranium += uranium_refuel
                uranium.unities = uranium.unities - uranium_refuel
                # self.base_rocket_resources(rocket.name)
            # Base vai ser a Base lunar 
            # else:
                # rocket = Rocket('LION')
                # uranium_refuel = uranium.unities
        lock_u.release()

        if self.name != 'MOON' and (self.fuel > 0 or self.uranium > 0):
            self.print_space_base_info()

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.refuel_oil()
            self.refuel_uranium()
            if(self.name == 'MOON'):
                rocket = Rocket('LION')
                self.base_rocket_resources('LION')
            pass

lock_u = Lock()
lock_o = Lock()