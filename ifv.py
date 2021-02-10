import argparse

from pca_plot import plot
from folding import parse, parse_two


class Ifv:

    def __init__(self):
        print(self)

    def main(self, args):
        input_file = 'C:/Users/Marco/IFV/data/insilico_AT5G02120.1.dbr'
        #input_file = 'C:/Users/Marco/IFV/data/AT5G02120.1.fa.dbr'
        file_version = 2

        with open(input_file, 'r') as input:
            lines = input.readlines()

        foldings = []
        sequence = ''
        heading = ''
        folding = ''

        if file_version == 1:
            for line in lines:

                if line.startswith('>'):
                    heading = line.strip()

                if not line.startswith('>') and sequence != '':
                    folding = line.strip()

                if not line.startswith('>') and sequence == '':
                    sequence = line.strip()

                if sequence != '' and heading != '' and folding != '':
                    foldings.append(parse(heading, sequence, folding))
                    heading = ''
                    folding = ''

            if sequence != '' and heading != '' and folding != '':
                foldings.append(parse(heading, sequence, folding))

        if file_version == 2:
            count  = 0
            for line in lines:

                if line.startswith('>'):
                    if sequence != '' and heading != '' and folding != '':

                        heading = heading.replace('ENERGY:', 'ENERGY = ') + 'AT5G02120.1::Chr5:419090-419773(+)'
                        foldings.append(parse_two(heading, sequence, folding))
                        heading = ''
                        folding = ''
                    count += 1
                    heading = line.strip()

                if not line.startswith('>') and count > 1:
                    folding += line.strip()

                if not line.startswith('>') and count == 1:
                    sequence += line.strip()

            if sequence != '' and heading != '' and folding != '':
                heading = heading.replace('ENERGY:', 'ENERGY = ') + 'AT5G02120.1::Chr5:419090-419773(+)'
                foldings.append(parse_two(heading, sequence, folding))

        pca_vectors = []
        labels = []
        colors = []
        for val in foldings:
            pca_vectors.append(val.pca_vector)
            labels.append(str(val.energy)+' kcal/mol')
            colors.append(val.energy)


            print(val.pca_vector)

        plot(pca_vectors, labels, colors)

if __name__ == '__main__':
    prs = argparse.ArgumentParser(
        description='Interactive Folding Visualizer')
    prs.add_argument('-i', '--input', required=False,
                     help='Working Directory')
    ifv = Ifv()
    ifv.main(prs.parse_args())

