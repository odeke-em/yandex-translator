# coding: utf-8
import os
import sys
import unittest
import importlib

base_dir = os.path.dirname(__file__)
test_dir = os.path.join(base_dir, 'tests')

sys.path.insert(0, test_dir)


def get_suites():
    loader = unittest.TestLoader()
    for file_name in (fname[:-3]
                      for fname in os.listdir(test_dir)
                      if fname.endswith('.py')):
        module = importlib.import_module(file_name)
        yield loader.loadTestsFromModule(module)


def run_tests():
    return unittest.TestSuite(get_suites())
