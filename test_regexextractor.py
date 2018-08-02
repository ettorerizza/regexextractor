import unittest
import pandas as pd
import numpy as np
from regexextractor import render

class TestRegexExtractor(unittest.TestCase):

    def setUp(self):
        # Test data includes:
        #  - rows of numeric and string types
        #  - zero entries (which should not be removed)
        #  - some partially and some completely empty rows
        self.table = pd.DataFrame([
            ['workbench!!!!',      2,      3.14,       '@workbench',     1.0],
            ['.workbench!',    5,		None,		'.workbench!',    2.0],
            ['[workbench]', -10, 	None, 	    '$data!',    None],
            ['workbench',        -2,		10.0,			'data!!!',     3.0],
            ['@workbench.com',		8,		0.0,			'@workbench.com',    4.0]],
            columns=['stringcol','intcol','floatcol','catcol','floatcatcol'])

        # Pandas should infer these types anyway, but leave nothing to chance
        self.table['stringcol'] = self.table['stringcol'].astype(str)
        self.table['intcol'] = self.table['intcol'].astype(np.int64)
        self.table['floatcol'] = self.table['floatcol'].astype(np.float64)
        self.table['catcol'] = self.table['catcol'].astype('category')
        self.table['floatcatcol'] = self.table['floatcatcol'].astype('category')

    def test_NOP(self):
        params = { 'column': '', 'expression': '[^\w\s]', 'newcolumn': 'newcol'}
        out = render(self.table, params)
        self.assertTrue(out.equals(self.table)) # should NOP when first applied

        params = {'column': 'stringcol', 'expression': '[^\w\s]', 'newcolumn': ''}
        out = render(self.table, params)
        self.assertTrue(out.equals(self.table))  # should NOP when first applied

        params = {'column': 'stringcol', 'expression': '', 'newcolumn': 'newcol'}
        out = render(self.table, params)
        self.assertTrue(out.equals(self.table))  # should NOP when first applied

    def test_string(self):
        params = {'column': 'stringcol', 'expression': '([\w\s]+)', 'newcolumn': 'newcol'}
        out = render(self.table.copy(), params)
        ref = self.table
        ref['newcol'] = pd.Series(['workbench', 'workbench', 'workbench', 'workbench', 'workbench'])
        pd.testing.assert_frame_equal(out, ref)

    def test_num(self):
        # converts number to strings, NaN if no result?
        params = {'column': 'floatcol', 'expression': '([\w\s]+)', 'newcolumn': 'newcol'}
        out = render(self.table.copy(), params)
        ref = self.table
        ref['newcol'] = pd.Series(['3', np.nan, np.nan, '10', '0'])
        pd.testing.assert_frame_equal(out, ref)

    def test_num_expect_none(self):
        # converts number to strings, NaN if no result?
        params = {'column': 'intcol', 'expression': '([a-z]+)', 'newcolumn': 'newcol'}
        out = render(self.table.copy(), params)
        ref = self.table
        ref['newcol'] = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan], dtype=object)
        pd.testing.assert_frame_equal(out, ref)

    def test_cat(self):
        params = {'column': 'catcol', 'expression': '([\w\s]+)', 'newcolumn': 'newcol'}
        out = render(self.table.copy(), params)
        ref = self.table
        ref['newcol'] = pd.Series(['workbench', 'workbench', 'data', 'data', 'workbench'])
        pd.testing.assert_frame_equal(out, ref)

    def test_cat_num(self):
        params = {'column': 'floatcatcol', 'expression': '([\w\s]+)', 'newcolumn': 'newcol'}
        out = render(self.table.copy(), params)
        ref = self.table
        ref['newcol'] = pd.Series(['1', '2', np.nan, '3', '4'])
        pd.testing.assert_frame_equal(out, ref)

    def test_overwrite_col(self):
        params = {'column': 'stringcol', 'expression': '([\w\s]+)', 'newcolumn': 'stringcol'}
        out = render(self.table.copy(), params)
        ref = self.table
        ref['stringcol'] = pd.Series(['workbench', 'workbench', 'workbench', 'workbench', 'workbench'])
        pd.testing.assert_frame_equal(out, ref)

    def test_regex_error(self):
        # invalid regex expression
        params = {'column': 'stringcol', 'expression': '#@55[\w\s]+!!!)', 'newcolumn': 'stringcol'}
        with self.assertRaises(ValueError):
            render(self.table.copy(), params)

        # multiple groups
        params = {'column': 'stringcol', 'expression': '[\w\s]', 'newcolumn': 'stringcol'}
        with self.assertRaises(ValueError):
            render(self.table.copy(), params)

if __name__ == '__main__':
    unittest.main()


