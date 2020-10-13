# tests/runner.py
import unittest

# import your test modules
import test_application

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_application))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=4)
result = runner.run(suite)
