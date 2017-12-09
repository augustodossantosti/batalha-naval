"""

EP final de Algoritmos

Banco de dados - 1º semestre - Noite - 2017
Professor: Lucas Nadalete

Aluno: Francilei Augusto dos Santos

Data: 12-11-17
Versão: 1.0

"""

# -*- coding: utf-8 -*-


from batalhanaval.jogospec.jogo_utils import ManipuladorDeArquivos
from batalhanaval.jogospec.batalha_naval import BatalhaNaval

jogadas_p1 = ManipuladorDeArquivos.ler_jogadas('jogador1.txt')
jogadas_p2 = ManipuladorDeArquivos.ler_jogadas('jogador2.txt')

jogo = BatalhaNaval(jogadas_p1, jogadas_p2)
jogo.iniciar_jogo()
