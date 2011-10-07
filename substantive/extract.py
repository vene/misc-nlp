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
	sg = open('singular.txt', 'w', encoding='utf-8')
	pl = open('plural.txt', 'w', encoding='utf-8')
	df = open('defective.txt', 'w', encoding='utf-8')
	subst = dict()
	for form, base, pos, gender, number, case, article in \
	extract_substantives():
		if 's' not in pos:
			continue  # only take substantives
		if 'n' not in case:
			continue  # only use nominative case
		if 'ne' not in article:
			continue  # only take weak forms

		subst.setdefault(base, dict())[number] = (form, gender)
		if number not in ('sg', 'pl'):
			print base, number
	
	for base, numbers_dict in subst.items():
		if numbers_dict.has_key('sg') and numbers_dict.has_key('pl'):
			print >> sg, '%s\t%s' % numbers_dict['sg']
			print >> pl, '%s\t%s' % numbers_dict['pl']
		else:
			print >> df, '%s\t%s' % numbers_dict.get('sg', 
										             numbers_dict.get('pl',
										             (base, '??')))

	[f.close() for f in (sg, pl, df)]
