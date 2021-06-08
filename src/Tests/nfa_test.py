import unittest
from unittest.main import main

from StringComparison.comparator import comparison
from Errors.log import Log

class TestNfaConstruction(unittest.TestCase):
    # Tests for Nfa 


    def __init__(self, *args, **kwargs):
        super(TestNfaConstruction, self).__init__(*args, **kwargs)

    # Correct usage
    def test_basic_re_one_correct_string(self):
        re = '1*'
        strings = ['111']
        logs = []
        pred_outpt = [True]

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt)

    def test_basic_re_one_incorrect_string(self):
        re = '1*'
        strings = ['110']
        logs = []
        pred_outpt = [False]

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt)

    def test_basic_re_multi_correct_string(self):
        re = '1*'
        strings = ['111', '1']
        logs = []
        pred_outpt = [True, True]

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt)

    def test_basic_re_multi_incorrect_string(self):
        re = '1*'
        strings = ['110', '0xa']
        logs = []
        pred_outpt = [False, False]

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt)

    def test_basic_re_multi__string(self):
        re = '1*.(0|a)*.x'
        strings = ['110ax', 'aaaax', '1111xx']
        logs = []
        pred_outpt = [True, True, False]

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt) 

    # Errors
    def test_e10(self):
        re = '1*/a'
        strings = ['111']
        logs = []
        err = 'e10'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e11(self):
        re = '1*a|c)'
        strings = ['110']
        logs = []
        err = 'e11'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e12(self):
        re = '1*(a|c'
        strings = ['111']
        logs = []
        err = 'e12'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e13(self):
        re = '+1*'
        strings = ['111']
        logs = []
        err = 'e13'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)
    
    def test_e14(self):
        re = '1*a.|c'
        strings = ['111']
        logs = []
        err = 'e14'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e15(self):
        re = '1(*a.|)c'
        strings = ['111']
        logs = []
        err = 'e15'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e16(self):
        re = '1.*a'
        strings = ['110']
        logs = []
        err = 'e16'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e17(self):
        re = '1*+'
        strings = ['111']
        logs = []
        err = 'e17'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    def test_e30(self):
        re = '1*'
        strings = ['11*1']
        logs = []
        err = 'e30'

        with self.assertRaises(Log) as cm:
            comparison(re, strings, logs)
        self.assertEqual(cm.exception.err_code, err)

    # Warnings
    def test_w10(self):
        re = '1* xa'
        strings = ['111']
        logs = []
        pred_outpt = [True]
        warn = 'w10'

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt)
        self.assertEqual(warn, logs[0].err_code)


    def test_w30(self):
        re = '1*'
        strings = [' ']
        logs = []
        pred_outpt = [True]
        warn = 'w30'

        self.assertEqual(comparison(re, strings, logs)[0], pred_outpt)
        self.assertEqual(warn, logs[0].err_code)


        