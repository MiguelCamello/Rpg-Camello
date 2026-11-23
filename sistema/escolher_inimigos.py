
from interface.telas.escolher_inimigos import tela_escolher_inimigos
from interface.formatação import limpar_terminal, slow_print, normalizar_texto

from utils.criar_classe import criar_inimigo
from utils.carregar_json import carregar_json
from utils.erros import *

from model.cores import cores_obj as c_obj

import time
import random


def escolher_inimigo():
    rerolls = 3
    while True:
            limpar_terminal()

            lista_inimigos = random.sample(
                list(carregar_json(inimigo=True)["inimigos"]), k=3)

            lista_inimigos_obj = []
            for inimigo in lista_inimigos:
                inimigo = criar_inimigo(inimigo)
                lista_inimigos_obj.append(inimigo)

            while True:
                try:
                    limpar_terminal()
                    tela_escolher_inimigos(lista_inimigos_obj, rerolls)

                    slow_print("Deseja lutar com qual inimigo?")

                    inimigo_nome = normalizar_texto(input(" > "))

                    if inimigo_nome == "reroll":
                        if rerolls <= 0:
                            slow_print("Você não tem mais rerolls! Se vira")
                            time.sleep(1)
                            continue

                        rerolls -= 1
                        break

                    if inimigo_nome not in carregar_json(inimigo=True)["inimigos"]:
                        raise InimigoInexistenteError

                    if inimigo_nome not in lista_inimigos:
                        raise OpcaoNaoEncontrada

                    inimigo_obj = criar_inimigo(nome=inimigo_nome)
                    return inimigo_obj

                except InimigoInexistenteError:
                    slow_print(f"\"{inimigo_nome}\" não é uma opção valida!", cor=c_obj.DOURADO)
                    time.sleep(2)
                except OpcaoNaoEncontrada:
                    slow_print(f"\"{inimigo_nome}\" não consta nas opções!", cor=c_obj.DOURADO)