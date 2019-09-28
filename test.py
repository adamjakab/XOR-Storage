import unittest

test_modules = [
    'tests.test_01_string_splitter',
    'tests.test_02_string_reconstructor',
    'tests.test_03_combo',
]

suite = unittest.TestSuite()

for t in test_modules:
    # print("Adding test: {0}".format(t))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner(descriptions=True, verbosity=1, failfast=False).run(suite)
