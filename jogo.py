#loop e atualizacao da tela ensinado por leonardo freitas
from telas import *

tela_atual = TelaInicial()
while True:
    tela_atual.roda()
    tela_atual = tela_atual.update()
