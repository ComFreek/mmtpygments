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
	html_anchors = list((
		"<a href='" + base_path + out_filename.replace("\\", "/") + "'>" + out_filename + "</a>"

		for out_filename in out_filenames
	))

	index_file.write("""
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">

		<!-- Don't cache! -->
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
		<meta http-equiv="Pragma" content="no-cache" />
		<meta http-equiv="Expires" content="0">

		<title>Render Results - mmt-pygments-lexer</title>
	</head>
	<body>
		<h1>Render Results</h1>""")
	if len(html_anchors) == 0:
		index_file.write("There are none, is the Travis build working? Please submit an issue.")
	else:
		index_file.write("<ul>")
		index_file.write("".join("<li>" + anchor + "</li>" for anchor in html_anchors))
		index_file.write("</ul>")

	index_file.write("""
		</ul>
	</body>
</html>""")

if __name__ == "__main__":
	lexer = MMTLexer()

	if len(sys.argv) != 2:
		sys.stderr.write("Usage: " + sys.argv[0] + " Base-Path-To-Use-For-Links-In-Generated-HTML-Index-File\n")
		sys.stderr.write("E.g. https://comfreek.github.io/mmt-pygments-lexer/test/ or ./ for local tests")
		sys.stderr.write("Pay attention to the required trailing slash!")

		sys.exit(1)

	TEST_FILES_DIR = 'data'
	INDEX_FILENAME = 'index.html'
	INDEX_FILE_BASE_PATH = sys.argv[1]

	TEST_FILES = glob.iglob(path.join(TEST_FILES_DIR, path.join("**", "*.mmt")), recursive = True)

	lexer = MMTLexer(encoding = "utf-8")
	html_formatter = HtmlFormatter(full = True, encoding = "utf-8")

	at_least_one_erroneous = False
	out_filenames = []

	for test_filename in TEST_FILES:
		print("Running test for " + test_filename)

		# We read both input and output file in binary mode to circumvent encoding issues
		# Indeed, we specified above UTF-8 encoding for the lexer and formatter
		with io.open(test_filename, mode="rb") as test_file:
			tokens = list(lexer.get_tokens(test_file.read()))
			erroneous = any(token is Token.Error for (token, _) in tokens)
			at_least_one_erroneous = at_least_one_erroneous or erroneous

			if erroneous:
				sys.stderr.write("  --> Lexing error, see corresponding .html file for details\n")

			out_filename = test_filename + ".html"
			out_filenames.append(out_filename)
			with io.open(out_filename, mode="wb") as out_file:
				pygments.format(tokens, html_formatter, out_file)

			print("  --> Output at " + out_filename)

	with io.open(INDEX_FILENAME, mode="w") as index_file:
		generate_index_file(out_filenames, INDEX_FILE_BASE_PATH, index_file)

	print("\nWrote index file to " + INDEX_FILENAME)

	if at_least_one_erroneous:
		sys.stderr.write("\nAt least one error occurred, returning with non-zero exit code.\n")
		sys.exit(1)