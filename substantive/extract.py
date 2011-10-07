from codecs import open

def extract_substantives(filename='subst-adj.txt'):
	"""Generator to iterate through entries from the dataset

	Parameters
	----------
		filename: string,
		name of the file

	Returns
	-------
		selected_lines: list of strings,
		list of the lines
	"""
	input_file = open(filename, 'r', encoding='latin2')
	selected_lines = []
	for line in input_file:
		form, base, typestring = line.split()
		split_typestring = typestring.split('.')
		if len(split_typestring) != 6:
			print form
			continue
		pos, gender, number, case, article, _ = split_typestring
		yield form, base, pos, gender, number,  case, article

if __name__ == '__main__':
	f = open('output.txt', 'w', encoding='utf-8')
	for form, _, pos, gender, number, case, article in extract_substantives():
		if 's' not in pos:
			continue  # only take substantives
		if 'n' not in case:
			continue  # only use nominative case
		if 'ne' not in article:
			continue  # only take weak forms

		print >> f, "%s\t%s" % (form, gender)
