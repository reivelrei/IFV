import dash_bio as dashbio
import math

from ColorScale import ColorScale
from position import Position
import operator


class FORNAPlotter:

    def __init__(self):
        pass

    def plot(self, folding, color_scale):
        clrs = self.__create_color_array(folding, color_scale is ColorScale.REGION,  color_scale is ColorScale.LOG)

        if color_scale is ColorScale.REGION:
            domain = [0, 100, 200]
            range = ['white', '#023E7D', '#5FADFC']
        else:
            domain = [0,  max(clrs.items(), key=operator.itemgetter(1))[1]]
            range = ['white', 'red']

        custom_colors = {
            'domain': domain,
            'range': range,
            'colorValues': {
                '': clrs
            }
        }

        sequences = [{
            'sequence': folding.sequence,
            'structure': folding.foldings,
            'options': {
                'applyForce': False,
                'name': folding.section.transcript
            }
        }]

        fig = dashbio.FornaContainer(id='forna'+str(int(color_scale)), sequences=sequences, height=900, width=1100,
                                     colorScheme='custom', customColors=custom_colors)
        print(fig)
        return fig

    def __create_color_array(self, folding, region, logscale):
        colors = {}
        values = []

        if not region:
            index = 0
            for base in folding.sequence:
                if folding.section.sign == '+':
                    pos = folding.section.start + index
                else:
                    pos = folding.section.end - index
                values.append(self.__find_value(folding.positions, folding.section, pos))
                index += 1

            if logscale:
                values = [math.log10(x) if x is not 0 else 0 for x in values]

        else:
            index = 0
            for base in folding.sequence:
                values.append(self.__find_block_value(index, folding.section))
                index += 1

        index = 0
        for val in values:
            colors[index] = val
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

    def __find_block_value(self, index, section):
        color = 0
        found = False
        found_block = {}
        for block in section.blocks:
            if not found:
                if block.end >= index >= block.start:
                    found = True
                    found_block = block

        if found:
            if found_block.is_utr():
                color = 200
            else:
                color = 100

        return color

