from multiprocessing import Process, Queue

def origem(fila1):
  for i in range(10):
    msg = 'Teste ' + str(i)
    # envia mensagem para a ponte pela fila 1
    fila1.put(msg)
    print('[origem] Mensagem enviada fila1: ', msg)

def ponte(fila1, fila2):
  for _ in range(10):
    # recebe mensagem na fila 1
    fila2.put(fila1.get())
    print('[ponte] Mensagem recebida fila1 e enviada fila2')

def destino(fila2):
  for _ in range(10):
    # recebe mensagem na fila 2
    msg = fila2.get()
    print('[destino] Mensagem recebida fila2: ', msg)

if __name__ == '__main__':
  fila1 = Queue()
  fila2 = Queue()
  o = Process(target=origem, args=(fila1,))
  p = Process(target=ponte, args=(fila1,fila2,))
  d = Process(target=destino, args=(fila2,))

  # executa os processos
  o.start()
  p.start()
  d.start()

  # aguarda conclusão
  o.join()
  p.join()
  d.join()

  # libera as filas
  fila1.close()
  fila2.close()

  # fila1.join_thread()
  # fila2.join_thread()