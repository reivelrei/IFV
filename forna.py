import dash_bio as dashbio
import math

from block import Block
from color import Color
from position import Position
import operator

# This class plots a single folding using the dash-bio forna container


class Forna:

    def __init__(self, block_colors):
        self.block_colors = block_colors
        pass

    # plots the given folding with the given color_scale
    # folding - the folding
    # color_scale -  the color scale
    # heatmap - the used heatmap when color_scale is not Region
    def plot(self, folding, color_scale, heatmap):
        clrs = self.__create_color_array(folding, color_scale is Color.REGION, color_scale is Color.LOG)

        if color_scale is Color.REGION:
            domain = [0, 100, 200, 300]
            rangecolors = [self._get_color('intron'), self._get_color('cds'), self._get_color('3\''),
                           self._get_color('5\'')]
        else:
            maxval = max(clrs.items(), key=operator.itemgetter(1))[1]
            steps = 0
            domain = [0, maxval / 2, maxval]
            stops = 3

            if heatmap is not None:
                values = heatmap.split(' ')
                stops = len(values) - 1
                steps = maxval / stops
                domain = [0]

                for x in range(stops):
                    if x > 0:
                        domain.append(x * steps)

                domain.append(maxval)
                rangecolors = values
            else:
                domain = [0,  maxval]
                rangecolors = ['white', 'red']



        custom_colors = {
            'domain': domain,
            'range': rangecolors,
            'colorValues': {
                '': clrs
            }
        }

        sequences = [{
            'sequence': folding.sequence,
            'structure': folding.foldings,
            'options': {
                'applyForce': False,
                'name': folding.transcript
            }
        }]
        size = 800
        fig = dashbio.FornaContainer(id='forna'+str(int(color_scale))+folding.transcript+(heatmap.replace(' ', '') if heatmap is not None else ''), sequences=sequences,
                                     height=size, width=size+300, colorScheme='custom', customColors=custom_colors)
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
                    if folding.section is not None and len(folding.positions) > 0:
                        if folding.section.sign == '+':
                            pos = folding.section.start + index
                        else:
                            pos = folding.section.end - index
                        values.append(self.__find_value(folding.positions, folding.section, pos))
                    else:
                        values.append(0)
                    index += 1

                if logscale:
                    values = [math.log10(x) if x is not 0 else 0 for x in values]

            else:
                index = 0
                for base in folding.sequence:
                    if folding.section is not None and len(folding.positions) > 0:
                        values.append(self.__find_block_value(index, folding.section))
                    else:
                        values.append(0)
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
            index = positions.index(Position(chromosome=section.chrom,  start=pos, end=0, sign=section.sign, mapped_reads=0))
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
                if found_block.is3():
                    color = 200
                else:
                    color = 300
            else:
                color = 100

        return color

    def _get_color(self, typ):
        found = None

        for entry in self.block_colors:
            if entry['label'] == typ:
                found = entry['value']

        return found if found is not None else 'black'


