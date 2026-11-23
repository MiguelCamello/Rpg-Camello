from interface.formatação import limpar_terminal, espacamento, normalizar_texto, slow_print
from interface.telas.menu import tela_creditos, tela_menu_principal
from sistema.configuracao import configuracao
from utils.resposta import verificar_resposta
from model.cores import cores_obj as c_obj
import time
import sys


def menu_principal():
    menu_aberto = True
    while menu_aberto:
        limpar_terminal()

        tela_menu_principal()

        espacamento(30)
        slow_print("O'que deseja fazer?")

        espacamento(30)
        acao = normalizar_texto(input(" > "))

        if acao == "jogar":
            return

        elif acao in ["configuracao", "configuracoes"]:
            configuracao()

        elif acao in ["creditos", "credito"]:
            limpar_terminal()

            tela_creditos()

            espacamento(30)
            input("[Voltar] ")

        elif acao == "sair":
            limpar_terminal()

            espacamento(30)
            slow_print("Tem certeza que deseja sair do jogo?")

            espacamento(30)
            sair = normalizar_texto(input(" > "))

            if verificar_resposta(sair):
                limpar_terminal()
                sys.exit()

        else:
            espacamento(30)
            slow_print("Está não é uma opção valida!", cor=c_obj.DOURADO)
            time.sleep(1)