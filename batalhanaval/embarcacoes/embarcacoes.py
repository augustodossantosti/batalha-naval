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

    def __init__(self, id_embarcacao: int, codigo: int, total_posicoes: int, linha_inicial: int,
                 coluna_inicial: int, orientacao: str, id_jogador: str):
        self.id_embarcacao = id_embarcacao
        self.codigo = codigo
        self.total_de_posicoes = total_posicoes
        self.linha_inicial = linha_inicial
        self.coluna_inicial = coluna_inicial
        self.orientacao = orientacao
        self.id_jogador = id_jogador

    def get_id_embarcacao(self) -> int:
        return self.id_embarcacao

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
            return self.PONTOS_PARCIALMENTE_ABATIDA, self.get_id_embarcacao()
        elif self.total_de_posicoes == 1:
            self.total_de_posicoes -= 1
            return self.PONTOS_TOTALMENTE_ABATIDA, self.get_id_embarcacao()
        else:
            raise RuntimeError('A embarcação já foi destruida!')

    def __str__(self):
        return str(self.get_codigo()) + self.get_id_jogador()

    def __repr__(self):
        return self.__str__()


class Submarino(Embarcacao):
    """ A representação de um Submarino no jogo. """

    def __init__(self, id_embarcacao: int, linha_inicial: int, coluna_inicial: int, id_jogador: str):
        super().__init__(id_embarcacao, 3, 1, linha_inicial, coluna_inicial, 'H', id_jogador)


class Cruzador(Embarcacao):
    """  A representação de um Cruzador no jogo. """

    def __init__(self, id_embarcacao: int, linha_inicial: int, coluna_inicial: int, orientacao: str, id_jogador: str):
        super().__init__(id_embarcacao, 4, 2, linha_inicial, coluna_inicial, orientacao, id_jogador)


class Encouracado(Embarcacao):
    """ A reresentação de um Encouraccado no jogo """

    def __init__(self, id_embarcacao: int, linha_inicial: int, coluna_inicial: int, orientacao: str, id_jogador: str):
        super().__init__(id_embarcacao, 1, 4, linha_inicial, coluna_inicial, orientacao, id_jogador)


class PortaAvioes(Embarcacao):
    """ A representação de um Porta-aviões no jogo """

    def __init__(self, id_embarcacao: int, linha_inicial: int, coluna_inicial: int, orientacao: str, id_jogador: str):
        super().__init__(id_embarcacao, 2, 5, linha_inicial, coluna_inicial, orientacao, id_jogador)


class EmbarcacaoFactory:
    """ Constroi instâncias de Embarcações de acordo com
     o tipo especificado. """

    CODIGO_ENCOURACADO = '1'
    CODIGO_PORTA_AVIOES = '2'
    CODIGO_SUBMARINO = '3'
    CODIGO_CRUZADOR = '4'
    contador_id = 0

    @staticmethod
    def construir_a_partir_de(jogadas: dict, id_jogador: str) -> list:
        """ Constroi as embarcações especificadas no dicionario,
        retornando uma lista das mesmas."""

        embarcacoes = []
        for codigo_embarcacao, emb_specs in jogadas.items():
            for emb_spec in emb_specs:
                if codigo_embarcacao == EmbarcacaoFactory.CODIGO_ENCOURACADO:

                    embarcacoes.append(Encouracado(EmbarcacaoFactory.get_proximo_id(),
                                                   ManipuladorDeString.get_linha_correta(emb_spec[:-1]),
                                                   ManipuladorDeString.get_coluna_correta(emb_spec[:-1]),
                                                   emb_spec[-1], id_jogador))

                elif codigo_embarcacao == EmbarcacaoFactory.CODIGO_PORTA_AVIOES:

                    embarcacoes.append(PortaAvioes(EmbarcacaoFactory.get_proximo_id(),
                                                   ManipuladorDeString.get_linha_correta(emb_spec[:-1]),
                                                   ManipuladorDeString.get_coluna_correta(emb_spec[:-1]),
                                                   emb_spec[-1], id_jogador))

                elif codigo_embarcacao == EmbarcacaoFactory.CODIGO_SUBMARINO:

                    embarcacoes.append(Submarino(EmbarcacaoFactory.get_proximo_id(),
                                                 ManipuladorDeString.get_linha_correta(emb_spec),
                                                 ManipuladorDeString.get_coluna_correta(emb_spec), id_jogador))

                elif codigo_embarcacao == EmbarcacaoFactory.CODIGO_CRUZADOR:

                    embarcacoes.append(Cruzador(EmbarcacaoFactory.get_proximo_id(),
                                                ManipuladorDeString.get_linha_correta(emb_spec[:-1]),
                                                ManipuladorDeString.get_coluna_correta(emb_spec[:-1]),
                                                emb_spec[-1], id_jogador))
                else:
                    raise RuntimeError('Codigo informado na construção da embarcação é inválido!')

        return embarcacoes

    @staticmethod
    def get_proximo_id():
        """ Retorna um numero de identificação unico. """

        EmbarcacaoFactory.contador_id += 1
        return EmbarcacaoFactory.contador_id
