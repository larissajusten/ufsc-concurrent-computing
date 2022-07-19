from threading import Thread
import globals

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform,name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self):
        '''
        Método que detecta se o nuke foi lançado no planeta
        '''
        # Ocorreu um bombardeio então pego um polo para usar
        globals.get_planets_dict_poles_semaphore()[self.name.lower()].acquire()
        while(self.terraform > 0):
            before_percentage = self.terraform
            while(before_percentage == self.terraform):
                pass
            print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
            
            
    def print_planet_info(self):
        globals.acquire_print()
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")
        globals.release_print()


    def run(self):
        self.print_planet_info()

        while(globals.get_release_system() == False):
            pass

        # Se o planeta ainda não é habitavel, ele precisa continuar a receber explosões
        while(not self.is_habitable()):
            # Se precisa ocorrer mais explosões ou se não precisa mais
            if self.terraform > 0:
                # Verificar se uma explosão foi detectada
                self.nuke_detected()

    #########
    # UTILS #
    #########


    def is_habitable(self):
        globals.get_planets_dict_locks()[self.name.lower()].acquire()
        is_habitable_var = True if self.terraform <= 0 else False
        globals.get_planets_dict_locks()[self.name.lower()].release()
        return is_habitable_var