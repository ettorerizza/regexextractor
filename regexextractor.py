import pandas as pd
import re

class Importable:
    @staticmethod
    def __init__(self):
        pass

    @staticmethod
    def event():
        pass

    @staticmethod
    def render(wf_module, table):
        col = wf_module.get_param_string('column')
        regex = wf_module.get_param_string('expression')
        newcol = wf_module.get_param_string('newcolumn')

        try:
            re.compile(regex)
            is_valid = True
        except re.error:
            is_valid = False

        if not is_valid:
            wf_module.set_error('Invalid regular expression.')
            return None
        elif re.compile(regex).groups != 1:
            wf_module.set_error('You need to specify one (and only one) capture group in your regular expression.')
            return None
        else:
            table[newcol] = table[col].str.extract(regex, expand=True)
            wf_module.set_ready(notify=False)
            return table