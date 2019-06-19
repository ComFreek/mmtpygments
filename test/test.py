# -*- coding: utf-8 -*-
"""
	Pygments Lexer for MMT Surface Syntax
	~~~~~~~~~~~~~~~~~~~~

	The MMT project can be found at https://uniformal.github.io/.

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2019 ComFreek
	:license: ISC, see LICENSE for details.
"""

import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token

import glob
import io
from os import path
import sys

# Add parent directory such that we can import from mmt_lexer
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from mmt_lexer import MMTLexer

def generate_index_file(out_filenames, base_path, index_file):
	# TODO Insecure HTML Injection!
	html_anchors = (
		"<a href='" + base_path + out_filename.replace("\\", "/") + "'>" + out_filename + "</a>"

		for out_filename in out_filenames
	)

	index_file.write("".join(html_anchors))

if __name__ == "__main__":
	lexer = MMTLexer()

	TEST_FILES_DIR = 'data'
	TEST_FILES = glob.iglob(path.join(TEST_FILES_DIR, "*.mmt"))

	lexer = MMTLexer(encoding = "utf-8")
	html_formatter = HtmlFormatter(full = True, encoding = "utf-8")

	at_least_one_erroneous = False
	out_filenames = []

	for test_filename in TEST_FILES:
		# We read both input and output file in binary mode to circumvent encoding issues
		# Indeed, we specified above UTF-8 encoding for the lexer and formatter
		with io.open(test_filename, mode="rb") as test_file:
			tokens = list(lexer.get_tokens(test_file.read()))
			erroneous = any(token is Token.Error for (token, _) in tokens)
			at_least_one_erroneous = at_least_one_erroneous or erroneous

			if erroneous:
				sys.stderr.write("File `" + test_filename + "` errored, see corresponding .html file for details.\n")

			out_filename = test_filename + ".html"
			out_filenames.append(out_filename)
			with io.open(out_filename, mode="wb") as out_file:
				pygments.format(tokens, html_formatter, out_file)

	with io.open('index.html', mode="w") as index_file:
		generate_index_file(out_filenames, 'https://', index_file)

	if at_least_one_erroneous:
		sys.stderr.write("\nAt least one error occurred, returning with non-zero exit code.\n")
		sys.exit(1)