import pandas as pd
import re


def render(table, params):
    col = params['column']
    regex = params['expression']
    newcol = params['newcolumn']

    if not col or not regex or not newcol:
        return table

    try:
        compiled = re.compile(regex)
    except re.error as err:
        return 'Invalid regex: ' + str(err)

    if not compiled.groups:
        return 'Your regex needs a capture group. Add (parentheses) around it.'


    series = table[col]

    # Ensure series is str, overwriting if needed
    # TODO [adamhooper, 2018-12-19] delete this feature: require str input
    try:
        series.str
    except AttributeError:
        strs = series.astype(str)
        strs[series.isna()] = None
        series = strs

    table[newcol] = series.str.extract(compiled, expand=False)[0]
    return table
