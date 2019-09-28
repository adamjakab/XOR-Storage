import unittest

test_modules = [
    'tests.test_string_reconstructor',
    'tests.test_string_splitter',
]

suite = unittest.TestSuite()

for t in test_modules:
    # print("Adding test: {0}".format(t))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner(descriptions=True, verbosity=1, failfast=False).run(suite)
