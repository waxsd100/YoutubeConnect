#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2021 wakokara
This software is released under the MIT License, see LICENSE.
"""

import enum


@enum.unique
class ChatType(enum.Enum):
    SUPER_CHAT = "superChat"
    TEXT_MESSAGE = "textMessage"
    SUPER_STICKER = "superSticker"
    NEW_SPONSOR = "newSponsor"
    GIFT_REDEMPTION = "giftRedemption"
    GIFT_PURCHASE = "giftPurchase"
