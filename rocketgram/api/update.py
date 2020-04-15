# Copyright (C) 2015-2020 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import Dict, Optional

from .callback_query import CallbackQuery
from .chosen_inline_result import ChosenInlineResult
from .inline_query import InlineQuery
from .message import Message
from .poll import Poll
from .poll_answer import PollAnswer
from .pre_checkout_query import PreCheckoutQuery
from .shipping_query import ShippingQuery
from .update_type import UpdateType


@dataclass(frozen=True)
class Update:
    """\
    Represents Update object:
    https://core.telegram.org/bots/api#update

    Additional fields:
    raw
    update_type
    """

    raw: Dict
    update_id: int
    update_type: UpdateType
    message: Optional[Message]
    edited_message: Optional[Message]
    channel_post: Optional[Message]
    edited_channel_post: Optional[Message]
    inline_query: Optional[InlineQuery]
    chosen_inline_result: Optional[ChosenInlineResult]
    callback_query: Optional[CallbackQuery]
    shipping_query: Optional[ShippingQuery]
    pre_checkout_query: Optional[PreCheckoutQuery]
    poll: Optional[Poll]
    poll_answer: Optional[PollAnswer]

    @classmethod
    def parse(cls, data: Dict) -> 'Update':
        message = Message.parse(data.get('message'))
        edited_message = Message.parse(data.get('edited_message'))
        channel_post = Message.parse(data.get('channel_post'))
        edited_channel_post = Message.parse(data.get('edited_channel_post'))
        inline_query = InlineQuery.parse(data.get('inline_query'))
        chosen_inline_result = ChosenInlineResult.parse(data.get('chosen_inline_result'))
        callback_query = CallbackQuery.parse(data.get('callback_query'))
        shipping_query = ShippingQuery.parse(data.get('shipping_query'))
        pre_checkout_query = PreCheckoutQuery.parse(data.get('pre_checkout_query'))
        poll = Poll.parse(data.get('poll'))
        poll_answer = PollAnswer.parse(data.get('poll_answer'))

        update_type = None
        if message:
            update_type = UpdateType.message
        elif edited_message:
            update_type = UpdateType.edited_message
        elif channel_post:
            update_type = UpdateType.channel_post
        elif edited_channel_post:
            update_type = UpdateType.edited_channel_post
        elif inline_query:
            update_type = UpdateType.inline_query
        elif chosen_inline_result:
            update_type = UpdateType.chosen_inline_result
        elif callback_query:
            update_type = UpdateType.callback_query
        elif shipping_query:
            update_type = UpdateType.shipping_query
        elif pre_checkout_query:
            update_type = UpdateType.pre_checkout_query
        elif poll:
            update_type = UpdateType.poll
        elif poll_answer:
            update_type = UpdateType.poll_answer

        assert update_type is not None, "Should have value here! This probably means api was changed."

        return cls(data, data['update_id'], update_type, message, edited_message, channel_post, edited_channel_post,
                   inline_query, chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll,
                   poll_answer)
