import random
import string
import unittest
from itertools import islice, count

from lib.StringReconstructor import StringReconstructor
from lib.StringSplitter import StringSplitter


class ComboTestCase(unittest.TestCase):
    _test_alphabet = string.digits + string.ascii_letters + string.punctuation
    _generated_input_length = 1024
    _number_of_databases = 3

    def test_simple(self):
        input_string = "TEST SIMPLE STRING"
        reconstructed_input = self._get_split_reconstruct_result(input_string, self._number_of_databases)
        self.assertEqual(input_string, reconstructed_input)

    def test_random(self):
        input_string = self._get_random_string()
        reconstructed_input = self._get_split_reconstruct_result(input_string, self._number_of_databases)
        self.assertEqual(input_string, reconstructed_input)

    def test_empty(self):
        input_string = ""
        reconstructed_input = self._get_split_reconstruct_result(input_string, self._number_of_databases)
        self.assertEqual(input_string, reconstructed_input)

    # Needs more extensive checking
    def test_unicode(self):
        input_string = ""
        for i in range(0, int("0x04ff", 16)):
            input_string += chr(i)
        reconstructed_input = self._get_split_reconstruct_result(input_string, self._number_of_databases)
        self.assertEqual(input_string, reconstructed_input)

    def test_multiple_databases(self):
        min_db = self._number_of_databases
        max_db = 6
        for num_db in range(min_db, max_db + 1):
            input_string = self._get_random_string()
            reconstructed_input = self._get_split_reconstruct_result(input_string, num_db)
            self.assertEqual(input_string, reconstructed_input)

    def test_missing_chunk_reconstruction(self):
        min_db = self._number_of_databases
        max_db = 6

        for num_db in range(min_db, max_db + 1):
            # print("-" * 64)
            # This array will tell which chunk to remove during testing (None means no chunks are removed)
            index_array = [None]
            for i in islice(count(), num_db):
                index_array.append(i)

            for chunk_index in index_array:
                # print("TESTING[DB={0}] WITH MISSING CHUNK: {1}".format(num_db, chunk_index))

                input_string = self._get_random_string()
                splitter = StringSplitter(input_string, num_db)
                splitter.split()
                splitter.create_parity()
                chunks = splitter.get_chunks()
                del splitter

                if chunk_index is not None:
                    del chunks[chunk_index]

                reconstructor = StringReconstructor(chunks)
                reconstructor.reconstruct()
                reconstructed_input = reconstructor.get_original_input()

                self.assertEqual(input_string, reconstructed_input)

    def test_zzz_big_1mb(self):
        input_length = 2 ** 20
        input_string = self._get_random_string(input_length)
        reconstructed_input = self._get_split_reconstruct_result(input_string, self._number_of_databases)
        self.assertEqual(input_string, reconstructed_input)

    @staticmethod
    def _get_split_reconstruct_result(input_string="", databases=3):
        splitter = StringSplitter(input_string, databases)
        splitter.split()
        splitter.create_parity()
        chunks = splitter.get_chunks()
        reconstructor = StringReconstructor(chunks)
        reconstructor.reconstruct()
        reconstructed_input = reconstructor.get_original_input()
        return reconstructed_input

    def _get_random_string(self, length=10):
        """Generate a random string of fixed length."""
        return ''.join(random.choice(self._test_alphabet) for i in range(length))


if __name__ == '__main__':
    unittest.main()
