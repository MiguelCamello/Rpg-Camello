def verificar_resposta(variavel):
    if variavel in ["sim", "ss", "s", "y", "yes", "claro"]:
        return True
    elif variavel in ["nao", "nn", "n", "negativo", ""]:
        return False
    else:
        return False