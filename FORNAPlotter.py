import dash_bio as dashbio

from position import Position
import operator

class FORNAPlotter:

    def __init__(self):
        self.colors = {}

    def plot(self, folding):

        try:
            clrs = self.colors[folding.section.transcript]
        except KeyError:
            self.colors[folding.section.transcript] = self.__create_color_array(folding)
            clrs = self.colors[folding.section.transcript]

        custom_colors = {
            'domain': [0, max(clrs.items(), key=operator.itemgetter(1))[1]],
            'range': ['white', 'red'],
            'colorValues': {
                '': clrs
            }
        }

        sequences = [{
            'sequence': folding.sequence,
            'structure': folding.foldings,
            'options': {
                'applyForce': False,
                'name': 'woof'
            }
        }]

        fig = dashbio.FornaContainer(id='forna', sequences=sequences, height=900, width=1100,
                                     colorScheme='custom', customColors=custom_colors)
        return fig

    def __create_color_array(self, folding):
        colors = {}
        index = 0
        for base in folding.sequence:
            if folding.section.sign == '+':
                pos = folding.section.start + index
            else:
                pos = folding.section.end - index

            colors[index+1] = self.__find_value(folding.positions, folding.section, pos)
            index += 1
        return colors

    def __find_value(self, positions, section, pos):
        value = 0
        try:
            index = positions.index(Position(chromosome=section.chrom,  start=pos, end=0, mapped_reads=0))
            value = positions[index].mapped_reads
        except ValueError:
            value = 0
        return value
