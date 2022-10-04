#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2021 wakokara
This software is released under the MIT License, see LICENSE.
"""
import unittest

from library.comment_parse import make_send_json, parse_send_message


class MessageTestCase(unittest.TestCase):
    def test_trim_message(self):
        self.assertEqual("HELLOWORLD", parse_send_message(message="HELLOWORLD"))
        self.assertEqual("HELLO␣WORLD", parse_send_message(message="HELLO WORLD"))
        self.assertEqual("HELLO␣WORLD", parse_send_message(message="HELLO　WORLD"))
        self.assertEqual("HELLO␣WORLD", parse_send_message(message="HELLO     WORLD"))
        self.assertEqual("🐷", parse_send_message(message=":pig:"))
        self.assertEqual(None, parse_send_message(message=":youtube:"))
        self.assertEqual("🍣Θ👅Θ🍣", parse_send_message(message="🍣Θ👅Θ🍣"))
        self.assertEqual("🍣🐷HELLO␣WORLD🐷🍣", parse_send_message(message="🍣:pig:HELLO:youtube:WORLD:pig:🍣"))
        self.assertEqual(None, parse_send_message(message='"'))
        self.assertEqual(None, parse_send_message(message="'"))

    def test_sender_message(self):
        t = exec_message(outer="ApexCup01",
                         msg=':pig:')
        self.assertEqual('{from:"YouTube",name:"ApexCup01",text:["🐷"]}',
                         t)

        t = exec_message(outer="ApexCup02",
                         msg='HELLO     WORLD')
        self.assertEqual('{from:"YouTube",name:"ApexCup02",text:["HELLO␣WORLD"]}',
                         t)

        t = exec_message(outer="ApexCup03",
                         msg='🍣:pig:HELLO:youtube:WORLD:pig:🍣')
        self.assertEqual('{from:"YouTube",name:"ApexCup03",text:["🍣🐷HELLO␣WORLD🐷🍣"]}',
                         t)

        t = exec_message(outer="ApexCup04",
                         msg='"')
        self.assertEqual(None, t)

        t = exec_message(outer="ApexCup05",
                         msg="'")
        self.assertEqual(None, t)

        t = exec_message(outer="ApexCup06",
                         msg=':pig:"H:youtube:🍣Θ👅Θ🍣')
        self.assertEqual('{from:"YouTube",name:"ApexCup06",text:["🐷␣H␣🍣Θ👅Θ🍣"]}', t)

    def test_is_answer_message(self):
        # TODO is_answer のテストコードを書く
        pass


def exec_message(outer, msg):
    message = make_send_json(outer, parse_send_message(msg))
    print(message)
    if message is not None:
        print(f"send {outer}: {message} / TRUE")
        return message
    else:
        print(f"send {outer}: {message} / FALSE")


if __name__ == '__main__':
    unittest.main()
