from setuptools import setup, find_packages

# Open readme with original (i.e. LF) newlines
# to prevent the all too common "`long_description_content_type` missing"
# bug (https://github.com/pypa/twine/issues/454)
with open('README.md', 'r', newline='', encoding='utf-8') as readme_file:
	long_description = readme_file.read()
	long_description_content_type = 'text/markdown'

setup(
	name = 'mmtpygments',
	version = '0.4.0',

	# This description field must not contain any newline characters
	# Otherwise, the all too common "`long_description_content_type` missing"
	# bug will appear (https://github.com/pypa/twine/issues/454)
	description = 'Pygments plugin for MMT surface syntax (lexer & style)',
	long_description = long_description,
	long_description_content_type = long_description_content_type,
	author = 'ComFreek',
	maintainer = 'ComFreek',
	maintainer_email = 'comfreek@outlook.com',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: ISC License (ISCL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Documentation',
		'Topic :: Multimedia :: Graphics :: Presentation',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
	keywords = 'pygments highlighting mmt minted',
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
