from random import randrange, random
from time import sleep
import globals


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0
            

    def nuke(self, planet): # Permitida a alteração - [bomba nuclear/ogiva]
        self.damage()
        print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
        print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
        pass
    
    def voyage(self, planet): # Permitida a alteração (com ressalvas) - [viagem]
        if self.do_we_have_a_problem(): return

        if planet == 'MOON' and self.name == 'LION':
            sleep(0.005) # Simula tempo de viagem para lua (4 dias)
            print(f"[CARGO] - The {self.name} ROCKET reached the MOON")
            with globals.get_moon_mutex():
                globals.set_moon_has_resources(True)
                self._set_moon_resources(planet)
            return

        self.simulation_time_voyage(planet)
        self.nuke(planet)

    def _set_moon_resources(self, planet_or_base):
        planet_or_base.fill_moon_resources(self.uranium_cargo, self.fuel_cargo)
        self.uranium_cargo = 0
        self.fuel_cargo = 0



    ####################################################
    #                   ATENÇÃO                        # 
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################
    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            sleep(2) # Marte tem uma distância aproximada de dois anos do planeta Terra.
        else:
            sleep(5) # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False
            
    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True
    
    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)        
