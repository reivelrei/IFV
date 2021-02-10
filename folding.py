def parse(startline, sequence, foldings):
    parts = startline.split('=')[1].split(' ')
    partsdescription = parts[3].split('::')
    partschromo = partsdescription[1].split(':')
    partsstart = partschromo[1].split('-')
    partsend = partsstart[1].split('(')

    folding = Folding(parts[1], partsdescription[0], partschromo[0], partsstart[0],
                      partsend[0], partsend[1][0], sequence, foldings)

    return folding

def parse_two(startline, sequence, foldings):
    parts = startline.split('=')[1].split(' ')

    folding = Folding(parts[1], 'TST', 'CRM', 4711, 815, '+', sequence, foldings)

    return folding


class Folding:
    def __init__(self, energy, filename, chrom, start, end, sign, sequence, foldings):
        self.energy = float(energy)
        self.fileName = filename
        self.chrom = chrom
        self.start = start
        self.end = end
        self.sequence = sequence
        self.foldings = foldings
        self.sign = sign

        self.pca_vector = []

        for c in foldings:

            if c == '.':
                self.pca_vector.append(0)
            else:
                self.pca_vector.append(1)