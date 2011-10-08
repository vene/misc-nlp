# -*- coding: utf8 -*-

from codecs import open
import string

def strip_accents_leave_diacritics(line):
	source_chars, target_chars = u'á÷äéíďóöú', u'aâăeiîoou'
	table = dict((ord(s), t) for s, t in zip(source_chars, target_chars))
	return line.translate(table)


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
		line = strip_accents_leave_diacritics(line)
		form, base, typestring = line.split()
		split_typestring = typestring.split('.')
		if len(split_typestring) != 6:
			print form
			continue
		pos, gender, number, case, article, _ = split_typestring
		yield form, base, pos, gender, number,  case, article

if __name__ == '__main__':
	sg, pl, sg_n, pl_n, df = files = (open(filename, 'w', encoding='utf-8') 
	                                  for filename in ('singular.txt',
	                                                   'plural.txt',
	                                                   'singular_n.txt',
	                                                   'plural_n.txt',
	                                                   'defective.txt'))
	subst = dict()
	for form, base, pos, gender, number, case, article in \
	extract_substantives():
		if 's' not in pos:
			continue  # only take substantives
		if 'n' not in case:
			continue  # only use nominative case
		if 'ne' not in article:
			continue  # only take weak forms

		subst.setdefault(base, dict())[number] = (form, gender[0])
		if number not in ('sg', 'pl'):
			print base, number
	
	for base, numbers_dict in subst.items():
		if numbers_dict.has_key('sg') and numbers_dict.has_key('pl'):
			sg_form, sg_gender = numbers_dict['sg']
			pl_form, pl_gender = numbers_dict['pl']
			if sg_gender == pl_gender:
				if sg_gender == 'm':
					print >> sg, '%s\t%d' % (sg_form, 0)
					print >> pl, '%s\t%d' % (pl_form, 0)
				if sg_gender == 'f':
					print >> sg, '%s\t%d' % (sg_form, 1)
					print >> pl, '%s\t%d' % (pl_form, 1)
				if sg_gender == 'n':
					print >> sg_n, sg_form
					print >> pl_n, pl_form
			else:
				print >> sg_n, sg_form
				print >> pl_n, pl_form

		else:
			print >> df, '%s\t%s' % numbers_dict.get('sg', 
										             numbers_dict.get('pl',
										             (base, '??')))

	[f.close() for f in files]
