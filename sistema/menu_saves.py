from database.salvar import obter_players, deletar_player, carregar_player, salvar_player
from model.cores import cores_obj as c_obj
from interface.formatação import limpar_terminal, normalizar_texto, slow_print
from interface.telas.saves import tela_saves
from utils.resposta import verificar_resposta
from utils.criar_classe import criar_player
import time

def menu_saves():    
    while True:
        limpar_terminal()
        
        saves = obter_players()

        tela_saves(saves)

        slow_print("Oque deseja fazer?")
        acao = normalizar_texto(input(" > "))
        print()

        if acao == "voltar":
            return acao

        elif acao in ["deletar_save","deletar_jogo", "deletar"]:

            slow_print("Qual deseja deletar?: Save 1, Save 2, Save 3")
            delete = normalizar_texto(input(" > "))

            if delete == "voltar":
                continue

            if delete not in ["save_1", "save_2", "save_3"]:
                slow_print(f"\"{delete}\" não é uma opção valida!", cor=c_obj.DOURADO)
                time.sleep(1)
                continue

            delete = int(delete.split("_")[1])

            if delete > len(saves):
                slow_print(f"O Slot {delete} está vazio!", cor=c_obj.DOURADO)
                time.sleep(1)
                continue

            delete -= 1

            slow_print(f"Será apagado todos os dados deste save!!", cor=c_obj.VERMELHO)
            slow_print(f"Você tem certeza que deseja deletar o save - {saves[delete]['nome']} - ?", cor=c_obj.VERMELHO)

            if verificar_resposta(input(" > ")):
                deletar_player(saves[delete]['id'])

                slow_print("Save deletado com sucesso!", cor=c_obj.VERDE)
                time.sleep(1)

        elif acao in ["novo_save", "novo_jogo", "novo"]:

            if len(saves) >= 3:
                slow_print("Você já criou o maximo de saves!", cor=c_obj.DOURADO)
                time.sleep(2)
                continue

            while True:
                slow_print("Qual será o nome do seu personagem?")
    
                nome_jogador = input(" > ").title().strip()

                nomes = [dado['nome'] for dado in saves]

                if nome_jogador in nomes:
                    print("Já existe um save com este nome, escolha outro\n")
                    continue
    
                slow_print(f"Está contente com - {nome_jogador} - ?")
    
                if verificar_resposta(input(" > ")):
                    break


            slow_print(f"Save - {nome_jogador} - criado com sucesso!", cor=c_obj.VERDE)
            time.sleep(1)

            player = criar_player(nome=nome_jogador)

            id_salvo = salvar_player(player)
            player.id = id_salvo

            return player

        elif acao in ["carregar_save", "carregar_jogo", "carregar"]:
            slow_print("Qual deseja carregar?: Save 1, Save 2, Save 3")
            select = normalizar_texto(input(" > "))
            print()

            if select == "voltar":
                continue

            if select not in ["save_1", "save_2", "save_3"]:
                slow_print(f"\"{select}\" não é uma opção valida!", cor=c_obj.DOURADO)
                time.sleep(1)
                continue

            select = int(select.split("_")[1])

            if select > len(obter_players()):
                slow_print("Este slot está vazio! volte e digite novo jogo pra criar novo save!", cor= c_obj.DOURADO)
                slow_print("volte e use novo jogo pra criar novo save!", cor=c_obj.DOURADO)
                time.sleep(2)
                continue

            select -= 1

            slow_print(f"O save - {saves[select]['nome']} - é o desejado?")
            desejado = input(" > ")
            print()

            if verificar_resposta(desejado):
                slow_print(f"Save - {saves[select]['nome']} - carregado com sucesso!", cor=c_obj.VERDE)
                time.sleep(1)

                player = carregar_player(saves[select]["id"])
                player.id = saves[select]["id"]

                return player

        else:
            slow_print("Está não é uma opção valida!", cor=c_obj.DOURADO)
            time.sleep(1)