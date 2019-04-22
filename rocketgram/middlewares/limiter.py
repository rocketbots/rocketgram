# Copyright (C) 2015-2019 by Vd.
# This file is part of RocketGram, the modern Telegram bot framework.
# RocketGram is released under the MIT License (see LICENSE).


import typing
from time import monotonic

if typing.TYPE_CHECKING:
    from ..bot import Bot
    from ..context import Context

from .middleware import EmptyMiddleware
from ..errors import RocketgramStopRequest


class LimiterMiddleware(EmptyMiddleware):
    """\
    This middleware pass no more than `quantity` messages per `period` seconds.
    """

    __slots__ = ('__quantity', '__period', '__values')

    def __init__(self, quantity: int, period: float):
        self.__quantity = quantity
        self.__period = period
        self.__values = dict()

    def shutdown(self, bot: 'Bot'):
        bot_id = id(bot)
        if bot_id in self.__values:
            del self.__values[bot_id]

    def process(self, context: 'Context') -> 'Context':
        bot_id = id(context.bot)
        current = monotonic()
        d = current - self.__period

        self.__values[bot_id] = [v for v in self.__values.get(bot_id, list()) if v > d]

        if len(self.__values[bot_id]) >= self.__quantity:
            raise RocketgramStopRequest(f'Update `{context.update.update_id}` was dropped due to '
                                        f'rate exceed `{self.__quantity}` msg per `{self.__period}` secs.')

        self.__values[bot_id].append(current)

        return context