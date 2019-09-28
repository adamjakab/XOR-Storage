import unittest
import string
import random
from lib.StringReconstructor import StringReconstructor


class StringReconstructorTestCase(unittest.TestCase):
    _test_alphabet = string.digits + string.ascii_letters + string.punctuation
    _generated_input_length = 256
    _number_of_databases = 3

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        # Class init

    def test_something(self):
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()
