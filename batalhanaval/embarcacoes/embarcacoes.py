"""
Este módulo contém a definição das embarcações presentes no jogo bem
como outras classes e métodos auxiliares para facilitar o seu uso.

author: Augusto Santos
version: 1.0

"""

# -*- coding: utf-8 -*-

from abc import ABC

from batalhanaval.jogospec.jogo_utils import ManipuladorDeString


class Embarcacao(ABC):
    """ Abstração para os diferentes tipos de embarcações
     presentes no jogo. """

    PONTOS_PARCIALMENTE_ABATIDA = 3
    PONTOS_TOTALMENTE_ABATIDA = 5

    def __init__(self, codigo: int, total_de_posicoes: int, posicao_inicial: str, orientacao: str, id_jogador: str):
        self.codigo = codigo
        self.total_de_posicoes = total_de_posicoes
        self.linha_inicial = ManipuladorDeString.get_linha_correta(posicao_inicial)
        self.coluna_inicial = ManipuladorDeString.get_coluna_correta(posicao_inicial)
        self.orientacao = orientacao
        self.id_jogador = id_jogador
        self.foi_atingida = False

    def get_codigo(self) -> int:
        return self.codigo

    def get_posicoes(self) -> int:
        return self.total_de_posicoes

    def get_linha(self) -> int:
        return self.linha_inicial

    def get_coluna(self) -> int:
        return self.coluna_inicial

    def get_orientacao(self) -> str:
        return self.orientacao

    def get_id_jogador(self) -> str:
        return self.id_jogador

    def calcular_dano(self) -> tuple:
        """ Calcula o dano do disparo recebido, retornando
        o total de pontos a serem atribuidos ao jogador
        adversário. """

        if self.total_de_posicoes > 1:
            self.total_de_posicoes -= 1
            if self.foi_atingida:
                return self.PONTOS_PARCIALMENTE_ABATIDA, False
            else:
                self.foi_atingida = True
                return self.PONTOS_PARCIALMENTE_ABATIDA, True
        elif self.total_de_posicoes == 1:
            self.total_de_posicoes -= 1
            if self.foi_atingida:
                return self.PONTOS_TOTALMENTE_ABATIDA, False
            else:
                self.foi_atingida = True
                return self.PONTOS_TOTALMENTE_ABATIDA, True
        else:
            raise RuntimeError('A embarcação já foi destruida!')

    def __str__(self):
        return str(self.get_codigo()) + self.get_id_jogador()

    def __repr__(self):
        return self.__str__()


class Submarino(Embarcacao):
    """ A representação de um Submarino no jogo. """

    def __init__(self, posicao_inicial: str, id_jogador: str):
        super().__init__(3, 1, posicao_inicial, 'H', id_jogador)


class Cruzador(Embarcacao):
    """  A representação de um Cruzador no jogo. """

    def __init__(self, posicao_inicial: str, orientacao: str, id_jogador: str):
        super().__init__(4, 2, posicao_inicial, orientacao, id_jogador)


class Encouracado(Embarcacao):
    """ A reresentação de um Encouraccado no jogo """

    def __init__(self, posicao_inicial: str, orientacao: str, id_jogador: str):
        super().__init__(1, 4, posicao_inicial, orientacao, id_jogador)


class PortaAvioes(Embarcacao):
    """ A representação de um Porta-aviões no jogo """

    def __init__(self, posicao_inicial: str, orientacao: str, id_jogador: str):
        super().__init__(2, 5, posicao_inicial, orientacao, id_jogador)


class EmbarcacaoFactory:
    """ Constroi instâncias de Embarcações de acordo com
     o tipo especificado. """

    @staticmethod
    def construir_a_partir_de(jogadas: dict, id_jogador: str) -> list:
        """ Constroi as embarcações especificadas no dicionario,
        retornando uma lista das mesmas."""

        embarcacoes = []
        for key, value in jogadas.items():
            for emb_spec in value:
                if key == '1':
                    embarcacoes.append(Encouracado(emb_spec[:-1], emb_spec[-1], id_jogador))
                elif key == '2':
                    embarcacoes.append(PortaAvioes(emb_spec[:-1], emb_spec[-1], id_jogador))
                elif key == '3':
                    embarcacoes.append(Submarino(emb_spec, id_jogador))
                else:
                    embarcacoes.append(Cruzador(emb_spec[:-1], emb_spec[-1], id_jogador))

        return embarcacoes
