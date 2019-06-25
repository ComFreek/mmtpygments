"""
Lexers and styles for the MMT language
"""
from setuptools import setup, find_packages

setup(
	name = "mmtpygments",
	version = "0.1.0",
	description = __doc__,
	author = "Comfreek",
	author_email = "comfreek@outlook.com",
	install_requires = ["pygments"],
	packages = ["mmtpygments", "mmtpygments.test"],
	entry_points = '''
	[pygments.styles]
	mmtdefault = mmtpygments.mmt_style:MMTDefaultStyle
	[pygments.lexers]
	mmt = mmtpygments.mmt_lexer:MMTLexer
	'''
)
