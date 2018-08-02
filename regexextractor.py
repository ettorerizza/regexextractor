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
            # Non-object types cast string "NaN" when None, remove first
            if table[col].dtype.name != 'category' and table[col].dtype.name != 'object':
                table[newcol] = table[col].fillna('').astype(str).str.extract(regex, expand=True)
            # Same issue with 'int' categorical dtypes, must add '' to categories (copy) first
            elif table[col].dtype.name == 'category':
                if any(pd.isna(table[col])):
                    table[newcol] = table[col].copy().cat.add_categories('').fillna('').astype(str).str.extract(regex, expand=True)
                else:
                    table[newcol] = table[col].astype(str).str.extract(regex, expand=True)
            else:
                table[newcol] = table[col].str.extract(regex, expand=True)
            return table
