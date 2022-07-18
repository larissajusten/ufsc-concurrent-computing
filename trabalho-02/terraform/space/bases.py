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
        lock_oil = globals.get_oil_mutex()
        mines = globals.get_mines_ref()
        oil = mines['oil_earth']

        lock_oil.acquire()
        if self._has_unities(oil):
            # Se o base não for a Base lunar (self = Alcantara / Moscou / Canaveral)
            if self.name != 'MOON':
                oil_unities_needed = self.constraints[1] - self.fuel

                # Se a base precisa de menos unidades do que exitem
                if oil_unities_needed <= oil.unities:
                    oil_refuel = oil_unities_needed

                # Se a base precisa de mais unidades do que exitem
                if oil_unities_needed > oil.unities:
                    oil_refuel = oil.unities

                self.fuel += oil_refuel
                oil.unities -= oil_refuel
        lock_oil.release()

        if self.name != 'MOON' and (self.fuel > 0 or self.uranium > 0):
            globals.acquire_print()
            self.print_space_base_info()
            globals.release_print()


    def refuel_uranium(self):
        lock_uranium = globals.get_uranium_mutex()
        mines = globals.get_mines_ref()
        uranium = mines['uranium_earth']

        lock_uranium.acquire()
        if self._has_unities(uranium):
            # Se o base não for a Base lunar (self = Alcantara / Moscou / Canaveral)
            if self.name != 'MOON':
                uranium_unities_needed = self.constraints[0] - self.uranium

                # Se a base precisa de menos unidades do que exitem
                if uranium_unities_needed <= uranium.unities:
                    uranium_refuel = uranium_unities_needed

                # Se a base precisa de mais unidades do que exitem
                if uranium_unities_needed > uranium.unities:
                    uranium_refuel = uranium.unities

                self.uranium += uranium_refuel
                uranium.unities = uranium.unities - uranium_refuel
        lock_uranium.release()

        if self.name != 'MOON' and (self.fuel > 0 or self.uranium > 0):
            globals.acquire_print()
            self.print_space_base_info()
            globals.release_print()


    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            if not self.uranium == self.constraints[0]:
                self.refuel_uranium()
            if not self.fuel == self.constraints[1]:
                self.refuel_oil()
            pass

    #########
    # UTILS #
    #########

    def _has_unities(self, type): return type.unities > 0
