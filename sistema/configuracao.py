from interface.formatação import limpar_terminal, espacamento, normalizar_texto, slow_print
from interface.telas.menu import tela_configuracoes
from utils.resposta import verificar_resposta
from utils.carregar_json import CORES_JSON
from model.cores import cores_obj as c_obj
from utils.erros import OpcaoNaoEncontrada
import json
import time


def configuracao():
    while True:
        limpar_terminal()

        tela_configuracoes()

        espacamento(30)
        slow_print("O'que deseja configurar?")
        
        espacamento(30)
        config = normalizar_texto(input(" > "))

        if config == "voltar":
            return

        elif config == "1":
            limpar_terminal()

            c_obj.teste_de_cores()

            print()
            slow_print("Os numeros listados, são os identificadores da cor")
            input(f"{c_obj.PRETO}[Voltar] {c_obj.RESET}")

        elif config == "2":
            while True:
                try:
                    limpar_terminal()

                    espacamento(30)
                    print(
                        f"{c_obj.PRETO}Preto, {c_obj.VERMELHO}Vermelho, {c_obj.DOURADO}Dourado, {c_obj.VERDE}Verde, {c_obj.AZUL}Azul, {c_obj.ROXO}Roxo{c_obj.RESET}")
                    espacamento(30)
                    slow_print(f"Qual cor deseja alterar?           {c_obj.VERMELHO}[Voltar]{c_obj.RESET}")

                    espacamento(30)
                    cor = normalizar_texto(input(" > "))

                    if cor == "voltar":
                        break

                    cores_dict = c_obj.getAll_codigos()

                    if cor not in cores_dict:
                        raise OpcaoNaoEncontrada

                    espacamento(30)
                    slow_print(f"{cor}: {cores_dict[cor]}")

                    espacamento(30)
                    slow_print("Qual codigo de cor, você quer que sobrescreva o original?")

                    espacamento(30)
                    codigo = input(" > ")
                    codigo = int(codigo)

                    with open(CORES_JSON, "r", encoding="utf-8") as arquivo_cores:
                        cores_json = json.load(arquivo_cores)

                        cores_json["cores"][cor] = codigo

                    with open(CORES_JSON, "w", encoding="utf-8") as arquivo_cores:
                        json.dump(cores_json, arquivo_cores,indent=4, ensure_ascii=False)

                    espacamento(30)
                    slow_print(
                        f"{cor} teve seu código alterado de {cores_dict[cor]} para {codigo} com sucesso!", cor=c_obj.VERDE)
                    time.sleep(1)

                    c_obj.atualizar()
                    break

                except OpcaoNaoEncontrada:
                    espacamento(30)
                    slow_print(f"\"{cor}\" não é uma opção valida!", cor=c_obj.DOURADO)
                    time.sleep(1)

                except ValueError:
                    espacamento(30)
                    slow_print(f"\"{codigo}\" não é um codigo valido! ", cor=c_obj.VERMELHO)
                    time.sleep(1)

        elif config == "3":
            limpar_terminal()

            espacamento(30)
            slow_print("Deseja restaurar as configurações ao estado original?")

            espacamento(30)
            restaurar = normalizar_texto(input(" > "))

            if not verificar_resposta(restaurar):
                espacamento(30)
                slow_print("Cores não restauradas!", cor=c_obj.DOURADO)
                time.sleep(1)
                continue

            with open(CORES_JSON, "r", encoding="utf-8") as arquivo_cores:
                cores_json = json.load(arquivo_cores)

                cores_json['cores'] = cores_json['cores_backup'].copy()

            with open(CORES_JSON, "w", encoding="utf-8") as arquivo_cores:
                json.dump(cores_json, arquivo_cores,indent=4, ensure_ascii=False)

            espacamento(30)
            slow_print("Configurações restauradas com sucesso!",cor=c_obj.VERDE)
            time.sleep(1)

            c_obj.atualizar()

        else:
            espacamento(30)
            slow_print(f"\"{config}\" não é uma opção valida!", cor=c_obj.DOURADO)
            time.sleep(1)
