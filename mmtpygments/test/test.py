# -*- coding: utf-8 -*-
"""
	Test Suite for the MMT Pygments lexer
	~~~~~~~~~~~~~~~~~~~~

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2019 ComFreek
	:license: ISC, see LICENSE for details.
"""

import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token, Generic

from datetime import datetime
import glob
import io
from os import path
import sys

# Add parent directory such that we can import from mmt_lexer
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from mmt_lexer import MMTLexer
from mmt_style import MMTDefaultStyle

def generate_index_file(out_statuses, num_succeeding_lines, num_failing_files, base_path, amalgamation_filename, index_file):
	"""Generate index file linking to all rendered HTML files.

	Args:
		out_statuses: An iterable of dictionaries {filename: ..., error: ...}, where
		              filename points to the rendered HTML file and error is a boolean
		              indicating whether an error occured.

		base_path:    Base path to use for links
		index_file:   File object to write the index HTML to, opened as text with encoding UTF-8!
	"""

	def error_to_symbol(error):
		if error:
			return "❌"
		else:
			return "✓"

	index_file.write("""
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">

		<!-- Don't cache! -->
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
		<meta http-equiv="Pragma" content="no-cache" />
		<meta http-equiv="Expires" content="0">

		<title>Index of Render Results - mmt-pygments-lexer</title>
	""")
	index_file.write("<base href='" + base_path + "'>")
	index_file.write("""
	</head>
	<body>
		<h1>Render Results</h1>
		Last update:
	""")
	index_file.write(str(datetime.now()))

	index_file.write("""
		<hr>
	""")

	index_file.write("<h2><a href='" + amalgamation_filename + "'>Amalgamation of Render Results (click)</a></h2>")
	index_file.write("""
		<h2>Overview (highlighted %d lines with success, %d failing files)</h2>
	""" % (num_succeeding_lines, num_failing_files))

	out_statuses = sorted(out_statuses, key = lambda s : s["error"])

	# TODO Insecure HTML Injection!
	html_anchors = list((
		"<a href='" + filename.replace("\\", "/") + "'>" + error_to_symbol(error) + " " + filename + "</a>"

		for (filename, error) in (
			(out_status["filename"], out_status["error"])
			for out_status in out_statuses
		)
	))

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

def count_lines(filename):
	with open(filename, mode="rt", encoding="utf-8") as file:
		for i, _ in enumerate(file):
			pass
		return i + 1

def run_tests(test_files, index_file, index_file_base_path, amalgamation_file, amalgamation_filename):
	"""Run all tests and produce HTML render results.

	Args:
		test_files: An iterable of filenames to lex, test and render
		index_file: A file object to write the HTML index to linking all render results
		            It must be opened as a text file with UTF-8 encoding.
		index_file_base_path: Base path to use for links in index
		amalgamation_file: A file object to write all HTML render results subsequently to
		                   It must be opened as a binary file and it will be written to with UTF-8 encoding.

	Return:
		The number of files that failed complete lexing. On success, this is 0.
	"""

	lexer = MMTLexer(encoding = "utf-8")
	full_html_formatter = HtmlFormatter(full = True, encoding = "utf-8", style = MMTDefaultStyle)
	snippet_html_formatter = HtmlFormatter(full = False, encoding = "utf-8", style = MMTDefaultStyle)

	amalgamation_file.write(b"""
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">

		<!-- Don't cache! -->
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
		<meta http-equiv="Pragma" content="no-cache" />
		<meta http-equiv="Expires" content="0">

		<title>Amalgamation of Render Results - mmt-pygments-lexer</title>
	</head>
	<body>
		<h1>Amalgamation of Render Results</h1>
""")

	amalgamation_file.write(b"<style>")
	amalgamation_file.write(snippet_html_formatter.get_style_defs().encode("utf-8"))
	amalgamation_file.write(b"</style>")

	num_failing_files = 0
	num_succeeding_lines = 0
	out_statuses = []

	# Tokens that we interpret as signalling a lexer error
	# Token.Error is Pygment's standard error token whereas Generic.Error
	# is issued by MMTLexer for graceful degradation
	error_tokens = [Token.Error, Generic.Error]

	for test_filename in test_files:
		print("Running test for " + test_filename)

		# We read both input and output file in binary mode to circumvent encoding issues
		# Indeed, we specified above UTF-8 encoding for the lexer and formatter
		with io.open(test_filename, mode="rb") as test_file:
			tokens = list(lexer.get_tokens(test_file.read()))
			erroneous = any(token in error_tokens for (token, _) in tokens)

		if erroneous:
			num_failing_files = num_failing_files + 1
			print("  --> Lexing error, see corresponding .html file for details\n")
		else:
			num_succeeding_lines = num_succeeding_lines + count_lines(test_filename)

		out_filename = test_filename + ".html"
		out_statuses.append({"filename": out_filename, "error": erroneous})
		with io.open(out_filename, mode="wb") as out_file:
			pygments.format(tokens, full_html_formatter, out_file)
			pygments.format(tokens, snippet_html_formatter, amalgamation_file)

		print("  --> Output at " + out_filename)

	generate_index_file(
		out_statuses,
		num_succeeding_lines,
		num_failing_files,
		index_file_base_path,
		amalgamation_filename,
		index_file
	)

	amalgamation_file.write(b"</body></html>")

	return (num_succeeding_lines, num_failing_files)

def get_test_files():
	"""Return an iterable of all test files in sorted order to consider for testing."""
	TEST_FILES_DIR = 'data'

	all_test_files = set(glob.iglob(path.join(TEST_FILES_DIR, path.join("**", "*.mmt")), recursive = True))

	# These files make use of the inductive structural feature
	# which the lexer doesn't support yet
	excluded_test_files = set(glob.iglob(path.join(TEST_FILES_DIR, '**/*/LFX/source/HOTT.mmt'))).union(
		set(glob.iglob(path.join(TEST_FILES_DIR, '**/*/LFX/source/test.mmt')))
	)

	return sorted(list(all_test_files - excluded_test_files))

if __name__ == "__main__":
	lexer = MMTLexer()

	if len(sys.argv) != 2:
		sys.stderr.write("Usage: " + sys.argv[0] + " Base-Path-To-Use-For-Links-In-Generated-HTML-Index-File\n")
		sys.stderr.write("E.g. https://comfreek.github.io/mmt-pygments-lexer/test/ or ./ for local tests")
		sys.stderr.write("Pay attention to the required trailing slash!")

		sys.exit(1)

	INDEX_FILENAME = 'index.html'
	AMALGAMATION_FILENAME = 'amalgamation.html'
	INDEX_FILE_BASE_PATH = sys.argv[1]
	test_files = get_test_files()

	with io.open(INDEX_FILENAME, "w", encoding = "utf-8") as index_file, io.open(AMALGAMATION_FILENAME, "wb") as amalgamation_file:
		(num_succeeding_lines, num_failures) = run_tests(
			test_files = test_files,
			index_file = index_file,
			index_file_base_path = INDEX_FILE_BASE_PATH,
			amalgamation_file = amalgamation_file,
			amalgamation_filename = AMALGAMATION_FILENAME
		)

		if num_failures is 0:
			print("\nSuccess! %d lines lexed successfully.\n" % (num_succeeding_lines))
			sys.exit(0)
		else:
			sys.stdout.flush() # avoid mixing of stdout and stderr for users' sanity
			sys.stderr.write("\nFailure! %d files failed complete lexing. See HTML output.\n" % num_failures)
			sys.exit(1)
