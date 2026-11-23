from utils.carregar_json import carregar_json
from model.inimigo import Inimigo
from model.player import Player


def criar_inimigo(nome):
    dados = carregar_json(inimigo=True, habilidades=True, sprites=True, efeitos=True)
    return Inimigo(
        inimigo_json=dados["inimigos"][nome],
        habilidades_json=dados["habilidades"],
        sprites_json=dados["sprites"],
        efeitos_json=dados["efeitos"],
        )

def criar_player(nome, **resto):
    dados = carregar_json(habilidades=True, efeitos=True)
    try:
        return Player(
            nome=nome,
            efeitos_json=dados["efeitos"],
            habilidades_json=dados["habilidades"],
            **resto
        )
    except:
        print("Deu erro ai!")
