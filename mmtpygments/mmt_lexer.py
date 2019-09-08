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
from pygments.token import Comment, Keyword, Name, Number, \
	Punctuation, String, Token, Whitespace

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
			(r'(namespace)(\s+)(\S+)(\s*)(❚)', bygroups(
				Keyword.Namespace, Whitespace, String, Whitespace, Token.MMT_MD
			)),
			(r'(import)(\s+)(\S+)(\s+)(\S+)(\s*)(❚)', bygroups(
				Keyword.Namespace, Whitespace, Name.Namespace, Whitespace, String, Whitespace, Token.MMT_MD
			)),
			(r'theory\b', Keyword.Declaration, 'theoryHeader'),
			(r'(implicit)(\s+)(view)\b', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'viewHeader'),
			(r'(view)\b', Keyword.Declaration, 'viewHeader'),
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
			(r'(\S+)(\s*)(:)(\s*)(\S+)(\s*)(->|→)(\s*)(\S+)(\s*)(=)', bygroups(
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
			# Comments
			(r'\/T .*?❙', Comment.Multiline),
			(r'\/\/.*?❙', Comment.Multiline),

			# Special declarations
			(r'(include)(\s+)([^❙]+)(❙)', bygroups(Keyword.Namespace, Whitespace, String, Token.MMT_DD)),
			(r'(constant)(\s+)([^\s:❘❙]+)', bygroups(Keyword.Declaration, Whitespace, Name.Constant), 'constantDeclaration'),
			(r'(rule)(\s+)([^❙]+)(\s*)(❙)', bygroups(Keyword.Namespace, Whitespace, String, Whitespace, Token.MMT_DD)),

			# Nested theories
			(r'theory\b', Keyword.Declaration, 'theoryHeader'),

			# Markdown-style header comments
			(r'(#+)([^❙]+)(❙)', bygroups(String.Doc, String.Doc, Token.MMT_DD)),

			# Constant declarations (only if nothing else applied!)
			(r'[^\s:❘❙❚]+', Name.Constant, 'constantDeclaration'),

			# The end
			(r'❚', Token.MMT_MD, '#pop:2') # Jump two levels above the theoryHeader or viewHeader
		],
		'constantDeclaration': [
			(r'\s', Whitespace),
			(r':', Punctuation, 'expression'),
			(r'=', Punctuation, 'expression'),
			(r'#', Punctuation, 'notationExpression'),
			(r'(@)([^❘❙]+)', bygroups(Punctuation, Name.Constant)),
			(r'role\b', Keyword, 'expression'),
			(r'(\/\/.*?)(?=❘|❙)', bygroups(Comment.Multiline, None)),
			(r'❘', Token.MMT_OD),
			(r'❙', Token.MMT_DD, '#pop')
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