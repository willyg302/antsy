import sys
import unittest

import antsy


def print_demo():
	print('All tests passed, printing manual verification page...\n')
	print(antsy.decorate('Some text and then (bold bold text and then (fg/red bold red text) now bold) and normal'))
	print(antsy.decorate('(b bold) (d dim) (i italic) (u underline) (b,fg/red DANGER) (bg/green,i,u,fg/yellow CRAZY)'))
	print(antsy.decorate('Different delimiters here (because this text has [fg/red parentheses] in it)', start='[', end=']'))
	# The table
	print(antsy.decorate(''.join(['        '] + ['(fg/{} {})'.format(c, c.ljust(8)) for c in antsy.COLORS])))
	for bgc in antsy.COLORS:
		sys.stdout.write(antsy.decorate('(bg/{} {}) '.format(bgc, bgc.ljust(7))))
		for fgc in antsy.COLORS:
			sys.stdout.write(antsy.decorate('(bg/{}  (fg/{} (d X) X (b X)) ) '.format(bgc, fgc)))
		sys.stdout.write('\n')
	print('')


class TestDemo(unittest.TestCase):

	pass


# @TODO: Test...
#   - Custom delimiters work


if __name__ == '__main__':
	try:
		unittest.main(exit=False)
	except Exception:
		raise
	else:
		print_demo()
