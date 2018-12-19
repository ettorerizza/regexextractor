import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import numpy as np
from regexextractor import render


class TestRegexExtractor(unittest.TestCase):
    def test_defaults_nop(self):
        out = render(pd.DataFrame({'A': [1, 2]}), {
            'column': '',
            'expression': '',
            'newcolumn': ''
        })
        assert_frame_equal(out, pd.DataFrame({'A': [1, 2]}))

    def test_no_column_nop(self):
        out = render(pd.DataFrame({'A': [1, 2]}), {
            'column': '',
            'expression': r'(\w)',
            'newcolumn': 'B'
        })
        assert_frame_equal(out, pd.DataFrame({'A': [1, 2]}))

    def test_no_newcolumn_nop(self):
        out = render(pd.DataFrame({'A': [1, 2]}), {
            'column': 'A',
            'expression': r'(\w)',
            'newcolumn': ''
        })
        assert_frame_equal(out, pd.DataFrame({'A': [1, 2]}))

    def test_no_expression_nop(self):
        out = render(pd.DataFrame({'A': ['a', 'b']}), {
            'column': 'A',
            'expression': '',
            'newcolumn': ''
        })
        assert_frame_equal(out, pd.DataFrame({'A': ['a', 'b']}))

    def test_string_match(self):
        out = render(pd.DataFrame({'A': ['abc', 'def']}), {
            'column': 'A',
            'expression': r'(\w{2})',
            'newcolumn': 'B',
        })
        assert_frame_equal(out, pd.DataFrame({
            'A': ['abc', 'def'],
            'B': ['ab', 'de'],
        }))

    def test_no_match_is_nan(self):
        out = render(pd.DataFrame({'A': ['abc', 'def']}), {
            'column': 'A',
            'expression': r'a(\w{2})',
            'newcolumn': 'B',
        })
        assert_frame_equal(out, pd.DataFrame({
            'A': ['abc', 'def'],
            'B': ['bc', None],
        }))

    def test_num(self):
        # converts number to strings, NaN if no result?
        # TODO [adamhooper, 2018-12-19] delete this feature: require str input
        out = render(pd.DataFrame({'A': [1, np.nan, 2000.1]}), {
            'column': 'A',
            'expression': r'(\d)',
            'newcolumn': 'B',
        })
        assert_frame_equal(out, pd.DataFrame({
            'A': [1, np.nan, 2000.1],
            'B': ['1', None, '2'],
        }))

    def test_categories(self):
        out = render(pd.DataFrame({'A': ['abc', 'def']}, dtype='category'), {
            'column': 'A',
            'expression': r'(\w{2})',
            'newcolumn': 'B',
        })
        expected = pd.DataFrame({
            'A': ['abc', 'def'],
            'B': ['ab', 'de'],
        })
        # Implementation detail: output is never 'category'.
        expected['A'] = expected['A'].astype('category')
        assert_frame_equal(out, expected)

    def test_overwrite_col(self):
        out = render(pd.DataFrame({'A': ['abc', 'def']}), {
            'column': 'A',
            'expression': r'(\w{2})',
            'newcolumn': 'A',
        })
        assert_frame_equal(out, pd.DataFrame({'A': ['ab', 'de']}))

    def test_invalid_regex_syntax_error(self):
        out = render(pd.DataFrame({'A': ['a', 'b']}), {
            'column': 'A',
            'expression': r'([x)',
            'newcolumn': 'B',
        })
        self.assertEqual(
            out,
            'Invalid regex: unterminated character set at position 1'
        )

    def test_invalid_regex_missing_group_captures_all(self):
        out = render(pd.DataFrame({'A': ['ab', 'cb']}), {
            'column': 'A',
            'expression': r'[ab]',
            'newcolumn': 'B',
        })
        self.assertEqual(
            out,
            'Your regex needs a capture group. Add (parentheses) around it.'
        )

    def test_invalid_regex_too_many_groups(self):
        out = render(pd.DataFrame({'A': ['a', 'b']}), {
            'column': 'A',
            'expression': r'([ab])([cd])',
            'newcolumn': 'B',
        })
        self.assertEqual(
            out,
            'Workbench only supports one (capture group). Remove '
            'some parentheses.'
        )


if __name__ == '__main__':
    unittest.main()
