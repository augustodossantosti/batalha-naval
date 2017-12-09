"""

"""

# -*- coding: utf-8 -*-

from collections import Counter
from enum import Enum

from batalhanaval.embarcacoes.embarcacoes import EmbarcacaoFactory
from batalhanaval.jogospec.jogo_utils import ManipuladorDeString, ManipuladorDeArquivos
from batalhanaval.jogospec.jogo_eventos import NotificadorDeEventos, TipoDeEvento, JogadaInvalidaListener, \
    JogadaInvalidaEvento


class Tabuleiro:
    """ A representação do tabuleiro do jogo. """

    TOTAL_DE_LINHAS = 15
    TOTAL_DE_COLUNAS = 15
    INDICE_LINHA = 0
    INDICE_COLUNA = 1

    def __init__(self):
        """ Constroi a matriz que irá representar cada posição do
         tabuleiro. Posteriormente posições especificas da matriz
         irão conter referências as embarcações definidas pelas
         jogadas de cada player. """

        self.matriz = [[None for x in range(self.TOTAL_DE_LINHAS)] for y in range(self.TOTAL_DE_COLUNAS)]

    def posicionar_pecas(self, embarcacoes: list):
        """ Posiciona as embarcações no tabuleiro adicionado referencias
         a elas nas devidas posicoes da matriz. """

        for embarcacao in embarcacoes:
            posicoes_da_embarcacao = []

            for posicao_complementar in range(embarcacao.total_de_posicoes):
                if embarcacao.get_orientacao() == 'V':
                    posicoes_da_embarcacao.append((embarcacao.get_linha() + posicao_complementar,
                                                   embarcacao.get_coluna()))
                else:
                    posicoes_da_embarcacao.append((embarcacao.get_linha(),
                                                   embarcacao.get_coluna() + posicao_complementar))

            for posicao in posicoes_da_embarcacao:
                self.matriz[posicao[self.INDICE_LINHA]][posicao[self.INDICE_COLUNA]] = embarcacao

    def get_embarcacao(self, linha: int, coluna: int):
        """ Retorna a referência para uma embarcação posicionada em
        uma casa especifica no tabuleiro. Caso não haja uma embarcação
        posicionada na casa None será retornado.

        :rtype: Embarcacao | None """

        return self.matriz[linha][coluna]

    def liberar_posicao(self, linha, coluna):
        """ Libera uma determinada casa da matriz que possuia uma embarcação. """

        self.matriz[linha][coluna] = None

    def exibir_posicionamento(self):
        """ Exibe o posicionamento das embarcações em um determinado momento. """

        print('\nTabuleiro: \n')
        print('\n'.join([''.join(['{:5}'.format(item.__str__() if item else '---')
                                  for item in linha]) for linha in self.matriz]))


class ChavePlacar(Enum):
    """"""

    PONTUACAO, ACERTOS, PECAS_PROPRIAS_TOTAIS = range(3)


class Placar:
    """ A representação do placar da partida. """

    def __init__(self):

        self.pontuacao = {'J1': {ChavePlacar.PONTUACAO: 0, ChavePlacar.ACERTOS: 0,
                                 ChavePlacar.PECAS_PROPRIAS_TOTAIS: 13},
                          'J2': {ChavePlacar.PONTUACAO: 0, ChavePlacar.ACERTOS: 0,
                                 ChavePlacar.PECAS_PROPRIAS_TOTAIS: 13}}

    def adicionar_pontuacao(self, pontos: tuple, id_jogador: str):

        if pontos[1] is not False:
            self.pontuacao[id_jogador][ChavePlacar.ACERTOS] += 1

        self.pontuacao[id_jogador][ChavePlacar.PONTUACAO] += pontos[0]

    def get_codigo_vencedor(self) -> str:

        return 'J1' if self.pontuacao['J1'][ChavePlacar.PONTUACAO] \
                       > self.pontuacao['J2'][ChavePlacar.PONTUACAO] else 'J2'

    def get_pontuacao(self, id_jogador: str) -> int:

        return self.pontuacao[id_jogador][ChavePlacar.PONTUACAO]

    def get_total_de_acertos(self, id_jogador: str) -> int:

        return self.pontuacao[id_jogador][ChavePlacar.ACERTOS]

    def get_total_alvos_nao_atingidos(self, id_jogador: str) -> int:

        return self.pontuacao[self.get_jogador_adversario(id_jogador)][ChavePlacar.PECAS_PROPRIAS_TOTAIS] \
               - self.pontuacao[id_jogador][ChavePlacar.ACERTOS]

    def get_jogador_adversario(self, id_jogador: str) -> str:

        for jogador in self.pontuacao:
            if jogador != id_jogador:
                return jogador

    def eh_um_empate(self) -> bool:

        return True if self.pontuacao['J1'][ChavePlacar.PONTUACAO] \
                       == self.pontuacao['J2'][ChavePlacar.PONTUACAO] else False

    def get_placar_final(self) -> str:

        if self.eh_um_empate():

            return '{} {}AA {}AE {}PT\n{} {}AA {}AE {}PT'.format('J1',
                                                                 self.get_total_de_acertos('J1'),
                                                                 self.get_total_alvos_nao_atingidos('J1'),
                                                                 self.get_pontuacao('J1'),
                                                                 'J2',
                                                                 self.get_total_de_acertos('J2'),
                                                                 self.get_total_alvos_nao_atingidos('J2'),
                                                                 self.get_pontuacao('J2'))
        else:

            codigo_vencedor = self.get_codigo_vencedor()
            return '{} {}AA {}AE {}PT'.format(codigo_vencedor, self.get_total_de_acertos(codigo_vencedor),
                                              self.get_total_alvos_nao_atingidos(codigo_vencedor),
                                              self.get_pontuacao(codigo_vencedor))


class BatalhaNaval:
    """ A representação do jogo. """

    COD_ENCOURACADO = 1
    COD_PORTA_AVIOES = 2
    COD_SUBMARINO = 3
    COD_CRUZADOR = 4
    MAX_PECAS_ENCOURACADO = 2
    MAX_PECAS_PORTA_AVIOES = 2
    MAX_PECAS_SUBMARINO = 5
    MAX_PECAS_CRUZADOR = 4
    MAX_DISPAROS = 20
    MIN_LINHA = 0
    MAX_LINHA = 14
    MIN_COLUNA = 0
    MAX_COLUNA = 14

    def __init__(self, jogadas_player1: dict, jogadas_player2: dict):
        self.jogadas_player1 = jogadas_player1
        self.disparos_player1 = self.jogadas_player1.pop('T')
        self.jogadas_player2 = jogadas_player2
        self.disparos_player2 = self.jogadas_player2.pop('T')
        self.placar = Placar()
        self.tabuleiro_p1 = Tabuleiro()
        self.tabuleiro_p2 = Tabuleiro()
        self.notificador_eventos = NotificadorDeEventos({TipoDeEvento.JOGADA_INVALIDA: [JogadaInvalidaListener(self)]})

    def iniciar_jogo(self):
        """ Da inicio a uma partida. """

        self.realizar_verificacoes(self.jogadas_player1, self.disparos_player1, 'J1')
        self.realizar_verificacoes(self.jogadas_player2, self.disparos_player2, 'J2')
        self.posicionar_pecas(self.jogadas_player1, 'J1')
        self.posicionar_pecas(self.jogadas_player2, 'J2')
        self.realizar_disparos(self.disparos_player1, 'J1')
        self.realizar_disparos(self.disparos_player2, 'J2')
        self.verificar_vencedor()

    def realizar_verificacoes(self, jogadas: dict, disparos_player: list, codigo_jogador: str):
        """"""

        embarcacoes = EmbarcacaoFactory.construir_a_partir_de(jogadas, codigo_jogador)

        self.verificar_quantidade_pecas(embarcacoes, codigo_jogador)
        self.verificar_posicoes_pecas(embarcacoes, codigo_jogador)
        self.verificar_sobreposicao(embarcacoes, codigo_jogador)
        self.verificar_quantidade_disparos(disparos_player, codigo_jogador)
        self.verificar_posicoes_disparos(disparos_player, codigo_jogador)

    def posicionar_pecas(self, jogadas: dict, codigo_jogador: str):
        """ Realiza o posicionamento das pecas no tabuleiro após
        realizar as validações conforme regras do jogo. """

        embarcacoes = EmbarcacaoFactory.construir_a_partir_de(jogadas, codigo_jogador)

        tabuleiro = self.tabuleiro_p1 if codigo_jogador == 'J1' else self.tabuleiro_p2
        tabuleiro.posicionar_pecas(embarcacoes)

    def realizar_disparos(self, disparos_player: list, codigo_jogador: str):
        """ Realiza os disparos nas posicoes especificadas, calculando
        a pontuacao obtida pelo jogador. """

        tabuleiro = self.tabuleiro_p2 if codigo_jogador == 'J1' else self.tabuleiro_p1

        for disparo in disparos_player:
            linha = ManipuladorDeString.get_linha_correta(disparo)
            coluna = ManipuladorDeString.get_coluna_correta(disparo)
            embarcacao = tabuleiro.get_embarcacao(linha, coluna)
            if embarcacao:
                self.placar.adicionar_pontuacao(embarcacao.calcular_dano(), codigo_jogador)
                tabuleiro.liberar_posicao(linha, coluna)

    def verificar_quantidade_pecas(self, itens: list, cod_jogador: str):
        """ Verifica se a quantidade de peças definidas para a partida
        é válida. Caso não seja uma mensagem de erro será gravada no
        arquivo de saída e a aplicação será finalizada. """

        counter = Counter(getattr(embarcao, 'codigo') for embarcao in itens)
        if counter[self.COD_ENCOURACADO] != self.MAX_PECAS_ENCOURACADO \
                or counter[self.COD_PORTA_AVIOES] != self.MAX_PECAS_PORTA_AVIOES \
                or counter[self.COD_SUBMARINO] != self.MAX_PECAS_SUBMARINO \
                or counter[self.COD_CRUZADOR] != self.MAX_PECAS_CRUZADOR:

            self.notificador_eventos.notificar_ouvintes(JogadaInvalidaEvento('ERROR_NR_PARTS_VALIDATION', cod_jogador))

    def verificar_quantidade_disparos(self, itens: list, cod_jogador: str):
        """ Verifica se a quantidade de disparos definidas para a partida
        é válida. Caso não seja uma mensagem de erro será gravada no
        arquivo de saída e a aplicação será finalizada. """

        if len(itens) != self.MAX_DISPAROS:
            self.notificador_eventos.notificar_ouvintes(JogadaInvalidaEvento('ERROR_NR_PARTS_VALIDATION', cod_jogador))

    def verificar_sobreposicao(self, embarcacoes: list, cod_jogador: str):
        """ Verifica a ocorrência de sobreposição de peças de um jogador. """

        posicoes_totais = []
        for embarcacao in embarcacoes:
            posicoes_da_embarcacao = []

            for posicao_complementar in range(embarcacao.total_de_posicoes):
                if embarcacao.get_orientacao() == 'V':
                    posicoes_da_embarcacao.append((embarcacao.get_linha() + posicao_complementar,
                                                   embarcacao.get_coluna()))
                else:
                    posicoes_da_embarcacao.append((embarcacao.get_linha(),
                                                   embarcacao.get_coluna() + posicao_complementar))

            for posicao in posicoes_da_embarcacao:
                if posicao not in posicoes_totais:
                    posicoes_totais.append(posicao)
                else:
                    self.notificador_eventos.notificar_ouvintes(
                        JogadaInvalidaEvento('ERROR_OVERWRITE_PIECES_VALIDATION', cod_jogador))

    def verificar_posicoes_pecas(self, posicoes: list, cod_jogador: str):
        """ Verifica se as posições das embarcações são válidas.
        Caso alguma posição inválida seja encontrada uma mensagem
        de erro será gravada no arquivo de saída e a aplicação
        será finalizada. """

        for embarcacao in posicoes:
            linha = embarcacao.get_linha()
            coluna = embarcacao.get_coluna()

            if linha < self.MIN_LINHA \
                    or linha > self.MAX_LINHA \
                    or coluna < self.MIN_COLUNA \
                    or coluna > self.MAX_COLUNA:

                self.notificador_eventos.notificar_ouvintes(
                    JogadaInvalidaEvento('ERROR_POSITION_NONEXISTENT_VALIDATION', cod_jogador))

    def verificar_posicoes_disparos(self, posicoes: list, cod_jogador: str):
        """ Verifica se as posições dos disparos são válidas.
        Caso alguma posição inválida seja encontrada uma mensagem
        de erro será gravada no arquivo de saída e a aplicação
        será finalizada. """

        for posicao in posicoes:
            linha = ManipuladorDeString.get_linha_correta(posicao)
            coluna = ManipuladorDeString.get_coluna_correta(posicao)

            if linha < self.MIN_LINHA \
                    or linha > self.MAX_LINHA \
                    or coluna < self.MIN_COLUNA \
                    or coluna > self.MAX_COLUNA:
                self.notificador_eventos.notificar_ouvintes(
                    JogadaInvalidaEvento('ERROR_POSITION_NONEXISTENT_VALIDATION', cod_jogador))

    def processar_erro(self, mensagem_de_erro: str, id_jogador_responsavel: str):
        """"""

        mensagem_de_saida = '{} {}'.format(id_jogador_responsavel, mensagem_de_erro)
        ManipuladorDeArquivos.escrever_resultado(mensagem_de_saida)
        quit()

    def verificar_vencedor(self):
        """"""

        mensagem_de_saida = self.placar.get_placar_final()
        ManipuladorDeArquivos.escrever_resultado(mensagem_de_saida)
        quit()
