"""
Este módulo contém a definição das especificações do jogo bem
como outras classes e métodos auxiliares para a execução de uma
partida entre dois jogadores.

author: Augusto Santos
version: 1.0

"""

# -*- coding: utf-8 -*-
import os


class ManipuladorDeArquivos:
    """ Fornece métodos de manipulacao de arquivos que
     sejam uteis a aplicação. """

    @staticmethod
    def ler_jogadas(nome_arquivo: str) -> dict:
        """ Realiza a leitura de um arquivo de texto contendo
        todas as jogadas de um determinado player."""

        jogadas = {}
        path_arquivo = os.path.join(os.getcwd() + os.sep + 'resources', nome_arquivo)
        arquivo = open(path_arquivo)
        for linha in arquivo.readlines():
            if linha.startswith('#'):
                pass
            else:
                codigo, jogadas_str = linha.split(';')
                jogadas_str = jogadas_str.strip()
                jogadas_list = jogadas_str.split('|')
                jogadas[codigo] = jogadas_list
        arquivo.close()
        return jogadas

    @staticmethod
    def escrever_resultado(resultado: str):
        """ Cria o arquivo resultados.txt contendo o resultado
        da partida. """

        path_arquivo = os.path.join(os.getcwd() + os.sep + 'resources', 'resultado.txt')
        arquivo = open(path_arquivo, 'w')
        arquivo.write(resultado)
        arquivo.close()


class ManipuladorDeString:
    """ Fornece métodos de manipulacao de strings que
     sejam uteis a aplicação. """

    @staticmethod
    def get_linha_correta(posicao: str) -> int:
        """ Retorna o indice correspondente a linha do tabuleiro.
        Como a letra 'K' não foi considerada no enunciado do
        exercicio é necessário descontar 1 a partir da letra J. """

        linha = ord(posicao[0].lower()) - 97
        if linha < 9:
            return linha
        else:
            return linha - 1

    @staticmethod
    def get_coluna_correta(posicao: str) -> int:
        """ Retorna o indice correspondente a coluna do tabuleiro. """

        return int(posicao[1:]) - 1
