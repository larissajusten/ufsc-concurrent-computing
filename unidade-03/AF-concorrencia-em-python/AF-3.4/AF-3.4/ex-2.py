from time import sleep
from random import randint
from threading import Thread, Semaphore, Condition

def produtort():
  global buffer
  for i in range(10):
    # decrementa o semáforo
    sem_vazio.acquire()   
    sleep(randint(0,2))
    item = 'item ' + str(i)
    if len(buffer) == tam_buffer:
        print('>>> Buffer cheio. Produtor ira aguardar.')
    buffer.append(item)
    print('Produzido %s (ha %i itens no buffer)' % (item,len(buffer)))
    # incrementa semáforo
    sem_cheio.release()

def consumidort():
  global buffer
  for i in range(10):
    # decrementa o semáforo
    sem_cheio.acquire()
    if len(buffer) == 0:
        print('>>> Buffer vazio. Consumidor ira aguardar.')
    item = buffer.pop(0)
    print('Consumido %s (ha %i itens no buffer)' % (item,len(buffer)))
    sleep(randint(0,2))
    # incrementa semáforo
    sem_vazio.release()

buffer = []
tam_buffer = 3
# cria semáforos
sem_cheio = Semaphore(0)
sem_vazio = Semaphore(tam_buffer)

# cria a thread produtora e a consumidora
produtor = Thread(target=produtort) 
consumidor = Thread(target=consumidort)

# inicia a thread produtora e a consumidora
produtor.start()
consumidor.start()

# aguarda a thread produtora e a consumidora finalizarem.
produtor.join()
consumidor.join() 
