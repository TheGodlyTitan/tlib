import os
import sys

from unittest import (
    TestLoader,
    TextTestRunner,
)
from .result import TestResult


DIRECTORY = "tlib/tlib_tests"

      
def run_tests(package: str = None): 

    test_dir = os.path.join(DIRECTORY, package) if package else DIRECTORY

    loader = TestLoader()
    tests = loader.discover(test_dir)

    if tests.countTestCases() == 0:
        print(f"No tests found in {test_dir}! Check your test files and naming conventions.")
        return

    runner = TextTestRunner(resultclass=TestResultFormatter, verbosity=0)
    runner.run(tests)


# Allow running a specific test package via command-line argument
if __name__ == "__main__":
    package = sys.argv[1] if len(sys.argv) > 1 else None
    run_tests(package)

