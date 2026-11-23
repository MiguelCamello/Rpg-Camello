from interface.formatação import slow_print

def mostrar_mensagens(player_obj, inimigo_obj):
    for mensagem in player_obj.mensagens + inimigo_obj.mensagens:
        slow_print(mensagem)

    player_obj.mensagens.clear()
    inimigo_obj.mensagens.clear()