from interface.formatação import limpar_terminal, espacamento, normalizar_texto, slow_print
from interface.telas.lista_habilidades import tela_lista_habilidades
from interface.telas.inspect_habilidade import tela_inspect_habilidade
from model.cores import cores_obj as c_obj

from utils.resposta import verificar_resposta
from utils.carregar_json import carregar_json
from utils.erros import *
import time


def escolher_habilidade(player_obj):

    escolhendo_hab = True
    while escolhendo_hab:  # escolha de habilidade para se usar
        try:
            limpar_terminal()
            tela_lista_habilidades(player_obj)

            espacamento(10)  # pra centralizar
            slow_print("Que habilidade deseja usar?")

            espacamento(10)  # pra centralizar
            habilidade = normalizar_texto(input(" > "))

            if habilidade == "voltar":
                return habilidade

            if habilidade not in carregar_json(habilidades=True)["habilidades"]:
                raise HabilidadeInexistenteError

            if habilidade not in player_obj.habilidades:
                raise HabilidadeNaoAdquiridaError
            

            limpar_terminal()
            tela_inspect_habilidade(habilidade)

            espacamento(10)
            slow_print("Deseja usar está habilidade?")

            espacamento(10)
            resposta = normalizar_texto(input(" > "))

            if not verificar_resposta(resposta):
                espacamento(10)
                slow_print(f"Habilidade - {habilidade.capitalize()} - não usada!", cor=c_obj.DOURADO)
                time.sleep(1)
                continue

            return habilidade

        except HabilidadeNaoAdquiridaError:
            espacamento(10)
            slow_print(f"Você não possui a habilidade - {habilidade} - !", cor=c_obj.DOURADO)
            time.sleep(2)
        except HabilidadeInexistenteError:
            espacamento(10)
            slow_print(f"\"{habilidade}\" não é uma habilidade valida!", cor=c_obj.DOURADO)
            time.sleep(2)
