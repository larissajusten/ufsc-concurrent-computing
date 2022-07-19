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
        '''
        Verifica se a base possui recursos para lançar um foguete
        '''
        match rocket_name:
            case 'DRAGON':
                if self.name == 'MOON':
                    fuel_to_consume = 50
                elif self.name == 'ALCANTARA':
                    fuel_to_consume = 70
                else:
                    fuel_to_consume = 100

                if self.uranium >= 35 and self.fuel >= fuel_to_consume:
                    self.uranium = self.uranium - 35
                    self.fuel = self.fuel - fuel_to_consume
                    return True

            case 'FALCON':
                if self.name == 'MOON':
                    fuel_to_consume = 90
                elif self.name == 'ALCANTARA':
                    fuel_to_consume = 100
                else:
                    fuel_to_consume = 120

                if self.uranium >= 35 and self.fuel >= fuel_to_consume:
                    self.uranium = self.uranium - 35
                    self.fuel = self.fuel - fuel_to_consume
                    return True

            case 'LION':
                # Alteração no Codigo do monitor: Lion não precisa criar ogiva nuclear com 35 unidades de uranio
                # self.uranium = self.uranium - 35
                if self.name == 'MOON':
                    return
                elif self.name == 'ALCANTARA':
                    fuel_to_consume = 100
                else:
                    fuel_to_consume = 115

                # 60 é a margem de erro possivel pra ir pra lua
                if self.fuel >= fuel_to_consume + 60:
                    self.fuel = self.fuel - fuel_to_consume
                    return True
            case _:
                print("Invalid rocket name")
        return False


    def refuel_oil(self):
        '''
        Recarrega a base com óleo(fuel)
        '''
        lock_oil = globals.get_oil_lock()
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
        '''
        Recarrega a base com uranio(uranium)
        '''
        lock_uranium = globals.get_uranium_lock()
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
        '''
        Método executado pelo thread
        '''
        self.print_space_base_info()

        while(globals.get_release_system() == False):
            pass

        while(globals.get_planets_to_terraform() != []):
            self.print_space_base_info()  # Imprime informações da base

            # Pergunta para satelites se precisa ou não mandar foguete
            with globals.get_planets_to_terraform_lock():
                # Se não há planetas para terraformar ele continua o código
                if not globals.get_planets_to_terraform():
                    continue

                for name_planet in globals.get_planets_to_terraform():
                    planet = globals.get_planets_ref()[name_planet]

                    if planet.is_habitable():
                        print(f'[{planet.name}] is habitable')
                        new_planets_list = globals.get_planets_to_terraform()
                        new_planets_list.remove(planet.name.lower())
                        globals.set_planets_to_terraform(new_planets_list)


            # Se o base não for a Base lunar (self = Alcantara / Moscou / Canaveral),
            # a base minera recursos (se precisar) e envia foguetes tanto pra lua quanto para o alvo
            if not self.name == 'MOON':
                if self.uranium <= self.constraints[0]:
                    self.refuel_uranium()
                if self.fuel <= self.constraints[1]:
                    self.refuel_oil()
                if self.rockets < self.constraints[2]:
                    # Prioridade de envio de foguete é para a Lua
                    # Pega mutex dos recursos da lua (pra saber se precisa)
                    with globals.get_moon_lock():  
                        # Pega mutex de foguete que vai pra lua (pra saber se já foi um foguete ou não)
                        with globals.get_rocket_to_moon_lock():
                            # Se a lua precisa de recursos, mas nenhum foguete foi enviado, Tenta enviar foguete para lua
                            if globals.get_moon_needs_resources() != [0, 0] and not(globals.get_rocket_to_moon()):
                                self._send_rocket_to_moon()
                                self.wait_next_launch()
                                continue
                            # Se a lua não precisa de recursos, pode enviar foguete normalmente

                    # Tenta enviar foguetes para alvos de terraformação
                    rocket_to_launch = choice(['DRAGON', 'FALCON'])
                    self._send_rocket_terraform(rocket_to_launch)

                    self.wait_next_launch()  # Espera o tempo necessário para o próximo lançamento

            else:
                # Se a Base lunar não tiver recursos necessários pra lançar foguetes Dragon e/ou Falcon e criar ogivas,
                # seta que ela precisa de recursos
                with globals.get_moon_lock():
                    if (self.uranium < (self.constraints[0] - 75)) or (self.fuel < (self.constraints[1] - 120)):
                        globals.set_moon_needs_resources(
                            self.constraints[0] - self.uranium, self.constraints[1] - self.fuel)
                    else:
                        globals.set_moon_needs_resources(0, 0)

                if self.rockets < self.constraints[2]:
                    rocket_to_launch = choice(['DRAGON', 'FALCON'])
                    self._send_rocket_terraform(rocket_to_launch)
                    self.wait_next_launch()

        globals.stop_simulation()


    #########
    # UTILS #
    #########


    def _has_unities(self, type) -> bool: return type.unities > 0


    def wait_next_launch(self) -> None:
        '''
        Espera o tempo necessário para o próximo lançamento
        '''
        sleep(0.0002)  # Tempo de espera para poder lançar outro foguete (equivalente a 1 dia de simulação, tempo escolhido arbitrariamente)
        pass


    def _send_rocket_to_moon(self) -> bool:
        '''
        Tenta enviar foguete para a lua
        '''
        if self.base_rocket_resources('LION'):
            self.rockets += 1
            rocket = Rocket('LION')  # Cria foguete
            base = globals.get_bases_ref()
            self.print_space_base_info()
            if globals.get_moon_needs_resources()[1] > 0:
                fuel_to_reduce = min([globals.get_moon_needs_resources()[1],self.fuel,120])
                self.fuel -= fuel_to_reduce
                rocket.fuel_cargo = fuel_to_reduce
            if globals.get_moon_needs_resources()[0] > 0:
                uranium_to_reduce = min([globals.get_moon_needs_resources()[0],self.uranium,75])
                self.uranium -= uranium_to_reduce
                rocket.uranium_cargo = uranium_to_reduce

            globals.get_rockets_executer().submit(rocket.launch(base=self, planet=base['moon']))
            
            self.rockets -= 1
            return True
        else:
            return False


    def _send_rocket_terraform(self, rocket_type) -> bool:
        '''
        Tenta enviar foguete para terraformar planeta
        '''
        if self.base_rocket_resources(rocket_type):
            self.rockets += 1
            rocket = Rocket(rocket_type)  # Cria foguete
            # Escolhe planeta/luas a ser terraformado
            globals.get_planets_to_terraform_lock().acquire()
            target = choice(globals.get_planets_to_terraform())
            globals.get_planets_to_terraform_lock().release()
            planets = globals.get_planets_ref()
            globals.get_rockets_executer().submit(
                rocket.launch(base=self, planet=planets[target]))
            self.rockets -= 1
            return True
        else:
            return False


    def fill_base_moon_resources(self, uranium, fuel) -> None:
        '''
        Preenche a lua com recursos
        '''
        self.uranium += uranium
        self.fuel += fuel
