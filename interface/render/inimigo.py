from utils.carregar_json import carregar_json
from interface.formatação import normalizar_texto
from model.cores import cores_obj as c_obj

def sprite_dict(inimigo_obj, reset="\033[0m"):
    sprite_raw = inimigo_obj.sprite_dict()
    cor = sprite_raw["cor"]

    return {
        chave: cor + valor + reset
        for chave, valor in sprite_raw.items()
        if chave != "cor"
    }


def drops_dict(inimigo_obj):
    drops_list = []

    for nome, porcentagem in inimigo_obj.drops.items():
        texto = f"= {nome.capitalize():<20}{porcentagem:02d}% ="
        drops_list.append(texto)

    return {
        f"l{linha}": texto
        for linha, texto in enumerate(drops_list, start=1)
    }

def formatar_dificuldade(inimigo_obj):
    dados = carregar_json(inimigo=True)["inimigos"][normalizar_texto(inimigo_obj.nome)]

    dif_cor = {
        "Muito fácil": c_obj.VERDE,
        "Fácil": c_obj.VERDE,
        "Médio": c_obj.DOURADO,
        "Difícil": c_obj.VERMELHO,
        "Muito difícil": c_obj.VERMELHO,
        "Chefe": c_obj.PRETO,
        }
    
    dificuldade = dados["dificuldade"]

    return f"{dif_cor[dificuldade]}{dificuldade}{c_obj.RESET}"