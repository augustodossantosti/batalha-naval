"""


"""

# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from enum import Enum


class TipoDeEvento(Enum):
    """ Define os possíveis tipos de erro que podem acontecer no na
    execução do jogo. """

    JOGADA_INVALIDA, FIM_DE_JOGO = range(2)


class Evento(ABC):
    """ Abstração para eventos ocorridos na aplicação. """

    def __init__(self, tipo: TipoDeEvento, mensagem: str, responsavel: str):
        self.tipo = tipo
        self.mensagem = mensagem
        self.responsavel = responsavel

    def get_tipo(self) -> TipoDeEvento:
        """ Retorna o tipo de evento ocorrido. """

        return self.tipo

    def get_mensagem(self) -> str:
        """ Retorna a mensagem que descreve o evento ocorrido. """

        return self.mensagem

    def get_responsavel(self) -> str:
        """ Retorna uma representação do responsável pela ocorrência
        do evento. """

        return self.responsavel


class JogadaInvalidaEvento(Evento):
    """"""

    def __init__(self, mensagem: str, responsavel: str):
        super().__init__(TipoDeEvento.JOGADA_INVALIDA, mensagem, responsavel)


class FimDeJogo(Evento):
    """"""

    def __init__(self, mensagem: str, responsavel: str):
        super().__init__(TipoDeEvento.FIM_DE_JOGO, mensagem, responsavel)


class NotificadorDeEventos:
    """ Contem os tipo de eventos e seus respectivos ouvintes, e é
    responsavel por notifica-los quanto a ocorrencia de eventos."""

    def __init__(self, listeners: dict):
        self.listeners = listeners

    def notificar_ouvintes(self, event: Evento):
        """Notifica todos os ouvintes de um determinado tipo de evento. """

        listeners = self.listeners.get(event.get_tipo())
        if len(listeners) > 0:
            for listener in listeners:
                listener.notify(event)


class AbstractListener(ABC):
    """ Abstração para ouvintes de eventos ocorridos na aplicação. """

    @abstractmethod
    def notify(self, event):
        """ Notifica possiveis interessados sobre a ocorrência de
        um evento na aplicação. """


class JogadaInvalidaListener(AbstractListener):
    """ Escuta eventos relacionados a jogadas invalidas de um player. """

    def __init__(self, batalha_naval):

        self.batalha_naval = batalha_naval

    def notify(self, evento: Evento):

        self.batalha_naval.processar_erro(evento.get_mensagem(), evento.get_responsavel())
