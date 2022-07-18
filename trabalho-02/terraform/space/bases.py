import globals
from threading import Thread
from space.rocket import Rocket
from random import choice
from time import sleep

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


    # create_rocket(self, rocket_name)
    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium >= 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA' and self.fuel >= 70:
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON' and self.fuel >= 50:
                        self.fuel = self.fuel - 50
                    elif (self.name == 'CANAVERAL CAPE' or self.name == 'MOSCOW') and self.fuel >= 100:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium >= 35:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA' and self.fuel >= 100:
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON' and self.fuel >= 90:
                        self.fuel = self.fuel - 90
                    elif (self.name == 'CANAVERAL CAPE' or self.name == 'MOSCOW') and self.fuel >= 120:
                        self.fuel = self.fuel - 120
            case 'LION':
                # ERRADO: Lion não precisa criar ogiva nuclear com 35 unidades de uranio
                # self.uranium = self.uranium - 35 
                if self.name == 'ALCANTARA' and self.fuel >= 100:
                    self.fuel = self.fuel - 100
                elif (self.name == 'MOSCOW' or self.name == 'CANAVERAL CAPE') and self.fuel >= 115:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")


    def refuel_oil(self):
        lock_oil = globals.get_oil_mutex()
        mines = globals.get_mines_ref()
        oil = mines['oil_earth']

        with lock_oil:
            if self._has_unities(oil):
                oil_unities_needed = self.constraints[1] - self.fuel

                # Se a base precisa de menos unidades do que exitem
                if oil_unities_needed <= oil.unities:
                    oil_refuel = oil_unities_needed

                # Se a base precisa de mais unidades do que exitem
                if oil_unities_needed > oil.unities:
                    oil_refuel = oil.unities

                self.fuel += oil_refuel
                oil.unities -= oil_refuel

    def refuel_uranium(self):
        lock_uranium = globals.get_uranium_mutex()
        mines = globals.get_mines_ref()
        uranium = mines['uranium_earth']

        with lock_uranium:
            if self._has_unities(uranium):
                uranium_unities_needed = self.constraints[0] - self.uranium

                # Se a base precisa de menos unidades do que exitem
                if uranium_unities_needed <= uranium.unities:
                    uranium_refuel = uranium_unities_needed

                # Se a base precisa de mais unidades do que exitem
                if uranium_unities_needed > uranium.unities:
                    uranium_refuel = uranium.unities

                self.uranium += uranium_refuel
                uranium.unities = uranium.unities - uranium_refuel


    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        while(True):
            # Se o base não for a Base lunar (self = Alcantara / Moscou / Canaveral),
            #   a base minera recursos
            if not self.name == 'MOON':
                if self.uranium <= self.constraints[0]:
                    self.refuel_uranium()
                if self.fuel <= self.constraints[1]:
                    self.refuel_oil()

                if self.rockets < self.constraints[2]:
                    with globals.get_rockets_executer() as rockets_executer:
                        # Prioridade de envio de foguete é para a Lua
                        lock_moon = globals.get_moon_mutex()
                        with lock_moon:
                            if not globals.get_moon_has_resources():
                                self._send_rocket_to_moon(rockets_executer)
                        
                        # Envia foguetes para alvos de terraformação
                        rocket_to_launch = choice(['DRAGON', 'FALCON'])
                        self._send_rocket_terraform(rocket_to_launch, rockets_executer)


            else:
                # Se a Base lunar não tiver recursos necessários pra lançar foguetes Dragon e/ou Falcon e criar ogivas,
                #   seta que ela precisa de recursos
                lock_moon = globals.get_moon_mutex()
                with lock_moon:
                    if self.uranium < 35 and (self.fuel < 90 or self.fuel < 50):
                        globals.set_moon_has_resources(False)


    #########
    # UTILS #
    #########

    def _has_unities(self, type): return type.unities > 0

    # LION -> MOON #
    def _has_resources_to_launch(self) -> bool:
        # Cado/Alcantara gastam 115 + 120 de gasolina para a carga
        # Moscou gasta 100 + 120 de gasolina para a carga
        # E todos gastam 75 de uranio para a carga
        print(f'🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}')
        return (self.fuel > (115+120) or self.fuel > (100+120)) and self.uranium > 75

    def _send_rocket_to_moon(self, rockets_executer) -> None:
        if self._has_resources_to_launch():
            self.base_rocket_resources('LION')
            self.rockets += 1
            rocket_lion = Rocket('LION')
            # Adiciona carga no foguete e remove carga da base
            rocket_lion.fuel_cargo = 120
            rocket_lion.uranium_cargo = 75
            self.fuel -= 120
            self.uranium -= 75
            bases = globals.get_bases_ref()
            rockets_executer.submit(rocket_lion.launch(self, bases['moon']))
            self.rockets -= 1
            sleep(0.1)

    # FALCON/DRAGON -> PLANET #
    def _send_rocket_terraform(self, rocket_type, rockets_executer):
        if self._has_resources_to_launch():
            self.base_rocket_resources(rocket_type)
            self.rockets += 1
            rocket = Rocket(rocket_type)
            target = choice(['mars', 'io', 'ganimedes', 'europa'])
            planets = globals.get_planets_ref()
            rockets_executer.submit(rocket.launch(self, planets[target]))
            self.rockets -= 1
            sleep(0.1)