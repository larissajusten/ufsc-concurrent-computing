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
        globals.acquire_print()
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
        globals.release_print()

    # create_rocket(self, rocket_name)
    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.name == 'MOON':
                    fuel_to_consume =  50
                elif self.name == 'ALCANTARA':
                    fuel_to_consume =  70
                else:    
                    fuel_to_consume =  100

                if self.uranium >= 35 and self.fuel >= fuel_to_consume:
                    self.uranium = self.uranium - 35
                    self.fuel = self.fuel - fuel_to_consume
                    return True

            case 'FALCON':
                if self.name == 'MOON':
                    fuel_to_consume =  90
                elif self.name == 'ALCANTARA':
                    fuel_to_consume =  100
                else:    
                    fuel_to_consume =  120

                if self.uranium >= 35 and self.fuel >= fuel_to_consume:
                    self.uranium = self.uranium - 35
                    self.fuel = self.fuel - fuel_to_consume
                    return True

            case 'LION':
                # ERRADO: Lion não precisa criar ogiva nuclear com 35 unidades de uranio
                # self.uranium = self.uranium - 35 
                
                if self.name == 'MOON':
                    return
                elif self.name == 'ALCANTARA':
                    fuel_to_consume =  100
                else:    
                    fuel_to_consume =  115

                if self.uranium >= 35 and self.fuel >= fuel_to_consume:
                    self.uranium = self.uranium - 35
                    self.fuel = self.fuel - fuel_to_consume
                    return True
            case _:
                print("Invalid rocket name")
            
        return False

    def fill_moon_resources(self,uranium, fuel):
        self.uranium += uranium
        self.fuel += fuel

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
        self.print_space_base_info()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.print_space_base_info()

            # Se o base não for a Base lunar (self = Alcantara / Moscou / Canaveral),
            # a base minera recursos
            if not self.name == 'MOON':
                if self.uranium <= self.constraints[0]:
                    self.refuel_uranium()
                if self.fuel <= self.constraints[1]:
                    self.refuel_oil()

                if self.rockets < self.constraints[2]:
                    rockets_executer = globals.get_rockets_executer()
                    # Prioridade de envio de foguete é para a Lua
                    with globals.get_moon_mutex():
                        with globals.get_rocket_to_moon_mutex():
                            # Se a lua precisa de recursos, mas nenhum foguete foi enviado, manda foguete
                            if globals.get_moon_needs_resources() != [0,0] and not(globals.get_rocket_to_moon()):
                                self._send_rocket_to_moon(rockets_executer)

                            #else: # Se a lua não precisa de recursos, pode enviar foguete normalmente
                            #    print(f"Pode enviar foguete normalmente, Já tem foguete pra lua, {globals.get_moon_needs_resources()},{globals.get_rocket_to_moon()}")
                                    
                    # Envia foguetes para alvos de terraformação
                    rocket_to_launch = choice(['DRAGON', 'FALCON'])
                    self._send_rocket_terraform(rocket_to_launch, rockets_executer)

                    self.wait_next_launch()

            else:
                # Se a Base lunar não tiver recursos necessários pra lançar foguetes Dragon e/ou Falcon e criar ogivas,
                # seta que ela precisa de recursos
                with globals.get_moon_mutex():
                    if self.uranium < self.constraints[0] or self.fuel < self.constraints[1]:
                        globals.set_moon_needs_resources(self.constraints[0] - self.uranium, self.constraints[1] - self.fuel)
                    else:
                        globals.set_moon_needs_resources(0,0)
            

    #########
    # UTILS #
    #########

    def _has_unities(self, type): return type.unities > 0
    
    def wait_next_launch(self):
        sleep(0.1) # Tempo de espera para poder lançar outro foguete

    # LION -> MOON #
    def _has_resources_to_launch(self) -> bool:
        # Cado/Alcantara gastam 115 + 120 de gasolina para a carga
        # Moscou gasta 100 + 120 de gasolina para a carga
        # E todos gastam 75 de uranio para a carga
        print(f'🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}')
        return (self.fuel > (115+120) or self.fuel > (100+120)) and self.uranium > 75

    def _send_rocket_to_moon(self, rockets_executer) -> None:
        if self.base_rocket_resources('LION'):
            print(f'🚀 - [{self.name}] → [MOON]')
            
            self.rockets += 1
            rocket_lion = Rocket('LION')

            # Adiciona carga no foguete e remove carga da base
            rocket_lion.fuel_cargo = 120 # TODO verificar quanto lua precisa e verificar quanto tenho
            rocket_lion.uranium_cargo = 75 # TODO verificar quanto lua precisa e verificar quanto tenho
            self.fuel -= 120
            self.uranium -= 75

            base = globals.get_bases_ref()
            rockets_executer.submit(rocket_lion.launch(self, base['moon']))
            self.rockets -= 1
            return True
        else:
            return False

    # FALCON/DRAGON -> PLANET #
    def _send_rocket_terraform(self, rocket_type, rockets_executer):
        if self.base_rocket_resources(rocket_type):
            self.rockets += 1
            rocket = Rocket(rocket_type)
            target = choice(['mars', 'io', 'ganimedes', 'europa'])
            print(f'🚀 - [{self.name}] → [{target.upper()}]')
            planets = globals.get_planets_ref()
            rockets_executer.submit(rocket.launch(self, planets[target]))
            self.rockets -= 1
            return True
        else:
            return False