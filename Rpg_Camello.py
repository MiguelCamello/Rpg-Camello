from sistema.escolher_inimigos import escolher_inimigo
from sistema.escolher_habilidade import escolher_habilidade
from sistema.menu_principal import menu_principal
from sistema.menu_pause import menu_pause
from sistema.menu_saves import menu_saves
from interface.telas.combate import tela_combate

from interface.formatação import limpar_terminal, slow_print, normalizar_texto, espacamento
from model.cores import cores_obj as c_obj

from database.criar_todas_tabelas import criar_todas_tabelas

from utils.mostrar_mensagens import mostrar_mensagens
from utils.erros import *

import time

criar_todas_tabelas()

while True: # loop principal, roda o jogo

    while True: # loop do menu principal e save
        menu_principal()

        player_obj = menu_saves()

        if player_obj == "voltar":
            continue

        break

    jogando = True

    while jogando: # loop jogando

        inimigo_obj = escolher_inimigo()

        while inimigo_obj.vivo and player_obj.vivo and jogando:  # loop dos turnos

            # vez do player
            if not player_obj.modificadores["perdeu_vez"]:

                escolhendo_acao = True

                while escolhendo_acao:

                    limpar_terminal()

                    tela_combate(player_obj=player_obj, inimigo_obj=inimigo_obj)

                    slow_print("Qual ação deseja executar?")
                    acao = normalizar_texto(input(" > "))

                    if acao == "pause":

                        sair = menu_pause(player_obj)
                        if sair == "sair":
                            jogando = False
                            break

                    elif acao in ["habilidade", "habilidades"]:  # pra erro ortografico humano

                        habilidade = escolher_habilidade(player_obj)

                        if habilidade == "voltar" or not habilidade:
                            continue

                        limpar_terminal()
                        tela_combate(player_obj, inimigo_obj)
                        time.sleep(0.5)

                        player_obj.usar_habilidade(
                            habilidade_req=habilidade,
                            alvo=inimigo_obj
                        )
                        limpar_terminal()
                        tela_combate(player_obj, inimigo_obj)

                        mostrar_mensagens(player_obj, inimigo_obj)

                        escolhendo_acao = False

                        input("[continuar]")

                    elif acao in ["item", "items", "iten", "itens"]:  # pra erro ortografico humano
                        print("futuras atualizações")
                        time.sleep(1)

                    elif acao in ["descansar", "descansa"]:
                        player_obj.descansar()
                        slow_print(
                            f"{player_obj.nome}, descansou e recuperou {c_obj.AZUL}50{c_obj.RESET} de mana!")
                        time.sleep(1)
                        escolhendo_acao = False

                    else:
                        slow_print("Está não é uma ação valida!", cor=c_obj.DOURADO)
                        time.sleep(1)


            # vez do inimigo
            if inimigo_obj.vivo and player_obj.vivo and jogando and not inimigo_obj.modificadores["perdeu_vez"]:
                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)
                time.sleep(0.5)

                inimigo_obj.atacar(player_obj)

                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)

                mostrar_mensagens(player_obj, inimigo_obj)

                input("[continuar]")

            if inimigo_obj.modificadores["perdeu_vez"]:
                espacamento(10)
                slow_print(f"Por cause de um estado, - {inimigo_obj.nome} - perdeu a vez!")

            if player_obj.modificadores["perdeu_vez"]:
                espacamento(10)
                slow_print(f"Por cause de um estado, - {player_obj.nome} - perdeu a vez!")

            if not player_obj.vivo:
                espacamento(10)
                slow_print("Você foi derrotado!", cor=c_obj.VERMELHO)
                espacamento(10)
                input("[continuar]")

            if inimigo_obj.vivo and player_obj.vivo and jogando:
                player_obj.finalizar_turno()
                player_obj.contabilizar_efeitos_continuos()
                player_obj.contabilizar_modificadores()
                player_obj.contabilizar_defesa()

                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)
                
                mostrar_mensagens(player_obj, inimigo_obj)
                time.sleep(1)

                inimigo_obj.finalizar_turno()
                inimigo_obj.contabilizar_efeitos_continuos()
                inimigo_obj.contabilizar_modificadores()
                inimigo_obj.contabilizar_defesa()

                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)

                mostrar_mensagens(player_obj, inimigo_obj)
                time.sleep(1)