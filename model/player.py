from sistema.nova_habilidade import nova_habilidade
from interface.formatação import slow_print
from utils.sorteio import sortear_habilidades
from utils.erros import *
from model.cores import cores_obj as c_obj
import random as rm
import time


class Player:
    def __init__(self,
                 efeitos_json,
                 habilidades_json,
                 nome,
                 estados=[],
                 nivel=1,
                 exp_necessario=200,
                 exp=0,
                 mana_maxima=100,
                 mana=100,
                 vida_maxima=150,
                 vida=150,
                 defesa_base=10,
                 defesa=10,
                 itens={},
                 habilidades=None
                 ):
        self.efeitos_json = efeitos_json
        self.habilidades_json = habilidades_json
        self.nome = nome

        self.estados = estados

        efeitos_ativos = {}
        for estado in self.estados:
            efeitos_ativos[estado] = self.efeitos_json[estado].get(
                "duracao_turnos")

        self.modificadores = {
            "mod_dano": 0,
            "mod_defesa": 0,
            "perdeu_vez": False
        }

        self.efeitos_ativos = efeitos_ativos

        self.nivel = nivel
        self.exp_necessario = exp_necessario
        self.exp = exp
        self.mana_maxima = mana_maxima
        self.mana = mana
        self.vida_maxima = vida_maxima
        self.vida = vida
        self.defesa_base = defesa_base
        self.defesa = defesa
        self.inventario = itens

        if habilidades is None:
            habilidades_possiveis = [
                hab for hab, dados in habilidades_json.items() if dados["raridade"] == "comum"]
            self.habilidades = rm.sample(habilidades_possiveis, 3)
        else:
            self.habilidades = [hab.lower() for hab in habilidades]

        self.mensagens = []

    # vivo morto descanso

    @property
    def vivo(self):
        return self.vida > 0

    def morrer(self, atacante):
        self.mensagens.append(
            f"{c_obj.VERMELHO}Você morreu para - {atacante} -{c_obj.RESET}")
        time.sleep(1)
        # vou fazer penalidade

    def descansar(self):
        self.mana = min(
            self.mana_maxima,
            self.mana + 50
        )

    # estados

    def tomou_estado(self, estado):
        if estado in self.estados:
            return

        self.estados.append(estado)
        self.efeitos_ativos[estado] = self.efeitos_json[estado].get(
            "duracao_turnos")

        self.contabilizar_modificadores()
        self.contabilizar_defesa()

        self.mensagens.append(
            f"{c_obj.DOURADO}Você recebeu o efeito - {estado} -")

    def contabilizar_modificadores(self):
        self.modificadores = {
            "mod_dano": 0,
            "mod_defesa": 0,
            "perdeu_vez": False
        }

        for efeito in list(self.efeitos_ativos):
            efeito_dados = self.efeitos_json[efeito]
            tipo = efeito_dados["tipo"]

            if tipo == "controle":
                self.modificadores["perdeu_vez"] = True

            if tipo in ["debuff", "buff"]:
                if "modificador_dano" in efeito_dados:
                    self.modificadores["mod_dano"] += efeito_dados["modificador_dano"]

                if "defesa_por_turno" in efeito_dados:
                    self.modificadores["mod_defesa"] += efeito_dados["defesa_por_turno"]

    def contabilizar_efeitos_continuos(self):
        for efeito in list(self.efeitos_ativos):
            efeito_dados = self.efeitos_json[efeito]
            tipo = efeito_dados["tipo"]

            if tipo in ["dano_continuo", "cura_continua"]:
                vida = self.vida + efeito_dados["dano_por_turno"]
                self.vida = max(0, (min(self.vida_maxima, vida)))
            if tipo == "dano_continuo":
                self.mensagens.append(
                    f"Você recebeu {abs(efeito_dados["dano_por_turno"])} de dano devido ao efeito {efeito}")
            if tipo == "cura_continuo":
                self.mensagens.append(
                    f"Você recebeu {efeito_dados["dano_por_turno"]} de cura devido ao efeito {efeito}")

    def contabilizar_defesa(self):
        self.defesa = self.defesa_base

        self.defesa += self.modificadores["mod_defesa"]

    def finalizar_turno(self):
        for efeito in list(self.efeitos_ativos):

            self.efeitos_ativos[efeito] -= 1

            if self.efeitos_ativos[efeito] <= 0:

                del self.efeitos_ativos[efeito]

                self.estados.remove(efeito)

                slow_print(f"Efeito {efeito} se esvaiu!")
                time.sleep(1)

    # level up

    def calculo_habilidades(self):
        NIVEIS_HABILIDADES = [
            2, 4, 6, 9, 12, 16, 20
        ]
        if self.nivel in NIVEIS_HABILIDADES or self.nivel % 20 == 0:
            hab_sorteadas = sortear_habilidades(self, self.habilidades_json)
            nova_habilidade(self, hab_sorteadas)

    def calculo_lvlUp(self):
        nivel = self.nivel - 1

        self.exp_necessario = 200 + (nivel * 50) + (nivel ** 2 * 10)

        self.vida_maxima = 150 + (nivel * 20)
        self.mana_maxima = 100 + (nivel * 12)
        self.defesa_base = 10 + round(nivel * 1.2)

        # Restaura vida e mana e defesa
        self.defesa = self.defesa_base
        self.vida = self.vida_maxima
        self.mana = self.mana_maxima

    def ganhou_exp(self, exp):
        if exp <= 0:
            print("Esse valor de exp é invalido!")
            return
        self.exp += exp

        while self.exp >= self.exp_necessario:
            self.exp -= self.exp_necessario
            self.nivel += 1
            self.calculo_lvlUp()

    # itens

    def ganhou_item(self, item, quantia=1):
        if item not in self.inventario:
            self.inventario[item] = quantia
            return
        self.inventario[item] += quantia

    # habilidades

    def tomou_dano(self, habilidade_tomada, modificador, atacante):
        dano_base = habilidade_tomada["potencia"]
        dano_modificado = dano_base * (1 + modificador / 100)
        penetracao_defesa = habilidade_tomada.get("penetracao_defesa", 0)
        ignorar_defesa = habilidade_tomada.get("ignorar_defesa", False)

        if ignorar_defesa:
            defesa_aplicada = 0
        else:
            defesa_aplicada = self.defesa * (
                1 - penetracao_defesa / 100
            )

        dano_final = max(0, round(dano_modificado - defesa_aplicada))

        estava_vivo = self.vivo

        self.vida = max(0, self.vida - dano_final)

        if estava_vivo and not self.vivo:
            self.morrer(atacante)

    def ganhou_habilidade(self, habilidade_adquirida):
        habilidade_adquirida = habilidade_adquirida.lower()

        if habilidade_adquirida not in self.habilidades_json:
            raise HabilidadeInexistenteError
        if habilidade_adquirida in self.habilidades:
            return print(f"{self.nome} Ganhou uma habilidade repetida!")

        self.habilidades.append(habilidade_adquirida)

    def deletar_habilidade(self, habilidade_del):
        habilidade_del = habilidade_del.lower()

        if habilidade_del not in self.habilidades:
            raise HabilidadeNaoAdquiridaError

        self.habilidades.remove(habilidade_del)

    def habilidades_disponiveis(self):
        return [hab for hab in self.habilidades if self.habilidades_json[hab]["custo_mana"] <= self.mana]

    def contabilizar_habilidade(self, alvo, habilidade_req):
        habilidade = self.habilidades_json[habilidade_req]

        if "dano" in habilidade["tipos"]:
            alvo.tomou_dano(habilidade, self.modificadores["mod_dano"], self)

        if "cura" in habilidade["tipos"]:
            self.vida = min(self.vida_maxima, self.vida + habilidade["cura"])

        if "efeito" in habilidade["tipos"]:
            for efeito in habilidade["efeitos"]:
                if efeito["alvo"] == "proprio":
                    self.tomou_estado(efeito["nome"])
                elif efeito["alvo"] == "inimigo":
                    alvo.tomou_estado(efeito["nome"])

        self.mana -= habilidade["custo_mana"]

    def usar_habilidade(self, alvo, habilidade_req):
        habilidade_req = habilidade_req.lower()

        if habilidade_req not in self.habilidades_json:
            raise HabilidadeInexistenteError(
                f"A habilidade {habilidade_req} não existe no jogo!")

        if habilidade_req not in self.habilidades:
            raise HabilidadeNaoAdquiridaError(
                f"Você não possui a habilidade {habilidade_req}!")

        # comparador morsa := cria variavel e usa na comparação em 1 linha
        if not (hab_disp := self.habilidades_disponiveis()):
            raise ManaInsuficienteError(
                "Você não possui mana suficiente para nenhuma habilidade!")

        if habilidade_req not in hab_disp:
            raise ManaInsuficienteError(
                "Você não possui mana suficiente para está habilidade!")

        self.mensagens.append(
            f"{self.nome} usou a habilidade - {habilidade_req} - !")

        self.contabilizar_habilidade(alvo, habilidade_req)
