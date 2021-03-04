

# parses different strings and create a folding object from the given parameters.
# startline - first line of the folding in the .dbr file
# sequence - the sequence of the folding found in the .dbr file
# foldings - the folding structure found in the .dbr file
# section - the section for the structure
# positions - the positions for the structure
# section_file -  name of the section file (.bed)
# position_file - name of the position file (.bedgraph)
def parse(startline, sequence, foldings, section, positions, section_file, position_file):
    parts = startline.split('=')[1].split(' ')
    folding = Folding(parts[1], sequence, foldings, section, positions, section_file, position_file)

    return folding


# This class represents a single folding structure from a fa.dbr file.
# It contains every necessary information for plotting, calculating and exporting the data.
# energy - the energy value for this folding
# sequence - the sequence of the folding found in the .dbr file
# foldings - the folding structure found in the .dbr file
# section - the section for the structure
# positions - the positions for the structure
# section_file -  name of the section file (.bed)
# position_file - name of the position file (.bedgraph)
class Folding:
    def __init__(self, energy, sequence, foldings, section, positions, section_file, position_file):
        self.energy = float(energy)
        self.sequence = sequence
        self.foldings = foldings
        self.section = section
        self.positions = positions
        self.label = energy
        self.section_file = section_file
        self.position_file = position_file
        self.colors = {}
        self.graph = {}
        self.pca_vector = []

        for c in foldings:
            if c == '.':
                self.pca_vector.append(0)
            else:
                self.pca_vector.append(1)