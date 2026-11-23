from model.cores import cores_obj as c_obj


def barra(maximo=1, atual=1, tamanho=10, cor=c_obj.RESET):
    proporcao = max(0, min(atual / maximo, 1))
    barra_prenchida = round(proporcao * tamanho)
    barra_vazia = tamanho - barra_prenchida
    return (cor + "▮" * barra_prenchida + "▯" * barra_vazia + "\033[0m")


def barra_exp(maximo=1, atual=1, nivel=1):
    exp = str(atual)+"/"+str(maximo)
    linhas = {
        "l1": f" {c_obj.VERDE}{" ____":<29}{c_obj.RESET}",
        "l2": f" {c_obj.VERDE}{"|    | Exp":<18}{exp:>8}{c_obj.RESET}{" "*3}",
        "l3": f" {c_obj.VERDE}| {nivel:02d} |{c_obj.RESET}{barra(maximo, atual, 20, c_obj.VERDE):<32}",
        "l4": f" {c_obj.VERDE}{"|____|":<29}{c_obj.RESET}"}
    return linhas


def barra_vida(vd_maxima=1, vd_atual=1, df_base=10, defesa=10):
    vida = str(vd_atual)+"/"+str(vd_maxima)
    df_extra = defesa - df_base
    if df_extra == 0:
        df_extra = ""
    elif df_extra > 0:
        df_extra = f"+{defesa - df_base}"
    elif df_extra < 0:
        df_extra = f"-{abs(defesa - df_base)}"

    linhas = {
        "l1": f"  {c_obj.VERMELHO}{"Vida"}{vida:>14}{c_obj.DOURADO} {"Def"} {df_base:<5}{c_obj.RESET}",
        "l2": f" {barra(vd_maxima, vd_atual, 19, cor=c_obj.VERMELHO)+barra(tamanho=7, cor=c_obj.DOURADO)}   ",
        "l3": f" {" "*22}{c_obj.DOURADO}{df_extra:^5}  {c_obj.RESET}"}
    
    return linhas


def barra_mana(maximo=1, atual=1):
    mana = str(atual)+"/"+str(maximo)
    linhas = {
        "l1": f" {barra(maximo, atual, 16, cor=c_obj.AZUL)} {" "*12}",
        "l2": f"  {c_obj.AZUL}{"Mana"} {mana:>10}{c_obj.RESET}{" "*13}"}
    return linhas
