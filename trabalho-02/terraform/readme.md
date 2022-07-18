
## Restrições:
- Foguetes:
    - Se a lua precisa de recursos, o foguete (LION) é enviado para lá
    - Outros Foguetes são enviados aleatóriamente para marte ou para luas de júpiter (se tem recursos)
    - Lion só é enviado da terra para lua
    - Lion pode mandar Combustível (120 unidades) e Urânio (75 unidades) pra lua
    - Foguetes tem ogivas (35 unidades de Urânio) e Combustível baseado no nome e na base de lançamento (conforme tabela)

    |    Foguete/Base    |            Cabo Canaveral            |                Moscou                |                 Alcântara                |             Lua             |
    |:------------------:|:------------------------------------:|:------------------------------------:|:----------------------------------------:|:---------------------------:|
    | Dragon (Explosivo) |     35 Urânio<br>100 Combustível     |     35 Urânio<br>100 Combustível     |        35 Urânio<br>70 Combustível       | 35 Urânio<br>50 Combustível |
    | Falcon (Explosivo) |     35 Urânio <br>120 Combustível    |     35 Urânio<br>120 Combustível     |       35 Urânio<br>100 Combustível       | 35 Urânio<br>90 Combustível |
    |    Lion (Carga)    | 115 Combustível<br>Recursos para lua | 115 Combustível<br>Recursos para lua | 100 Combustível<br><br>Recursos para lua |     NÃO PODE SAIR DA LUA    |

- Bases:
    - Numero maximo de foguetes de cada base:
        - Lua: 2
        - Cabo Canaveral: 5
        - Moscou: 5
        - Alcântara: 1
    - Somente uma base pode pegar Urânio de uma vez
    - Somente uma base pode pegar Combustível de uma vez

- Satelites nos planetas:
    - Serve para dizer se o planeta está habitável ou não, e onde foi bombardeado.
    - Planeta é inabitável? podemos mandar foguetes com ogiva!
    - Planeta é habitavél? não mandamos foguetes!

- Lançamentos e viagens:
    - Foguete para lua (4 dias)
    - Foguete para Marte (2 anos)
    - Foguete para Luas de Júpiter: IO, EUROPA e Ganímedes (5 anos)
    - Foguetes podem falhar no lançamento (perdemos recursos)
    - Foguetes podem falhar durante a viagem (perdemos recursos)

## Arquivos Inalteraveis:
- simulation.py
- mines/oil.py
- mines/oil.py

## Todo:
- [ ] Criar Satelite Endurance dos planetas.
- [ ] Fazer a verificação se o planeta foi bombardeado.
- [ ] Permitir que base analise.
