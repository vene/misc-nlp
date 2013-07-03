import codecs


def process_line(line):
    word, pos, syl = line.strip()[1:-1].split(' ', 2)
    word = word[1:-1]  # remove quotes
    syl = syl[2:-2]
    syl = syl.split(') (')
    syl = [s.rsplit(' ', 1) for s in syl]
    syl = [(phones[1:-1].split(), int(stress)) for phones, stress in syl]
    syl, stress = zip(*syl)  # transpose
    return word, pos, syl, stress


if __name__ == '__main__':
    f = codecs.open('ita.txt')
    f.next()  # skip first line
    different = total = 0
    for line in f:
        word, pos, syl, stress = process_line(line)
        if not len(word) == sum(len(s) for s in syl):
            print word, syl
            different += 1
        total += 1
    print "{} / {}".format(different, total)
