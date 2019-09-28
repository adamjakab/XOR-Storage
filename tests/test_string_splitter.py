import unittest
import string
import random
from lib.StringSplitter import StringSplitter


class StringSplitterTestCase(unittest.TestCase):
    _test_alphabet = string.digits + string.ascii_letters + string.punctuation
    _generated_input_length = 256
    _number_of_databases = 3

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        # Class init

    def test__init(self):
        input_string = self.random_string(self._generated_input_length)
        splitter = StringSplitter(input_string, self._number_of_databases)

        self.assertIsInstance(splitter, StringSplitter)
        self.assertEqual(splitter._number_of_databases, self._number_of_databases)
        self.assertEqual(splitter._number_of_chunks, self._number_of_databases - 1)
        self.assertEqual(splitter._input_string, input_string)
        self.assertIsNone(splitter._chunks)
        self.assertIsNone(splitter._chunk_length)

    def test__split(self):
        input_string = self.random_string(self._generated_input_length)
        splitter = StringSplitter(input_string, self._number_of_databases)
        splitter.split()

        self.assertIsNotNone(splitter._chunks)
        self.assertEqual(len(splitter._chunks), self._number_of_databases - 1)
        self.assertGreater(splitter._chunk_length, 0)

        # All chunk should be the same length
        for chunk in splitter._chunks:
            self.assertEqual(len(chunk), splitter._chunk_length)

    def test__create_parity(self):
        input_string = self.random_string(self._generated_input_length)
        splitter = StringSplitter(input_string, self._number_of_databases)
        splitter.split()
        splitter.create_parity()

        # This is quite bad! The 'test__split' test was testing for a different value - this is because parity
        # chunk is added to this list - parity chunk should be stored separately
        self.assertEqual(len(splitter._chunks), self._number_of_databases)

    def test__get_chunks(self):
        input_string = self.random_string(self._generated_input_length)
        splitter = StringSplitter(input_string, self._number_of_databases)

        splitter.split()
        self.assertListEqual(splitter.get_chunks(), splitter._chunks)

        splitter.create_parity()
        self.assertListEqual(splitter.get_chunks(), splitter._chunks)

    def random_string(self, string_length=10):
        """Generate a random string of fixed length """
        return ''.join(random.choice(self._test_alphabet) for i in range(string_length))


if __name__ == '__main__':
    unittest.main()
