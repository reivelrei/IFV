from block import Block


# This class represents a single section for a single transcript (= a row in the .bed file)
# transcript - the transcript and name of the .fa.dbr file
# chrom -  the chromosome
# start - the start value
# end - the end value
# sign - the sign value
# thickstart - the thickstart value
# thickend - the thickend value
# block_size - the blocksizes
# block_start - the blockstarts
class Section:
    def __init__(self, transcript, chrom, start, end, sign, thickstart, thickend,  block_size, block_start):
        self.transcript = transcript
        self.chrom = chrom
        self.start = int(start)
        self.end = int(end)
        self.sign = sign
        self.thickstart = int(thickstart)
        self.thickend = int(thickend)
        self.block_size = block_size.split(",")
        self.block_start = block_start.split(",")
        self.blocks = self._calc_blocks()

    # [PRIVATE] calculates the blocks for this section
    def _calc_blocks(self):
        blocks = []
        utr_start_block_ende = self.thickstart - self.start

        blocks.append(Block("UTR_START", 0, utr_start_block_ende-1))

        index = 0
        for size in self.block_size:
            if len(size) > 0:

                if index is 0:
                    # first block
                    start = utr_start_block_ende
                    end = int(size) - 1
                    blocks.append(Block("CDS_" + str(index + 1), start, end))
                else:
                    start = int(self.block_start[index])
                    if index is len(self.block_size) - 2:
                        # last block
                        end = self.thickend - self.start
                    else:
                        # every other block
                        end = int(start) + int(size)
                    blocks.append(Block("CDS_" + str(index + 1), start, end))
                index = index+1

        blocks.append(Block("UTR_END", self.thickend+1 - self.start, self.end - self.start-1))

        #for block in blocks:
            #print(block.bezeichnung+"\t"+str(block.start)+"\t" + str(block.end))

        return blocks

    # get the name of the folder
    @staticmethod
    def get_display_name():
        return "sections"
