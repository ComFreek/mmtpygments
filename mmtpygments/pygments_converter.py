# -*- coding: utf-8 -*-
"""
	Utility class for converting Pygments regex lexers to frameworks
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	:author: ComFreek <comfreek@outlook.com>
	:copyright: Copyright 2020 ComFreek
	:license: ISC, see LICENSE for details.
"""

from pygments.lexer import RegexLexer

class PygmentsConverter:
	def __init__(self):
		pass
	
	PYGMENTS_START_STATE_NAME = 'root'
	target_start_state_name = 'root'

	def transform_state_name(self, state):
		"""
		Injectively transform a state name

		By default, if not overridden, this methods transforms PYGMENTS_START_STATE_NAME
		to target_start_state_name.

		Use cases in general:

		  1. the target framework does not support specific state names (e.g. no whitespace)
		  2. the start state name in the target framework differs from PYGMENTS_TART_STATE_NAME
		"""
		if state == self.PYGMENTS_START_STATE_NAME:
			return self.target_start_state_name
		elif state == self.target_start_state_name:
			return state + '__permuted'
		elif state == self.target_start_state_name + '__permuted':
			raise Exception('Permutation exhausted')
		else:
			return state

	def transform_lexer_header(self, regex_lexer):
		pass

	def transform_lexer_footer(self, regex_lexer):
		pass

	def transform_state_header(self, state):
		pass

	def transform_state_footer(self, state):
		pass

	def transform_regex(self, regex, python_flags):
		pass

	# input is Pygments token type
	def transform_single_token_type(self, token_type):
		pass

	def transform_token_types(self, token_types):
		pass

	def transform_transition(self, 	next_state_type, next_state_info, indentation):
		pass

	def transform_rule(self, regex, token_types, next_state_type, next_state_info, indentation = "", regex_python_flags = []):
		pass

	def transform(self, regex_lexer):
		target = ""
		
		target += self.transform_lexer_header(regex_lexer)
		
		for raw_state, rules in regex_lexer.tokens.items():
			state = self.transform_state_name(raw_state)

			target += self.transform_state_header(state)

			for rule in rules:
				regex = rule[0]
				token_type = rule[1]
				if not type(token_type) is tuple:
					token_type = [token_type]
			
				next_state_type = None
				next_state_info = None

				if len(rule) == 3 and isinstance(rule[2], str):
					if rule[2] == '#pop':
						next_state_type = 'pop'
						next_state_info = 1
					elif rule[2].startswith("#pop:"): # pop the number of states given after colon
						number_of_states = int(rule[2][len("#pop:"):]) 

						next_state_type = 'pop'
						next_state_info = number_of_states
					else:
						next_state_type = 'push'
						next_state_info = [self.transform_state_name(rule[2])] # push a single state
				elif len(rule) == 3 and isinstance(rule[2], tuple):
					# rule[2] contains a list of states to be pushed
					next_state_type = 'push'
					next_state_info = map(self.transform_state_name, rule[2])
			
				target += self.transform_rule(regex, token_type, next_state_type, next_state_info, indentation="\t\t\t\t", regex_python_flags=regex_lexer.flags)

			target += self.transform_state_footer(state)
	
		target += self.transform_lexer_footer(regex_lexer)

		return target
