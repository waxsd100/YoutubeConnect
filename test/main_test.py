#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2021 wakokara
This software is released under the MIT License, see LICENSE.
"""
import unittest

from main import trim_message


class MessageTestCase(unittest.TestCase):
    def test_trim_message(self):
        self.assertEqual("HELLOWORLD", trim_message(message="HELLOWORLD"))
        self.assertEqual("HELLO WORLD", trim_message(message="HELLO WORLD"))
        self.assertEqual("HELLO WORLD", trim_message(message="HELLO　WORLD"))
        self.assertEqual("HELLO WORLD", trim_message(message="HELLO     WORLD"))
        self.assertEqual("🐷", trim_message(message=":pig:"))
        self.assertEqual(" ", trim_message(message=":youtube:"))
        self.assertEqual("🍣Θ👅Θ🍣", trim_message(message="🍣Θ👅Θ🍣"))
        self.assertEqual("🍣🐷HELLO WORLD🐷🍣", trim_message(message="🍣:pig:HELLO:youtube:WORLD:pig:🍣"))
        self.assertEqual("", trim_message(message='"'))
        self.assertEqual("", trim_message(message="'"))

    # m = emoji.emojize(m, use_aliases=True)
    # m = delete_emoji_message(m)
    # m = m.strip('"')
    # m = m.strip("'")


if __name__ == '__main__':
    unittest.main()
