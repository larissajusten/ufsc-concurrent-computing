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

        while(True):
            # TODO: Verificar se o nuke foi lançado, 
            # TODO: se precisa fazer nuke ou se não precisa mais
            # TODO: Resposta para as bases se precisa ou não mandar foguete
            self.nuke_detected()
