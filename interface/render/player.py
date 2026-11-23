from interface.formatação import descricao_efeito
from utils.carregar_json import carregar_json
from utils.erros import EfeitoInexistenteError
from model.cores import cores_obj as c_obj


def formatar_estados(estados_lista):
    efeitos_json = carregar_json(efeitos=True)["efeitos"]

    for estado in estados_lista:
        if estado.lower() not in efeitos_json:
            raise EfeitoInexistenteError

    return " ".join(
        f"{efeitos_json[estado.lower()].get('cor', c_obj.RESET)}[{estado}]{c_obj.RESET}"
        for estado in estados_lista
    )


def formatar_raridade(dicionario):
    raridade = dicionario["raridade"]

    raridade_cor = {
        "comum": c_obj.PRETO,
        "raro": c_obj.AZUL,
        "epico": c_obj.ROXO,
        "lendario": c_obj.DOURADO,
        "mitico": c_obj.VERMELHO
    }

    return raridade_cor[raridade]


def habilidades_list(player_obj):
    hab_json = player_obj.habilidades_json

    raridades = {
        "comum": [],
        "raro": [],
        "epico": [],
        "lendario": [],
        "mitico": []
    }

    for habilidade in player_obj.habilidades:
        dados = hab_json[habilidade]

        efeito = descricao_efeito(dados)

        texto = (
            f"  ==  {dados['nome']:<28}"
            f"{efeito:<18}"
            f"{'Mana: ' + str(dados['custo_mana']):<10}  ==  "
        )
        raridade = dados["raridade"]
        cor = formatar_raridade(dados)
        texto = cor + texto + c_obj.RESET

        raridades[raridade].append(texto)

    todas = sum(raridades.values(), [])

    return {
        f"l{i}": texto
        for i, texto in enumerate(todas, start=1)
    }
