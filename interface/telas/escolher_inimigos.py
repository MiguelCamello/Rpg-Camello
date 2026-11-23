from interface.render.inimigo import sprite_dict, formatar_dificuldade
from interface.render.barras import barra
from interface.formatação import centralizar
from model.cores import cores_obj as c_obj

def inimigo_card_render(inimigo_obj): # renderiza as info do card
    sprite = sprite_dict(inimigo_obj)
    vida = str(inimigo_obj.vida)+"/"+str(inimigo_obj.vida_maxima)
    mana = str(inimigo_obj.mana)+"/"+str(inimigo_obj.mana_maxima)

    return [
        # sprite
        centralizar(sprite.get("l1", ""), 24),
        centralizar(sprite.get("l2", ""), 24),
        centralizar(sprite.get("l3", ""), 24),
        centralizar(sprite.get("l4", ""), 24),
        centralizar(sprite.get("l5", ""), 24),

        # dificuldade
        centralizar(formatar_dificuldade(inimigo_obj), 24),

        # vida
        centralizar(f" {c_obj.VERMELHO}{"Vida"}{vida:>10}{c_obj.DOURADO} {"Def"} {inimigo_obj.defesa}{c_obj.RESET}", 24),
        centralizar(f"{barra(inimigo_obj.vida_maxima, inimigo_obj.vida, 15, cor=c_obj.VERMELHO)+barra(tamanho=7, cor=c_obj.DOURADO)}", 24),

        # mana
        centralizar(f"{barra(inimigo_obj.mana_maxima, inimigo_obj.mana, 18, cor=c_obj.AZUL)}", 24),
        centralizar(f" {c_obj.AZUL}{"Mana"}   {mana:>10}{c_obj.RESET}", 24)
    ]

def inimigo_card(inimigo_obj): # card com as info do render
    nome = centralizar(f"{c_obj.DOURADO}{("- " + inimigo_obj.nome + " -"):^24}{c_obj.RESET}",24)
    espaco, linha = " "*24, "_"*24
    linhas = inimigo_card_render(inimigo_obj)

    return [
        f"{linha:^30}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{centralizar("|"+nome+"|", 30)}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{centralizar("|"+ linhas[0] +"|",30)}",
        f"{centralizar("|"+ linhas[1] +"|",30)}",
        f"{centralizar("|"+ linhas[2] +"|",30)}",
        f"{centralizar("|"+ linhas[3] +"|",30)}",
        f"{centralizar("|"+ linhas[4] +"|",30)}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{centralizar("|"+ linhas[5] +"|", 30)}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{centralizar("|"+ linhas[6] +"|", 30)}",
        f"{centralizar("|"+ linhas[7] +"|", 30)}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{centralizar("|"+ linhas[8] +"|", 30)}",
        f"{centralizar("|"+ linhas[9] +"|", 30)}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{("|"+(espaco)+"|"):^30}",
        f"{("|"+linha+"|"):^30}",
    ]

def tela_escolher_inimigos(lista_inimigos_obj, rerolls):

    card1 = inimigo_card(lista_inimigos_obj[0])
    card2 = inimigo_card(lista_inimigos_obj[1])
    card3 = inimigo_card(lista_inimigos_obj[2])

    linha, espaco = f"|{"="*92}|", f"|{" "*92}|"

    print(f"""
{linha}
|{"-- INIMIGOS --":^92}|
{linha}
{espaco}""")
    for c1, c2, c3 in zip(card1, card2, card3):
            print(f"| {c1}{c2}{c3} |")
    print(f"""{espaco}
{espaco}
|{c_obj.VERDE}   [Reroll]   [{rerolls}]{c_obj.RESET}{"":^75}|
{espaco}
{linha}
""")