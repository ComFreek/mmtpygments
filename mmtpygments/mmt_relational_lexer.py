# -*- coding: utf-8 -*-
"""
	Pygments Lexer for MMT Relational Information
	~~~~~~~~~~~~~~~~~~~~

	The MMT project can be found at https://uniformal.github.io/.

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2019 ComFreek
	:license: ISC, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Keyword, String, Whitespace

__all__ = ['MMTRelationalLexer']

class MMTRelationalLexer(RegexLexer):
	"""
	Pygments Lexer for MMT relational info (.rel)

	The MMT project can be found at https://uniformal.github.io/.
	"""

	name = 'MMTRelational'
	aliases = ['mmtrel']
	filenames = ['*.rel']
	mimetypes = ['text/plain']

	flags = re.DOTALL | re.UNICODE | re.IGNORECASE | re.MULTILINE

	tokens = {
		'root': [
			(r'\s', Whitespace),
			(r'(\S+)(\s+)([^\r\n]+)', bygroups(Keyword.Declaration, Whitespace, String))
		]
	}
