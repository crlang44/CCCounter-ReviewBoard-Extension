from cc_counter.ccreader import get_comparison_data
import copy
import logging


def track_diff_ccchanges(new_diff_comparison_data, orig_diff_comparison_data):
	"""
	"""
	
	orig_file_names = set(orig_file for orig_file in orig_diff_comparison_data)
	logging.debug("orig_diff_coparison_data: " + str(orig_diff_comparison_data))
	logging.debug("new_diff_coparison_data: " + str(new_diff_comparison_data))

	logging.debug("orig_file_names: " + str(orig_file_names))

	diff_ccchanges = []

	for new_filename in new_diff_comparison_data:
		logging.debug("new_filename: " + new_filename)
		if new_filename not in orig_file_names:
			orig_comparison = dict()
		else:
			orig_comparison = orig_diff_comparison_data[new_filename]
			logging.debug("orig_diff_comparison_data[new_filename]: " + str(orig_diff_comparison_data[new_filename]))


		if new_diff_comparison_data[new_filename] != None:
			logging.debug("New_diff_comparison_data[new_filename]: " + str(new_diff_comparison_data[new_filename]))
			ccchanges = _track_func_ccchanges(new_diff_comparison_data[new_filename], orig_comparison)
		else:
			ccchanges = None
		diff_ccchanges += [{
			'filename': new_filename,
			'ccchanges': ccchanges
		}]
	return diff_ccchanges

def _track_func_ccchanges(new_analysis, orig_analysis):
	"""Returns a list of dictionary entries for the net change in cyclomatic complexity
	of all the functions between two different diff cc data files
	"""
	all_functions = list()
	logging.debug("New_Analysis:" + str(new_analysis))
	logging.debug("Orig_Analysis:" + str(orig_analysis))
	
	for function in new_analysis:
		if function not in orig_analysis:
			all_functions += get_all_instances(function, new_analysis)
		else:
			function_comparison = compare_function(function, new_analysis, orig_analysis)
			all_functions.append(function_comparison)
	return all_functions


def get_all_instances(function, file_analysis):
	"""Returns all the function instances from the file_analysis
	"""
	return [file_analysis[function][linenum] for linenum in file_analysis[function]]

def compare_function(function, new_analysis, orig_analysis):
	"""Tracks the changes of a function between two file analysis, outputting the 'new' 
	and 'changed' functions. 'new' functions are functions that have new headers/titles/
	parameters. 'changed' functions are functions that have been tracked as changed
	"""

	all_functions= list()
	if function not in new_analysis or len(new_analysis[function]) == 0: 
		return all_functions
	if function not in orig_analysis or len(orig_analysis[function]) == 0:
		return get_all_instances(function, new_analysis)

	for linenum in new_analysis[function]:
		new_func_instance = new_analysis[function][linenum]

		closest_match = closest_func_match(new_func_instance, orig_analysis)
		orig_cc = None
		if closest_match == None:
			pass
		else:
			orig_cc = closest_match.cc
		current_function = (new_func_instance.function, new_func_instance.line, orig_cc, new_func_instance.cc)
		all_functions.append(current_function)
	return all_functions

def closest_func_match(function_instance, orig_analysis):
	"""Returns a list of how closely matched the instances in orig_analysis 
	are to an instance of a function
	"""

	match = list()
	for linenum in orig_analysis[function_instance.function]:
		orig_instance = orig_analysis[function_instance.function][linenum]
		if compare_instances(function_instance, orig_instance) == 1: 
			match += [orig_instance]
	if len(match) > 1:
		logging.debug("Multiple declarations: %s", match)
		#raise Exception("multiple functions with the same parameters")
	if len(match) == 0:
		match = [None]
	return match[0]

def compare_instances(new_instance, orig_instance):
	count = 0.0
	for parameter in new_instance.parameters:
		if parameter in orig_instance.parameters:
			count+=1
	return count/len(new_instance.parameters)
