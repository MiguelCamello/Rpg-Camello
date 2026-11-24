from interface.formatação import limpar_terminal, slow_print, normalizar_texto
from interface.telas.inspect_habilidade import tela_inspect_habilidade
from interface.telas.nova_habilidade import tela_nova_habilidade
from utils.resposta import verificar_resposta
from utils.sorteio import sortear_habilidades
from model.cores import cores_obj as c_obj

from utils.erros import *
import time


def nova_habilidade(player_obj):
    hab_sorteadas = sortear_habilidades(
            player_obj, player_obj.habilidades_json
        )

    limpar_terminal()
    slow_print(f"Voce pode aprender novas habilidades!", cor=c_obj.VERDE)

    while True:
        time.sleep(1)

        limpar_terminal()
        tela_nova_habilidade(hab_sorteadas)

        try:
            slow_print("Qual destas habilidades deseja aprender?")
            hab = normalizar_texto(input(" > "))

            if hab not in hab_sorteadas:
                raise OpcaoNaoEncontrada

            limpar_terminal()
            tela_inspect_habilidade(hab)

            slow_print("Você deseja aprender está habilidade?")

            if verificar_resposta(input(" > ")):
                player_obj.ganhou_habilidade(hab)

                slow_print(
                    f"{player_obj.nome} aprendeu a habilidade {hab}!", cor=c_obj.VERDE)
                time.sleep(1)
                return

        except OpcaoNaoEncontrada:
            slow_print("Está habilidade não consta nas opção!",cor=c_obj.DOURADO)
            time.sleep(1)
        except HabilidadeInexistenteError:
            slow_print("Está habilidade não existe!", cor=c_obj.VERMELHO)
            time.sleep(1)
