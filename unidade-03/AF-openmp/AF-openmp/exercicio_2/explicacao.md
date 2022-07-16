O programa dava erro de timout por usar um chunk de tamanho 1, e isso causava problemas pra as threads porque quando uma 
precisava acessar a região critica as outras threads tinham que esperar para ter esse acesso.

Foi usado uma clausula reduction com operador de soma para poder remover a linha `out[i*cols_right+j] = 0;`. Foi também removida a segunda `diretiva parallel for` já que se mostrava desnecessária. E foi adicionada a clausula collapse na `diretiva parallel for` para expandir a região paralela para os 3 laços de for.
