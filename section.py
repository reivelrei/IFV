from Block import Block


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
                    end = int(size)
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

        blocks.append(Block("UTR_END", self.thickend+1 - self.start, self.end - self.start))

        for block in blocks:
            print(block.bezeichnung+"\t"+str(block.start)+"\t" + str(block.end))

        return blocks
