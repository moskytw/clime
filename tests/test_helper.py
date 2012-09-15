#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from clime.helpers import *

class TestClimeHelper(unittest.TestCase):

    def test_autotype(self):
        cases   = ('string', '100', '100.0', None)
        answers = ('string',  100 ,  100.0 , None)
        for case, answer in zip(cases, answers):
            self.assertEqual(autotype(case), answer)

    def test_getargspec(self):

        docs = [
            None,
            '',
            'abcd',
            'f1()',
            'f2(x)',
            'f3(x, y)',
            'f4(x[, a])',
            'f5(x, y[, a])',
            'f6(x, y[, a[, b]])',
            'f7([a])',
            'f8([a[, b]])',
        ]

        answers = [
            (None, 0),
            (None, 0),
            (None, 0),
            (None, 0),
            (['x'], 0),
            (['x', 'y'], 0),
            (['x', 'a'], 1),
            (['x', 'y', 'a'], 1),
            (['x', 'y', 'a', 'b'], 2),
            (['a'], 1),
            (['a', 'b'], 2),
        ]

        f = type('Dummy', tuple(), {'__doc__': None})()
        trans = lambda x: (x[0], len(x[-1] or []))

        for doc, answer in zip(docs, answers):
            f.__doc__ = doc
            self.assertEqual(trans(getargspec( f )), answer)

    def test_getoptmetas(self):

        doc = """
        -d, --debug                enable debug mode
        -q, -s, --quiet, --slient  enable slient mode
        -n N, --times N            how many times do you want
        """

        answer = [ [('d', None), ('debug', None)],
                   [('q', None), ('s', None), ('quiet', None), ('slient', None)],
                   [('n', 'N'), ('times', 'N')] ]

        self.assertEqual(list(getoptmetas(doc)), answer)

if __name__ == '__main__':
    unittest.main()
