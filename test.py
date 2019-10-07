import unittest

test_modules = [
    'tests.unit.test_01_string_splitter',
    'tests.unit.test_02_string_reconstructor',
    'tests.unit.test_03_combo',
]

suite = unittest.TestSuite()

for t in test_modules:
    # print("Adding test: {0}".format(t))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner(descriptions=False, verbosity=1, failfast=False).run(suite)
