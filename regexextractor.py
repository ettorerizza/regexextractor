def render(table, params):
    col = params['column']
    regex = params['expression']
    newcol = params['newcolumn']

    if col == '' or regex == '' or newcol == '':
        return table
    else:
        try:
            re.compile(regex)
            is_valid = True
        except re.error:
            is_valid = False

        if not is_valid:
            raise ValueError('Invalid regular expression.')
        elif re.compile(regex).groups != 1:
            raise ValueError('You need to specify one (and only one) capture group in your regular expression.')
        else:
            table[newcol] = table[col].str.extract(regex, expand=True)
            return table
