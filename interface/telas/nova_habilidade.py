from utils.carregar_json import carregar_json
from interface.formatação import centralizar
from interface.render.player import formatar_estados, formatar_raridade
from model.cores import cores_obj as c_obj
import textwrap

espada = [
    r"        /\                ",
    r"  ______||_______         ",
    r" |><><><()       ¨¨¨¨--_  ",
    r"  ¨¨¨¨¨¨||¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ ",
    r"        \/                "
]

def habilidade_card(nova_habilidade): # card com as info do render
    hab_dados = carregar_json(habilidades=True)["habilidades"][nova_habilidade]
    espaco, linha = " "*26, "_"*26

    tipos = hab_dados["tipos"]
    
    tipo1 = f"[{tipos[0]}]" if len(tipos) > 0 else "N/A"
    tipo2 = f"[{tipos[1]}]" if len(tipos) > 1 else ""

    linha_tipos = f"{tipo1} {tipo2}".strip()

    potencia = hab_dados.get("potencia", "N/A")
    cura = hab_dados.get("cura", "N/A")

    efeitos_list = [efeito["nome"] for efeito in hab_dados.get("efeitos", [])]

    if not efeitos_list:
        efeitos = "N/A" 
    else:
        efeitos = formatar_estados(efeitos_list)

    raridade_cor = formatar_raridade(hab_dados)

    descricao = hab_dados['descricao']
    linhas = textwrap.wrap(descricao, width=20)
    linhas = (linhas + [""] * 4)[:4]

    return [
        f"{raridade_cor}  {linha}  {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{espada[0]}| {c_obj.RESET}",
        f"{raridade_cor} |{espada[1]}| {c_obj.RESET}",
        f"{raridade_cor} |{espada[2]}| {c_obj.RESET}",
        f"{raridade_cor} |{espada[3]}| {c_obj.RESET}",
        f"{raridade_cor} |{espada[4]}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{hab_dados["nome"]:^26}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{"-- Tipos --":^26}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{linha_tipos:^26}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{"-- Descrição --":^26}| {c_obj.RESET}",
        f"{raridade_cor} |{espaco}| {c_obj.RESET}",
        f"{raridade_cor} |{linhas[0]:^26}| {c_obj.RESET}",
        f"{raridade_cor} |{linhas[1]:^26}| {c_obj.RESET}",
        f"{raridade_cor} |{linhas[2]:^26}| {c_obj.RESET}",
        f"{raridade_cor} |{linhas[3]:^26}| {c_obj.RESET}",
        f"{raridade_cor} |{linha}| {c_obj.RESET}",
    ]

def tela_nova_habilidade(lista_habilidades):

    card1 = habilidade_card(lista_habilidades[0])
    card2 = habilidade_card(lista_habilidades[1])
    card3 = habilidade_card(lista_habilidades[2])

    linha, espaco = f"|{"="*92}|", f"|{" "*92}|"

    print(f"""
{linha}
|{"-- NOVA HABILIDADE --":^92}|
{linha}
{espaco}""")
    for c1, c2, c3 in zip(card1, card2, card3):
            print(f"| {c1}{c2}{c3} |")
    print(f"""{espaco}
{espaco}
{linha}
""")

tela_nova_habilidade(("estocada", "ira_do_dragao_primordial", "soco_pesado"))