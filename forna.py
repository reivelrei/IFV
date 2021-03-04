import dash_bio as dashbio
import math

from color import Color
from position import Position
import operator

# This class plots a single folding using the dash-bio forna container


class Forna:

    def __init__(self):
        pass

    # plots the given folding with the given color_scale
    # folding - the folding
    # color_scale -  the color scale
    def plot(self, folding, color_scale):
        clrs = self.__create_color_array(folding, color_scale is Color.REGION, color_scale is Color.LOG)

        if color_scale is Color.REGION:
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

        fig = dashbio.FornaContainer(id='forna'+str(int(color_scale))+folding.section.transcript, sequences=sequences,
                                     height=900, width=1100, colorScheme='custom', customColors=custom_colors)
        return fig

    # [PRIVATE] creates a color array
    def __create_color_array(self, folding, region, logscale):
        colors = {}
        values = []

        key = None
        if region:
            key = Color.REGION
        else:
            if logscale:
                key = Color.LOG
            else:
                key = Color.ABSOLUTE

        try:
            colors = folding.colors[str(key)]
        except KeyError:
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
                colors[index+1] = val
                index += 1

            folding.colors[str(key)] = colors

        return colors

    # [PRIVATE] finds the value for the given parameters
    def __find_value(self, positions, section, pos):
        value = 0
        try:
            index = positions.index(Position(chromosome=section.chrom,  start=pos, end=0, mapped_reads=0))
            value = positions[index].mapped_reads
        except ValueError:
            value = 0
        return value

    # [PRIVATE] finds the block value for the given parameters
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

