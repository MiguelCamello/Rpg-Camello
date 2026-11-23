from utils.erros import SpriteInexistenteError
from utils.sorteio import sortear_quantidade, sortear_drops
from interface.formatação import slow_print
from model.cores import cores_obj as c_obj
import random as rm
import time

class Inimigo:
    def __init__(self, inimigo_json, habilidades_json, sprites_json, efeitos_json):
        self.habilidades_json = habilidades_json
        self.sprites_json = sprites_json
        self.efeitos_json = efeitos_json
        self.sprite = inimigo_json["sprite"]
        self.nome = inimigo_json["nome"]
        self.estados = []

        self.efeitos_ativos = {}

        self.modificadores = {
            "mod_dano": 0,
            "mod_defesa": 0,
            "perdeu_vez": False
        }

        self.mana_maxima = inimigo_json["mana"]
        self.mana = inimigo_json["mana"]
        self.vida_maxima = inimigo_json["vida"]
        self.vida = inimigo_json["vida"]
        self.defesa_base = inimigo_json["defesa"]
        self.defesa = inimigo_json["defesa"]
        self.exp_drop = inimigo_json["exp_drop"]
        self.drops = inimigo_json["drops"]

        habilidades_possiveis = inimigo_json["habilidades_possiveis"]

        if len(habilidades_possiveis) <= 3:
            quantidade = len(habilidades_possiveis)
        else:
            quantidade = sortear_quantidade(len(habilidades_possiveis))

        self.habilidades = rm.sample(habilidades_possiveis, quantidade)

        self.mensagens = []

    # vivo morto descanso

    @property
    def vivo(self):
        return self.vida > 0

    def morrer(self, atacante):
        self.mensagens.append(f"{c_obj.VERDE}{self.nome} foi morto por {atacante.nome}!{c_obj.RESET}")

        atacante.ganhou_exp(self.exp_drop)

        self.mensagens.append(f"{c_obj.VERDE}{atacante.nome} ganhou {self.exp_drop} de exp!{c_obj.RESET}")

        for item, chance in self.drops.items():
            if sortear_drops(chance):
                atacante.ganhou_item(item)
                self.mensagens.append(f"{c_obj.VERDE}{atacante.nome} ganhou {item}!{c_obj.RESET}")

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
        self.efeitos_ativos[estado] = self.efeitos_json[estado].get("duracao_turnos")

        self.contabilizar_modificadores()
        self.contabilizar_defesa()

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
                self.mensagens.append(f"O Inimigo recebeu {abs(efeito_dados["dano_por_turno"])} de dano devido ao efeito {efeito}")
            if tipo == "cura_continuo":
                self.mensagens.append(f"O Inimigo recebeu {efeito_dados["dano_por_turno"]} de cura devido ao efeito {efeito}")

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

    def habilidades_disponiveis(self):
        return [hab for hab in self.habilidades if self.habilidades_json[hab]["custo_mana"] <= self.mana]

    def atacar(self, alvo): # é aleatoria
        if not (habilidades_disponiveis := self.habilidades_disponiveis()): # := cria var e usa na comparação na msm linha
            self.descansar()
            return

        habilidade_req = rm.choice(habilidades_disponiveis)
        habilidade = self.habilidades_json[habilidade_req]

        self.mensagens.append(f"{self.nome} usou a habilidade - {habilidade['nome']} - !")

        if "dano" in habilidade["tipos"]:
            alvo.tomou_dano(habilidade,self.modificadores["mod_dano"], self)

        if "cura" in habilidade["tipos"]:
            self.vida = min(self.vida_maxima, self.vida + habilidade["cura"])

        if "efeito" in habilidade["tipos"]:
            for efeito in habilidade["efeitos"]:
                if efeito["alvo"] == "proprio":
                    self.tomou_estado(efeito["nome"])
                elif efeito["alvo"] == "inimigo":
                    alvo.tomou_estado(efeito["nome"])

        self.mana -= habilidade["custo_mana"]

    def sprite_dict(self):
        if self.sprite not in self.sprites_json:
            raise SpriteInexistenteError
        return self.sprites_json[self.sprite]