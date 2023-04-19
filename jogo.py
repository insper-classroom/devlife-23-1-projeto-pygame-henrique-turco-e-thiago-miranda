from funcoes import inicializa, desenha, atualiza_estado

window = inicializa()
while atualiza_estado():
    desenha(window)