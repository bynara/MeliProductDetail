#!/usr/bin/env python3
"""
Test runner for Frontend tests
Run all tests in the frontend test suite
"""

import unittest
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all test modules
from test_login_service import TestLoginService
from test_product_service import TestProductService
from test_review_service import TestReviewService
from test_seller_service import TestSellerService
from test_app import TestApp


def create_test_suite():
    """Create and return a test suite with all frontend tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases - all should work now
    suite.addTest(loader.loadTestsFromTestCase(TestLoginService))
    suite.addTest(loader.loadTestsFromTestCase(TestProductService))
    suite.addTest(loader.loadTestsFromTestCase(TestReviewService))
    suite.addTest(loader.loadTestsFromTestCase(TestSellerService))
    suite.addTest(loader.loadTestsFromTestCase(TestApp))
    
    return suite


def run_tests():
    """Run all frontend tests and return the result"""
    print("=" * 70)
    print("RUNNING FRONTEND TESTS")
    print("=" * 70)
    
    # Create test suite
    suite = create_test_suite()
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
