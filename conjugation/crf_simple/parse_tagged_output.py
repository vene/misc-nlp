"""
assumes $1 is a list of words and $2 is output from `crfsuite tag` but
combined into one item per row
"""

import sys
import codecs

if __name__ == '__main__':
    word_file = codecs.open(sys.argv[1], encoding='utf8')
    tag_file = open(sys.argv[2])
    out_file = codecs.open(sys.argv[3], 'w', encoding='utf8')
    for word, tagline in zip(word_file, tag_file):
        proba, tags = tagline.split(' ', 1)
        tags = tags.strip()
        print >> out_file, proba
        word_output = u''
        for letter, tag in zip(word, tags.split(' ')):
            word_output += (len(tag) - 1) * ' ' + letter + ' '
        print >> out_file, tags
        print >> out_file, word_output
        print >> out_file
