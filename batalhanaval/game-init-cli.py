"""
Jogo Batalha Naval

@authot: Augusto Santos
@version: 1.0

"""

# -*- coding: utf-8 -*-


from batalhanaval.jogospec.jogo_utils import ManipuladorDeArquivos
from batalhanaval.jogospec.batalha_naval import BatalhaNaval

jogadas_p1 = ManipuladorDeArquivos.ler_jogadas('jogador1.txt')
jogadas_p2 = ManipuladorDeArquivos.ler_jogadas('jogador2.txt')

jogo = BatalhaNaval(jogadas_p1, jogadas_p2)
jogo.iniciar_jogo()
