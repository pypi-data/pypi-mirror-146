"""
    test_collada
    ~~~~~~~~~~~~
"""

import unittest

from domonic.xml.collada import *

# import requests
# from mock import patch

# from domonic import domonic

# from domonic.decorators import silence


class TestCase(unittest.TestCase):

    # @silence
    def test_domonic_collada(self):
        col = COLLADA()
        print(col)


if __name__ == '__main__':
    unittest.main()
