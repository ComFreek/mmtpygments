"""
Pygments plugin for MMT surface syntax (lexer & style)
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme_file:
	long_description = readme_file.read()

setup(
	name = 'mmtpygments',
	version = '0.1.0',
	description = __doc__,
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	author = 'ComFreek',
	maintainer = 'ComFreek',
	maintainer_email = 'comfreek@outlook.com',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: ISC License (ISCL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python'
		'Topic :: Documentation',
		'Topic :: Multimedia :: Graphics :: Presentation'
	],
	python_requires = '>=3.6',
	url = 'https://github.com/ComFreek/mmtpygments',
	author_email = 'comfreek@outlook.com',
	install_requires = ['pygments'],
	packages = [
		'mmtpygments',
		'mmtpygments.test'
	],
	entry_points = '''
		[pygments.styles]
			mmtdefault = mmtpygments.mmt_style:MMTDefaultStyle
		[pygments.lexers]
			mmt = mmtpygments.mmt_lexer:MMTLexer
	'''
)
