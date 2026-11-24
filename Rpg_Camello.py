from sistema.escolher_inimigos import escolher_inimigo
from sistema.escolher_habilidade import escolher_habilidade
from sistema.nova_habilidade import nova_habilidade
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

while True:  # loop principal, roda o jogo

    while True:  # loop do menu principal e save
        menu_principal()

        player_obj = menu_saves()

        if player_obj == "voltar":
            continue

        break

    jogando = True

    while jogando:  # loop jogando

        inimigo_obj = escolher_inimigo()

        while inimigo_obj.vivo and player_obj.vivo and jogando:  # loop dos turnos

            # vez do player
            if not player_obj.modificadores["perdeu_vez"]:

                escolhendo_acao = True

                while escolhendo_acao:

                    limpar_terminal()

                    tela_combate(player_obj=player_obj,
                        inimigo_obj=inimigo_obj)

                    slow_print("Qual ação deseja executar?")
                    acao = normalizar_texto(input(" > "))
                    print()

                    if acao == "pause":

                        sair = menu_pause(player_obj)
                        if sair == "sair":
                            jogando = False
                            break

                    if acao == "exp":
                        player_obj.calculo_nivel(int(input(">")))

                    elif acao in ["habilidade", "habilidades"]:  # pra erro ortografico humano
                        try:
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
                            print()

                        except ManaInsuficienteError:
                            espacamento(10)
                            slow_print(
                                f"Mana insuficiente para usar a habilidade - {habilidade} - !", cor=c_obj.DOURADO)
                            time.sleep(2)

                    # pra erro ortografico humano
                    elif acao in ["inventario", "inventarios"]:
                        print("futuras atualizações")
                        time.sleep(1)

                    elif acao in ["descansar", "descansa"]:
                        player_obj.descansar()
                        slow_print(
                            f"{player_obj.nome} descansou e recuperou {c_obj.AZUL}50{c_obj.RESET} de mana!")
                        time.sleep(1)
                        escolhendo_acao = False

                    else:
                        slow_print("Está não é uma ação valida!",
                                cor=c_obj.DOURADO)
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
                print()


            if player_obj.habilidades_pendentes:
                nova_habilidade(player_obj)
                player_obj.habilidades_pendentes = False

            if not player_obj.vivo:
                jogando = False
                continue

            if inimigo_obj.modificadores["perdeu_vez"] and inimigo_obj.vivo:
                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)

                slow_print(
                    f"Por cause de um estado, - {inimigo_obj.nome} - perdeu a vez!")
                time.sleep(1)

            if player_obj.modificadores["perdeu_vez"] and player_obj.vivo:
                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)

                slow_print(
                    f"Por cause de um estado, - {player_obj.nome} - perdeu a vez!")
                time.sleep(1)

            slow_print("Fim do Turno", cor=c_obj.VERDE)
            time.sleep(1)

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
                inimigo_obj.contabilizar_efeitos_continuos(player_obj)
                inimigo_obj.contabilizar_modificadores()
                inimigo_obj.contabilizar_defesa()

                limpar_terminal()
                tela_combate(player_obj, inimigo_obj)

                mostrar_mensagens(player_obj, inimigo_obj)
                time.sleep(1)
