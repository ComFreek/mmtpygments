# -*- coding: utf-8 -*-
"""
	Pygments Lexer for MMT Surface Syntax
	~~~~~~~~~~~~~~~~~~~~

	The MMT project can be found at https://uniformal.github.io/.

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2019 ComFreek
	:license: ISC, see LICENSE for details.
"""

import re, sys

from pygments.lexer import RegexLexer
from pygments.token import Comment, Generic, Keyword, Literal, \
	Name, Number, Punctuation, String, Token, Whitespace

__all__ = ['MMTLexer']

IS_CONVERSION_MODE = False

if __name__ == '__main__' and len(sys.argv) == 2 and sys.argv[1] == 'convert':
	IS_CONVERSION_MODE = True

def bygroups(*bygroup_args):
	global IS_CONVERSION_MODE

	import pygments.lexer
	if IS_CONVERSION_MODE:
		return bygroup_args
	else:
		return pygments.lexer.bygroups(*bygroup_args)

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
			(r'\/T .*?❚', Comment.Multiline),
			(r'\/\/.*?❚', Comment.Multiline),

			# Document-level directives
			(r'(meta)(?= )', Keyword.Declaration, ('expectMD', 'metaAnnotation')),
			(r'(namespace)(\s+)(\S+?)(\s*)(❚)', bygroups(
				Keyword.Namespace, Whitespace, Literal.URI, Whitespace, Token.MMT_MD
			)),
			(r'(import)(\s+)(\S+)(\s+)(\S+?)(\s*)(❚)', bygroups(
				Keyword.Namespace, Whitespace, Name.Namespace, Whitespace, Literal.URI, Whitespace, Token.MMT_MD
			)),
			(r'(fixmeta|ref)(\s+)(\S+?)(\s*)(❚)', bygroups(
				Comment.Preproc, Whitespace, Literal.URI, Whitespace, Token.MMT_MD
			)),
			(r'diagram\b', Keyword.Declaration, 'diagramHeader'),
			
			# Modules (theories, views)
			(r'theory\b', Keyword.Declaration, 'theoryHeader'),
			(r'(implicit)(\s+)(view)\b', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'viewHeader'),
			(r'(view)\b', Keyword.Declaration, 'viewHeader'),

			# If nothing before matched, do graceful degradation
			(r'[^❚]*?❚', Generic.Error)
		],
		'expectMD': [
			(r'(\s*)(❚)', bygroups(Whitespace, Token.MMT_MD), '#pop')
		],
		'expectDD': [
			(r'(\s*)(❙)', bygroups(Whitespace, Token.MMT_DD), '#pop')
		],
		'expectOD': [
			(r'(\s*)(❘)', bygroups(Whitespace, Token.MMT_OD), '#pop')
		],
		'metaAnnotation': [
			(r'(\s*)(.*?)(\s+)', bygroups(Whitespace, Name.Constant, Whitespace), 'metaAnnotationValue'),
		],
		'metaAnnotationValue': [
			# either URI
			(r'\?[^ ❘❙❚]*', Literal.URI, '#pop:2'),
			# or arbitrary expression
			(r'[^❘❙❚]*', Token.MMT_ObjectExpression, '#pop:2')
		],
		'theoryHeader': [
			(r'\s', Whitespace),
			# First try matching with meta theory
			(r'(\S+)(\s*)(:)(\s*)([^❚=]+)', bygroups(
				Name.Variable,
				Whitespace,
				Punctuation, Whitespace, Name.Variable # the meta part
			), 'moduleDefiniens'),

			# Then without meta theory
			(r'[^❚=]+', Name.Variable, 'moduleDefiniens')
		],
		'moduleDefiniens': [
			(r'\s', Whitespace),
			(r'=', Punctuation, 'moduleBody'),

			# The end
			# jump back to outer container (either root or other module in case of nested modules)
			# theoryHeader/viewHeader --> outer container
			(r'❚', Token.MMT_MD, '#pop:2')
		],
		'viewHeader': [
			(r'\s', Whitespace),
			(r'(\S+)(\s*)(:)(\s*)(\S+)(\s*)(->|→)(\s*)([^❚=]+)', bygroups(
					Name.Variable,
					Whitespace,
					Punctuation,
					Whitespace,
					Name.Variable,
					Whitespace,
					Punctuation,
					Whitespace,
					Name.Variable,
			), 'moduleDefiniens')
		],
		'diagramHeader': [
			(r'\s', Whitespace),
			# First try matching with meta theory
			(r'(\S+)(\s*)(:)(\s*)([^❚=]+)', bygroups(
				Name.Variable,
				Whitespace,
				Punctuation, Whitespace, Name.Variable # the meta part
			), 'expression'),

			# Then without meta theory
			(r'[^❚=]+', Name.Variable, 'expression'),
			(r'❚', Token.MMT_MD, '#pop')
		],

		# Modules subsume both theories and views
		# Invariant: moduleBody jumps at end two levels up since it assumes a theoryHeader or viewHeader before
		'moduleBody': [
			(r'\s', Whitespace),
			# Comments
			(r'\/T .*?❙', Comment.Multiline),
			(r'\/\/.*?❙', Comment.Multiline),

			# Meta Annotations
			(r'(meta)(?= )', Keyword.Declaration, ('expectDD', 'metaAnnotation')),

			# Special declarations
			(r'(include)(\s+)([^❙]+)(❙)', bygroups(Keyword.Namespace, Whitespace, Literal.URI, Token.MMT_DD)),
			(r'(constant)(\s+)([^\s:❘❙]+)', bygroups(Keyword.Declaration, Whitespace, Name.Constant), 'constantDeclaration'),
			(r'(rule)(\s+)([^❙]+)(\s*)(❙)', bygroups(Keyword.Namespace, Whitespace, Literal.URI, Whitespace, Token.MMT_DD)),
			(r'(realize)(\s+)([^❙]+)(\s*)(❙)', bygroups(Keyword, Whitespace, Literal.URI, Whitespace, Token.MMT_DD)),

			# Structures
			(r'(total\s+)?(structure\b)', Keyword, 'theoryHeader'),

			# Nested theories
			(r'theory\b', Keyword.Declaration, 'theoryHeader'),

			# Markdown-style header comments
			(r'(#+)([^❙]+)(❙)', bygroups(String.Doc, String.Doc, Token.MMT_DD)),

			# Constant declarations (only if nothing else applied!)
			(r'[^\s:❘❙❚]+', Name.Constant, 'constantDeclaration'),

			(r'[^❚]*?❙', Generic.Error),

			# The end
			# jump back to outer container (either root or other module in case of nested modules)
			# moduleDefiniens --> theoryHeader/viewHeader --> outer container
			(r'❚', Token.MMT_MD, '#pop:3')
		],
		'constantDeclaration': [
			(r'\s', Whitespace),
			(r':', Punctuation, 'expression'),
			(r'=', Punctuation, 'expression'),
			(r'#', Punctuation, 'notationExpression'),
			(r'(@)([^❘❙]+)', bygroups(Punctuation, Name.Constant)),
			(r'role\b', Keyword, 'expression'),
			(r'(meta)(?= )', Keyword.Declaration, 'metaAnnotation'),
			(r'\/\/[^❘❙]*', Comment.Multiline),
			(r'❘', Token.MMT_OD),
			(r'❙', Token.MMT_DD, '#pop'),

			# If nothing before matched, do graceful degradation for...

			# - ...unknown structural features that we detect via an equal sign.
			#
			#   Note that such structural features contain declaration delimiters (❙)
			#   themselves and are ended by a module delimiter (❙)!
			(r'[^❙❚]*?=[^❚]*?❚', Generic.Error, '#pop'),

			# - ... everything else
			(r'[^❚]*?❙', Generic.Error, '#pop'),
		],
		'notationExpression': [
			# Sample constant with notation expression:
			#
			# coprodmatch # 2 match V1 . 3|… to 4 %I5 prec -9000❙
			#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ notation
			#
			# Note that | is a regular pipe, not an MMT delimiter!
			#
			(r'\s+', Whitespace),

			# Specifiers for argument positions and implicit arguments
			(r'\d+', String.Interpol),
			(r'%?((I|V|L)\d+[Td]*)(_(I|L)\d+[Td]*)*', String.Interpol), # also supports %L1_L2

			# Specifier for arglists
			(r'…', String.Interpol),

			# Specifier for precedence specifier (e.g. `pred 1234`)
			(r'(\bprec)(\s+)(-?\d+)', bygroups(Keyword, Whitespace, Number.Integer), '#pop'),

			# Finally the actual notation string (e.g. "match", ".", "|", "to" in the example above)
			(r'([^\s\d…❘❙❚]+)', String.Symbol),

			(r'(?=[❘❙❚])', Whitespace, '#pop')
		],
		'expression': [
			(r'\s', Whitespace),
			(r'[^❘❙❚]+', Token.MMT_ObjectExpression, '#pop')
		],
	}


# Use this for debugging
if __name__ == "__main__":
	import io
	import sys

	if len(sys.argv) == 3 and sys.argv[1] == 'debug':
		test_file = io.open(sys.argv[2], mode="r", encoding="utf-8")

		lexer = MMTLexer()
		print(list(lexer.get_tokens(test_file.read())))
	elif len(sys.argv) == 2 and sys.argv[1] == 'convert':
		from pygments_to_rouge import convert_pygments_regex_lexer
	
		with io.open('mmt.rb', mode="w", newline="\n", encoding="utf-8") as ruby_lexer:
			ruby_lexer.write(convert_pygments_regex_lexer(
				MMTLexer,
				rouge_lexer_name = 'MMT',
				rouge_title = 'mmt',
				rouge_tag = 'mmt'
			))
		print('Successfully converted, see mmt.rb')
	else:
		print("Usage\n==========")
		print(" a) `{} debug filename-of-MMT-file` to debug this Pygments lexer`".format(sys.argv[0]))
		print("    It will be read in UTF-8 encoding and lexed through our parser.")
		print(" b) `{} convert` to convert this Pygments lexer to a Rouge lexer".format(sys.argv[0]))

		sys.exit(1)
