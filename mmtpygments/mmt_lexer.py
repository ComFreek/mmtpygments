# -*- coding: utf-8 -*-
"""
	Pygments Lexer for MMT Surface Syntax
	========================================

	The MMT project can be found at https://uniformal.github.io/.

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2020 ComFreek
	:license: ISC, see LICENSE for details.
"""

import re, sys

from pygments.lexer import RegexLexer
from pygments.token import Comment, Generic, Keyword, Literal, \
	Name, Number, Punctuation, String, Token, Whitespace

__all__ = ['MMTLexer']

# This value will be set to True by the almost immediate __main__ entrypoint below
# if the current invocation of Python is in order to convert this lexer to Rouge.
#
# It changes the behavior of the bygroups wrapper directly below:
# upon conversion mode, the bygroups arguments are simply output as a tuple itself
# (for post-processing by the conversion happening in __main__); upon normal mode,
# calls are delegated to Pygment's true bygroups function.
IS_CONVERSION_MODE = False

def bygroups(*bygroup_args):
	global IS_CONVERSION_MODE

	import pygments.lexer
	if IS_CONVERSION_MODE:
		return bygroup_args
	else:
		return pygments.lexer.bygroups(*bygroup_args)

# Use this for debugging
if __name__ == "__main__" and len(sys.argv) == 3 and sys.argv[1] == 'convert':
	IS_CONVERSION_MODE = True

class MMTLexer(RegexLexer):
	"""
	Pygments Lexer for MMT Surface Syntax

	The MMT project can be found at https://uniformal.github.io/.

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2020 ComFreek
	:license: ISC, see LICENSE for details.
	"""

	name = 'MMT'
	aliases = ['mmt']
	filenames = ['*.mmt', '*.mmtx']
	mimetypes = ['application/x-mmt']

	flags = re.DOTALL | re.UNICODE | re.IGNORECASE | re.MULTILINE

	tokens = {
		'root': [
			(r'\s+', Whitespace),
			(r'\/T .*?❚', Comment.Multiline),
			(r'\/\/.*?❚', Comment.Multiline),

			# (super document)-level directives
			(r'(document)((?: |\t)+)(\S+?)(?=\s+)', bygroups(Keyword.Declaration, Whitespace, Name.Namespace)),

			# Document-level directives
			(r'(meta)(\s+)(\S+)(\s+)([^❚]+)(\s*)(❚)', bygroups(
				Keyword.Declaration,
				Whitespace,
				Literal.URI,
				Whitespace,
				Token.MMT_ObjectExpression,
				Whitespace,
				Token.MMT_MD
			)),
			(r'(namespace)(\s+)(\S+?)(\s*)(❚)', bygroups(
				Keyword.Namespace, Whitespace, Literal.URI, Whitespace, Token.MMT_MD
			)),
			(r'(import)(\s+)(\S+)(\s+)(\S+?)(\s*)(❚)', bygroups(
				Keyword.Namespace, Whitespace, Name.Namespace, Whitespace, Literal.URI, Whitespace, Token.MMT_MD
			)),
			(r'(fixmeta|ref|rule)(\s+)(\S+?)(\s*)(❚)', bygroups(
				Comment.Preproc, Whitespace, Literal.URI, Whitespace, Token.MMT_MD
			)),
			(r'(diagram)\b', Keyword.Declaration, 'diagramHeader'),
			
			# Theories
			(r'(theory)\b', Keyword.Declaration, 'theoryHeader'),

			# Views
			# (we duplicate the total|implicit subregex here to account for total *and* implicit views
			#  without imposing an ordering on those keywords)
			(r'(?:(total|implicit)(\s+))?(?:(total|implicit)(\s+))?(view)\b', bygroups(
				Keyword, Whitespace,
				Keyword, Whitespace,
				Keyword.Declaration
			), 'viewHeader'),

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

		# Lex structural features within modules (incl. ordinary structures) beginning with their header
		#
		# Examples: (w/o = without, w/ = with)
		#
		#  (1) `structure s = ?someTheory ❙` (structures w/o meta, body; w/ definiens)
		#                 ^
		#  (2) `structure s : ?someTheory ❙` (structures w/o body; w/ meta, definiens)
		#                 ^
		#  (3) `structure s : ?someTheory = ?someOtherTheory ❙` (structures w/o body; w/ meta, definiens)
		#                 ^
		#  (4) `reflect list1(a: type) : ☞?InductivelyDefinedTypes/list_decls(a:type) ❙` (structural features w/o body; w/ meta)
		#               ^
		#  (5) `inductive list1_unreflected(a: type) ❘ = list: type ❙  nil: list ❙ cons: a ⟶ list ⟶ list ❙` (structural features w/o meta; w/ body, parameter list)
		#                 ^
		#
		# and probably more combinations.
		# The caret (^) stands for the character at which this rule set can and should be invoked.
		# In particular, neither `structure` nor any other name of a structural feature (e.g. `reflect`, `inductive`)
		# can be processed by this rule set.
		'structuralFeatureHeader': [
			(r'\s+', Whitespace),

			# Structural Features without body
			#
			# IF YOU EDIT, edit the regex below for structural features with body accordingly
			#
			(r'([^\s(❙❚:=]+)(\s*)(?:(\()([^)]*)(\)))?(\s*)(?:(:)(\s*)([^❘❙❚=]+))?(\s*)(?:(=)(\s*)([^\s:❙❚]+))?(\s*)(❙)', bygroups(
			#  ^^^^^^^^^^^^        ^^^^^^^^^^^^^^^          ^^^^^^^^^^^^^^^^^          ^^^^^^^^^^^^^^^^^^
			#    name            optional param list          optional meta part    optional definiens (URI)
				Name.Class,
				Whitespace,

				# the optional parameter list (TODO: doesn't handle nested brackets)
				Punctuation,
				Name.Variable,
				Punctuation,

				Whitespace,

				# the optional meta part
				Punctuation, Whitespace, Name.Variable,
				
				Whitespace,

				# the optional `= <URI>` part
				Punctuation, Whitespace, Literal.URI,

				Whitespace,
				Token.MMT_DD
			), '#pop:1'),

			# Structural Features with body: process param and meta part if existing, then delegate to `moduleDefiniens`
			#
			# IF YOU EDIT, edit the regex above for structural features without body accordingly
			#
			(r'([^\s(❙❚:=]+)(\s*)(?:(\()([^)]*)(\)))?(\s*)(?:(:)(\s*)([^❘❙❚=]+))?(\s*)', bygroups(
			#  ^^^^^^^^^^^^        ^^^^^^^^^^^^^^^          ^^^^^^^^^^^^^^^^^
			#    name            optional param list        optional meta part
				Name.Class,
				Whitespace,

				# the optional parameter list (TODO: doesn't handle nested brackets)
				Punctuation,
				Name.Variable,
				Punctuation,

				Whitespace,

				# the optional meta part
				Punctuation, Whitespace, Name.Variable,
				
				Whitespace
			), 'moduleDefiniens')
		],

		'theoryHeader': [
			(r'\s+', Whitespace),

			(r'([^\s❙❚:=]+)(\s*)(?:(:)(\s*)([^\s❙❚=]+))?(\s*)(?:(>)([^❙❚=]+))?', bygroups(
				Name.Class,
				Whitespace,

				# the optional meta part
				Punctuation, Whitespace, Literal.URI,

				Whitespace,

				# the optional parameter specification (for parametric theories)
				Punctuation, Name.Variable # TODO: Name.Variable is a crude approximation for coloring here
			), 'moduleDefiniens')
		],
		'moduleDefiniens': [
			(r'\s+', Whitespace),
			(r'❘', Token.MMT_OD),

			# usually theories and views do not have notation expressions, but usages of structural features within 
			# theories might
			(r'#', Punctuation, 'notationExpression'),
			(r'=', Punctuation, 'moduleBody'),

			# The cases of a module/structural feature with an empty body
			# => jump back to outer container (either root or other module in case of nested modules)
			(r'❚', Token.MMT_MD, '#pop:2')
		],
		'viewHeader': [
			(r'\s+', Whitespace),
			(r'(\S+)(\s*)(:)(\s*)(\S+)(\s*)(->|→)(\s*)([^❚=]+)', bygroups(
					Name.Class,
					Whitespace,
					Punctuation,
					Whitespace,
					Literal.URI,
					Whitespace,
					Punctuation,
					Whitespace,
					Literal.URI,
			), 'moduleDefiniens')
		],

		'diagramHeader': [
			(r'\s+', Whitespace),
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
		# Invariant: moduleBody jumps at end two levels up since it assumes one of {theory|view|structuralFeature}Header before
		'moduleBody': [
			(r'\s+', Whitespace),

			# Comments
			# comments in module may also be ended with the module delimiter ❚
			(r'\/T .*?(❙|❚)', Comment.Multiline),
			(r'\/\/.*?(❙|❚)', Comment.Multiline),

			# old way of providing meta annotations that are strings
			# e.g. see https://gl.mathhub.info/MMT/examples/-/blob/206d8ed1eb172d18c26b2f1530681f911ea1af45/source/tutorial/2-algebra.mmt#L21-26
			(r'(@_description)(\s+)([^❙])+(❙)', bygroups(Keyword, Whitespace, String, Token.MMT_DD)),

			# Meta Annotations
			(r'(meta)(\s+)(\S+)(\s+)([^❙❚]+)(\s*)(❙)', bygroups(
				Keyword.Declaration,
				Whitespace,
				Literal.URI,
				Whitespace,
				Token.MMT_ObjectExpression,
				Whitespace,
				Token.MMT_MD
			)),

			# Special declarations
			(r'(include)(\s+)([^❙]+)(❙)', bygroups(Keyword.Namespace, Whitespace, Literal.URI, Token.MMT_DD)),
			(r'(constant)(\s+)([^\s:❘❙]+)', bygroups(Keyword.Declaration, Whitespace, Name.Variable.Class), 'constantDeclaration'),
			(r'(rule)(\s+)([^❙]+)(\s*)(❙)', bygroups(Keyword.Namespace, Whitespace, Literal.URI, Whitespace, Token.MMT_DD)),
			(r'(realize)(\s+)([^❙]+)(\s*)(❙)', bygroups(Keyword, Whitespace, Literal.URI, Whitespace, Token.MMT_DD)),

			# Structures
			# (we duplicate the total|implicit subregex here to account for total *and* implicit structures
			#  without imposing an ordering on those keywords)
			(r'(?:(total|implicit)(\s+))?(?:(total|implicit)(\s+))?(structure\b)', bygroups(
				Keyword, Whitespace,
				Keyword, Whitespace,
				Keyword.Declaration
			), 'structuralFeatureHeader'),

			# Nested theories
			(r'theory\b', Keyword.Declaration, 'theoryHeader'),

			# Nested views
			# (we duplicate the total|implicit subregex here to account for total *and* implicit views
			#  without imposing an ordering on those keywords)
			(r'(?:(total|implicit)(\s+))?(?:(total|implicit)(\s+))?(view\b)', bygroups(
				Keyword, Whitespace,
				Keyword, Whitespace,
				Keyword.Declaration
			), 'viewHeader'),

			# Markdown-style header comments
			(r'(#+)([^❙]+)(❙)', bygroups(String.Doc, String.Doc, Token.MMT_DD)),

			# Structural features
			(r'([^\s:=#❘❙❚]+)(\s+)(?=[^\s:=@#❘❙❚]+)', bygroups(Keyword.Declaration, Whitespace), 'structuralFeatureHeader'),

			# Constant declarations (only if nothing else applied!)
			# only match the name greedily until a whitespace \s, a typing colon :, a notation expression #,
			# or a delimiter appears
			(r'[^\s:=#❘❙❚]+', Name.Variable.Class, 'constantDeclaration'),

			(r'[^❚]*?❙', Generic.Error),

			# The end
			# jump back to outer container (either root or other module in case of nested modules)
			# moduleDefiniens --> theoryHeader/viewHeader --> outer container
			(r'❚', Token.MMT_MD, '#pop:3')
		],
		'constantDeclaration': [
			(r'\s+', Whitespace),
			(r':', Punctuation, 'expression'),
			(r'=', Punctuation, 'expression'),
			(r'#', Punctuation, 'notationExpression'),

			# old way of providing meta annotations that are strings
			# e.g. see https://gl.mathhub.info/MMT/examples/-/blob/206d8ed1eb172d18c26b2f1530681f911ea1af45/source/tutorial/2-algebra.mmt#L21-26
			(r'(@_description)(\s+)([^❘❙])+', bygroups(Keyword, Whitespace, String)),

			(r'(@)([^❘❙]+)', bygroups(Punctuation, Name.Constant)),
			(r'role\b', Keyword, 'expression'),
			(r'(meta)(\s+)(\S+)(\s+)([^❘❙]+)(\s*)(?=❘|❙)', bygroups(
				Keyword.Declaration,
				Whitespace,
				Literal.URI,
				Whitespace,
				Token.MMT_ObjectExpression,
				Whitespace
			)),
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
			(r'\s+', Whitespace),
			(r'[^❘❙❚]*', Token.MMT_ObjectExpression, '#pop')
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
	
	# if you change the conditions here, also change it way above the MMTLexer class
	# in the code snippet that sets IS_CONVERSION_MODE to true.
	elif len(sys.argv) == 3 and sys.argv[1] == 'convert':
		from pygments_to_rouge import convert_pygments_regex_lexer

		out_filename = sys.argv[2]
	
		with io.open(out_filename, mode="w", newline="\n", encoding="utf-8") as ruby_lexer:
			ruby_lexer.write(convert_pygments_regex_lexer(
				MMTLexer,
				rouge_lexer_name = 'MMT',
				rouge_title = 'mmt',
				rouge_tag = 'mmt'
			))
		print('Successfully converted, see `{}`'.format(out_filename))
	else:
		print("Usage\n==========")
		print(" a) `{} debug in-filename` to debug this Pygments lexer`".format(sys.argv[0]))
		print("    It will be read in UTF-8 encoding and lexed through our parser.")
		print("")
		print(" b) `{} convert out-filename` to convert this Pygments lexer to a Rouge lexer".format(sys.argv[0]))

		sys.exit(1)
