# -*- coding: utf-8 -*-
"""
	Pygments Lexer for MMT Surface Syntax
	~~~~~~~~~~~~~~~~~~~~

	The MMT project can be found at https://uniformal.github.io/.

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2019 ComFreek
	:license: ISC, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Keyword, Name, String, \
	Number, Punctuation, Whitespace

__all__ = ['MMTLexer']

class MMTLexer(RegexLexer):
	"""
	Pygments Lexer for MMT Surface Syntax (.mmt)

	The MMT project can be found at https://uniformal.github.io/.
	"""

	name = 'MMT'
	aliases = ['mmt']
	filenames = ['*.mmt']
	mimetypes = ['text/plain']

	flags = re.DOTALL | re.UNICODE | re.IGNORECASE | re.MULTILINE

	tokens = {
		'root': [
			(r'\s', Whitespace),
			(r'(namespace)(\s+)(\S+)(\s*)(❚)', bygroups(Keyword.Namespace, Whitespace, String, Whitespace, Punctuation)),
			(r'(import)(\s+)(\S+)(\s+)(\S+)(\s*)(❚)', bygroups(Keyword.Namespace, Whitespace, Name.Namespace, Whitespace, String, Whitespace, Punctuation)),
			(r'theory', Keyword.Declaration, 'theoryHeader'),
			(r'view\b', Keyword.Declaration, 'viewHeader'),
			(r'\/T .*?❚', Comment.Multiline),
			(r'\/\/.*?❚', Comment.Multiline)
		],
		'theoryHeader': [
			(r'\s', Whitespace),
			# First try matching with meta theory
			(r'(\S+)(\s*)(:)(\s*)(\S+)(\s*)(=)', bygroups(Name.Variable, Whitespace, Punctuation, Whitespace, Name.Variable, Whitespace, Punctuation), 'moduleBody'),

			# Then without meta theory
			(r'(\S+)(\s*)(=)', bygroups(Name.Variable, Whitespace, Punctuation), 'moduleBody')
		],
		'viewHeader': [
			(r'\s', Whitespace),
			(r'(\S+)(\s*)(:)(\s*)(\S+)(\s*)(->)(\s*)(\S+)(\s*)(=)', bygroups(
					Name.Variable,
					Whitespace,
					Punctuation,
					Whitespace,
					Name.Variable,
					Whitespace,
					Punctuation,
					Whitespace,
					Name.Variable,
					Whitespace,
					Punctuation
			), 'moduleBody')
		],

		# Modules subsume both theories and views
		# Invariant: moduleBody jumps at end two levels up since it assumes a theoryHeader or viewHeader before
		'moduleBody': [
		  (r'\s', Whitespace),
			(r'\/T .*?❙', Comment.Multiline),
			(r'\/\/.*?❙', Comment.Multiline),
			(r'include\b', Keyword.Namespace, 'includeDeclaration'),
			(r'rule\b', Keyword.Namespace, 'ruleDeclaration'),
			(r'[^\s:❘❙❚]+', Name.Constant, 'constantDeclaration'),
			(r'❚', Punctuation, '#pop:2') # Jump two levels above
		],
		'includeDeclaration': [
			(r'❙', Punctuation, '#pop'),

			# If not end delimiter, interpret everything else as an expression
			(r'', Whitespace, 'expression')
		],
		'ruleDeclaration': [
			(r'❙', Punctuation, '#pop'),

			# If not end delimiter, interpret everything else as an expression
			(r'', Whitespace, 'expression')
		],
		'constantDeclaration': [
			(r'\s', Whitespace),
			(r':', Punctuation, 'expression'),
			(r'=', Punctuation, 'expression'),
			(r'#', Punctuation, 'notationExpression'),
			(r'@', Punctuation, 'aliasExpression'),
			(r'role\b', Keyword, 'expression'),
			(r'(\/\/.*?)(?=❘|❙)', bygroups(Comment.Multiline, None)),
			(r'❘', Punctuation),
			(r'❙', Punctuation, '#pop')
		],
		'aliasExpression': [
			(r'[^❘❙]+', Name.Constant, '#pop')
		],
		'notationExpression': [
			# Lexing rule for notations specifying precedence
			(r'([^❘❙]+)(\bprec)(\s+)(-?\d+)', bygroups(String, Keyword, Whitespace, Number.Integer), '#pop'),

			# And for notations without
			# (Theoretically, both could be merged into one regex, however I couldn't figure out bygroups usage in that case.)
			(r'([^❘❙]+)', bygroups(String), '#pop')
		],
		'expression': [
			(r'\s', Whitespace),
			(r'[^❘❙]+', String, '#pop')
		],
	}

# Use this for debugging
if __name__ == "__main__":
	import io
	import sys

	if len(sys.argv) != 2:
		print("Debugging Interface for MMT's Pygments Lexer")
		print("Usage: " + sys.argv[0] + " filename-of-MMT-file")
		print("")
		print("It will be read in UTF-8 encoding and lexed through our parser.")
		sys.exit()

	test_file = io.open(sys.argv[1], mode="r", encoding="utf-8")

	lexer = MMTLexer()
	print(list(lexer.get_tokens(test_file.read())))