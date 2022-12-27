from struct import unpack
from unittest import TestCase
import utilities.data as du


def create_string_tuple(string: str):
    return tuple(x for x in string.encode('utf-8'))


class TestToString(TestCase):
    def test_basic_string(self):
        byte_tuple = create_string_tuple('Driver')
        self.assertEqual(du.to_string(byte_tuple), 'Driver')

    def test_with_multi_byte_char(self):
        byte_tuple = create_string_tuple('Pérez')
        self.assertEqual(du.to_string(byte_tuple), 'Pérez')
