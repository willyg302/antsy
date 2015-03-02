'''
antsy: Sweet interpolated ANSI strings
Repo: https://github.com/willyg302/antsy
'''
import os
import re
import sys


__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))


PY2 = sys.version_info[0] == 2

if not PY2:
	import functools
	reduce = functools.reduce


def is_a_tty():
	return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

def supports_color():
	'''Sort of from Django. True if the terminal supports color.'''
	if not is_a_tty():
		return False
	platform = sys.platform
	if platform == 'Pocket PC':
		return False
	if platform == 'win32' and 'ANSICON' not in os.environ:
		return False
	return True

SUPPORTS_COLOR = supports_color()


ESCAPE = '\033[{}m'
RESET = ESCAPE.format(0)
COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

def wrap(s, on, off):
	return ESCAPE.format(on) + s + ESCAPE.format(off)

def normal(s):
	return s  # A no-op, strings are implicitly wrapped in this

def bold(s):
	return wrap(s, 1, 22)

def dim(s):
	return wrap(s, 2, 22)

def italic(s):
	return wrap(s, 3, 23)

def underline(s):
	return wrap(s, 4, 24)

def fg(s, color):
	return wrap(s, 30 + COLORS.index(color), 39) if color in COLORS else s

def bg(s, color):
	return wrap(s, 40 + COLORS.index(color), 49) if color in COLORS else s

ANSI = {
	'normal': normal,
	'n': normal,
	'bold': bold,
	'b': bold,
	'dim': dim,
	'd': dim,
	'italic': italic,
	'i': italic,
	'underline': underline,
	'u': underline,
	'fg': fg,
	'bg': bg
}


def parse_tokens(tokens, start, end):
	if len(tokens) == 0:
		raise SyntaxError('Unexpected end of string reached while parsing')
	parsed = []
	while tokens:
		token = tokens.pop(0)
		if token == start:
			parsed.append(parse_tokens(tokens, start, end))
		elif token == end:
			break
		else:
			parsed.append(token)
	return parsed

def parse(s, start, end):
	tokens = [e for e in re.split('({}|{})'.format(re.escape(start), re.escape(end)), s) if e]
	return parse_tokens(tokens, start, end)

def transform_list(x):
	control, rest = x.pop(0).split(' ', 1)  # Get the control sequence off x
	s = ''.join([transform(e) for e in [rest] + x])  # Recurse transform to build string s
	if not SUPPORTS_COLOR:
		return s  # Short-circuit if there's no ANSI support!
	fns = control.split(',')  # The sequence may consist of multiple controls
	# Apply a single control, with possible args, to s
	def apply_fn(fn, s):
		code, args = fn.split('/')[0], fn.split('/')[1:]
		if code not in ANSI:
			raise SyntaxError('Undefined control code "{}"'.format(code))
		return ANSI[code](s, *args)
	return reduce(lambda s, fn: apply_fn(fn, s), fns, s)  # Apply all controls to s

def transform(x):
	return transform_list(x) if isinstance(x, list) else x

def decorate(s, start='(', end=')'):
	if start == end:
		raise SyntaxError('Start and end delimiters cannot match')
	return transform(parse("normal " + s, start, end))
