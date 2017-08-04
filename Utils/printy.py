__author__ = 'gjy'
from clint.textui import colored, puts, indent


def printy_result(s, status):
        with indent(4, quote='......   '):
            str = '{:.<40}'.format(s)
            if status:
                puts(getattr(colored, 'green')(str + '[OK]'))
            else:
                puts(getattr(colored, 'red')(str + '[ERROR]'))


def printy(s, status):
        colors = ['green', 'white', 'red', 'cyan', 'yellow']
        with indent(4, quote='......   '):
            str = '{:10}'.format(s)
            puts(getattr(colored, colors[status])(str))