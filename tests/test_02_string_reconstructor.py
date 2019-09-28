import random
import string
import unittest

from lib.StringReconstructor import StringReconstructor


class StringReconstructorTestCase(unittest.TestCase):
    _test_alphabet = string.digits + string.ascii_letters + string.punctuation
    _generated_input_length = 256
    _number_of_databases = 3

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        # Class init

    def test__init(self):
        # Number of chunks must be at least 2!
        self.assertRaises(ValueError, StringReconstructor, [])
        self.assertRaises(ValueError, StringReconstructor, ['A'])

        # Number of chunks can be maximum 6!
        self.assertRaises(ValueError, StringReconstructor, ['A', 'B', 'C', 'D', 'E', 'F', 'G'])

        # Default
        chunks = ['A', 'B']
        reconstructor = StringReconstructor(chunks)
        self.assertIsInstance(reconstructor, StringReconstructor)
        self.assertEqual(reconstructor._chunks, chunks)
        self.assertIsNone(reconstructor._reconstructed_chunk)
        self.assertIsNone(reconstructor._parity_bytes)
        self.assertIsNone(reconstructor._original_input)

        # Default 2
        chunks = ['A', 'B', 'C', 'D', 'E']
        reconstructor = StringReconstructor(chunks)
        self.assertEqual(reconstructor._chunks, chunks)
        self.assertIsNone(reconstructor._reconstructed_chunk)
        self.assertIsNone(reconstructor._parity_bytes)
        self.assertIsNone(reconstructor._original_input)
        del reconstructor

        # Chunks should be of the same size + allowed a bigger parity chunk
        chunks = ['A', 'B', 'XXX']
        reconstructor = StringReconstructor(chunks)
        self.assertEqual(reconstructor._chunks, chunks)
        self.assertIsNone(reconstructor._reconstructed_chunk)
        self.assertIsNone(reconstructor._parity_bytes)
        self.assertIsNone(reconstructor._original_input)
        del reconstructor

        # Only two sizes are allowed
        chunks = ['A', 'BB', 'XXX']
        self.assertRaises(ValueError, StringReconstructor, chunks)

        # Too many parity chunks
        chunks = ['A', 'XXX', 'YYY']
        self.assertRaises(ValueError, StringReconstructor, chunks)

    def test__reconstruct(self):
        # Bad chunks should raise ValueError
        chunks = ['A', 'B', 'C']
        reconstructor = StringReconstructor(chunks)
        self.assertRaises(ValueError, reconstructor.reconstruct)
        del reconstructor

        # Bad chunks should raise ValueError #2
        chunks = ['A', 'B', 'XXXXX']
        reconstructor = StringReconstructor(chunks)
        self.assertRaises(ValueError, reconstructor.reconstruct)
        del reconstructor

    def test__get_original_input(self):
        chunks = ['A', 'B', 'C']
        reconstructor = StringReconstructor(chunks)
        self.assertEqual(reconstructor.get_original_input(), reconstructor._original_input)

        changed_input = 'ABC'
        reconstructor._original_input = changed_input
        self.assertEqual(reconstructor.get_original_input(), reconstructor._original_input)

    def random_string(self, string_length=10):
        """Generate a random string of fixed length """
        return ''.join(random.choice(self._test_alphabet) for i in range(string_length))


if __name__ == '__main__':
    unittest.main()
