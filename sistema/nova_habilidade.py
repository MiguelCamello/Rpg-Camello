from interface.formatação import limpar_terminal, slow_print, normalizar_texto
from model.cores import cores_obj as c_obj

from utils.erros import *
import time


def nova_habilidade(player_obj, hab_sorteadas):
    while True:
        limpar_terminal()

        slow_print(f"Voce pode aprender novas habilidades! \n", cor=c_obj.VERDE)
        try:
            if hab_sorteadas:
                print(", ".join(hab_sorteadas))
                slow_print("Qual destas habilidades deseja aprender?")
                hab = normalizar_texto(input(" > "))

                if hab not in hab_sorteadas:
                    raise OpcaoNaoEncontrada

                player_obj.ganhou_habilidade(hab)
                slow_print(
                    f"{player_obj.nome} aprendeu a habilidade {hab}!", cor=c_obj.VERDE)
                time.sleep(1)
                return

        except OpcaoNaoEncontrada:
            slow_print("Está habilidade não consta nas opção!",
                    cor=c_obj.DOURADO)
            time.sleep(1)
        except HabilidadeInexistenteError:
            slow_print("Está habilidade não existe!", cor=c_obj.VERMELHO)
            time.sleep(1)
