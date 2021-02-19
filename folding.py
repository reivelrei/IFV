def parse(startline, sequence, foldings, section, positions):
    parts = startline.split('=')[1].split(' ')
    folding = Folding(parts[1], sequence, foldings, section, positions)

    return folding


class Folding:
    def __init__(self, energy, sequence, foldings, section, positions):
        self.energy = float(energy)
        self.sequence = sequence
        self.foldings = foldings
        self.section = section
        self.positions = positions

        self.pca_vector = []

        for c in foldings:

            if c == '.':
                self.pca_vector.append(0)
            else:
                self.pca_vector.append(1)