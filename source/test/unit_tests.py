import unittest
import sys

import extract_const_diff
import extract_const_same
import extract_dyn_same
import extract_dyn_diff
import test_phenomenon
import test_propertyset
import test_property


if __name__ == "__main__":

    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_phenomenon))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_propertyset))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_property))

    suite.addTest(unittest.TestLoader().loadTestsFromModule(extract_const_diff))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(extract_const_same))
    # suite.addTest(unittest.TestLoader().loadTestsFromModule(extract_dyn_same))
    # suite.addTest(unittest.TestLoader().loadTestsFromModule(extract_dyn_diff))

    result = unittest.TextTestRunner(verbosity=3).run(suite)
    test_result = (0 if result.wasSuccessful() else 1)

    sys.exit(test_result)
